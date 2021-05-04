__all__ = ('EventHandlerBase', 'EventWaitforBase', 'eventlist', )

import sys

from ...backend.utils import FunctionType, RemovedDescriptor, MethodLike, WeakKeyDictionary, NEEDS_DUMMY_INIT
from ...backend.futures import Task, is_coroutine_function
from ...backend.analyzer import CallableAnalyzer

from ..core import KOKORO
from ..message import Message

from .core import EVENT_HANDLER_NAME_TO_PARSER_NAMES

def _check_name_should_break(name):
    """
    Checks whether the passed `name` is type `str`.
    
    Used inside of ``check_name`` to check whether the given variable is usable, so we should stop checking
    other alternative cases.
    
    Parameters
    ----------
    name : `Any`
    
    Returns
    -------
    should_break : `bool`
        If non empty `str` is received returns `True`, meanwhile if `None` or empty `str` is received `False`.
    
    Raises
    ------
    TypeError
        If `name` was not passed as `None` or type `str`.
    """
    if (name is None):
        return False
        
    if type(name) is not str:
        raise TypeError(f'`name` should be `None` or type `str`, got `{name.__class__.__name__}`.')
        
    if name:
        return True
    
    return False
    
def check_name(func, name):
    """
    Tries to find the given `func`'s preferred name. The check order is the following:
    - Passed `name` argument.
    - `func.__event_name__`.
    - `func.__name__`.
    - `func.__class__.__name__`.
    
    If any of these is set (or passed at the case of `name`) as `None` or as an empty string, then those are ignored.
    
    Parameters
    ----------
    func : `None` or `callable`
        The function, what preferred name we are looking for.
    name : `None` or `str`
        A directly given name value by the user. Defaults to `None` by caller (or at least sit should).
    
    Returns
    -------
    name : `str`
        The preferred name of `func` with lower case characters only.
    
    Raises
    ------
    TypeError
        - If a checked name is not `None` or `str` instance.
        - If a metaclass was given.
        - If both `name` and `func` are given as `None`.
    """
    if None is func is name:
        raise TypeError(f'Both `func` and `name` are given as `None`')
    
    while True:
        if _check_name_should_break(name):
            break
        
        if hasattr(func, '__event_name__'):
            name = func.__event_name__
            if _check_name_should_break(name):
                break
        
        #func or method
        if hasattr(func, '__name__'):
            name = func.__name__
            if _check_name_should_break(name):
                break
        
        func = type(func)
        if not issubclass(func, type) and hasattr(func, '__name__'):
            name = func.__name__
            if _check_name_should_break(name):
                break
        
        raise TypeError(f'Meta-classes are not allowed, got {func!r}.')
    
    if not name.islower():
        name = name.lower()
    return name

def check_parameter_count_and_convert(func, expected, *, name='event', can_be_async_generator=False, error_message=None):
    """
    If needed converts the given `func` to an async callable and then checks whether it expects the specified
    amount of non reserved positional arguments.
    
    `func` can be either:
    - An async `callable`.
    - A class with non async `__new__` (neither `__init__` of course) accepting no non reserved parameters,
        meanwhile it's `__call__` is async. This is the convert (or instance) case and it causes the final argument
        count check to be applied on the type's `__call__`.
    - A class with async `__new__`.
    
    After the callable was chosen, then the amount of positional arguments are checked what it expects. Reserved
    arguments, like `self` are ignored and if the callable accepts keyword only argument, then it is a no-go.
    
    If every check passed, then at the convert case instances the type and returns that, meanwhile at the other cases
    it returns the received `func`.
    
    Parameters
    ----------
    func : `callable`
        The callable, what's type and argument count will checked.
    expected : `int`
        The amount of arguments, what would be passed to the given `func` when called at the future.
    name : `str`, Optional (Keyword only)
        The event's name, what is checked and converted. Defaults to `'event'`.
    can_be_async_generator : `bool`, Optional (Keyword only)
        Whether async generators are accepted as well.
    error_message : `str`, Optional (Keyword only)
        A specified error message with what a `TypeError` will be raised at the end, if the given `func` is not async
        and neither cannot be converted to an async callable.
    
    Returns
    -------
    func : `callable`
    
    Raises
    ------
    TypeError
        - If `func` was not given as callable.
        - If `func` is not as async and neither cannot be converted to an async one.
        - If `func` expects less or more non reserved positional arguments as `expected` is.
    """
    analyzer = CallableAnalyzer(func)
    if analyzer.is_async() or (analyzer.is_async_generator() if can_be_async_generator else False):
        min_, max_ = analyzer.get_non_reserved_positional_argument_range()
        if min_ > expected:
            raise TypeError(f'A `{name}` should accept `{expected!r}` arguments, meanwhile the given callable expects '
                f'at least `{min_!r}`, got `{func!r}`.')
        
        if min_ == expected:
            return func
        
        # min < expected
        if max_ >= expected:
            return func
        
        if analyzer.accepts_args():
            return func
        
        raise TypeError(f'A `{name}` should accept `{expected}` arguments, meanwhile the given callable expects up to '
            f'`{max_!r}`, got `{func!r}`.')
    
    if analyzer.can_instance_to_async_callable() or \
            (analyzer.can_instance_to_async_generator() if can_be_async_generator else False):
        
        sub_analyzer = CallableAnalyzer(func.__call__, as_method=True)
        if sub_analyzer.is_async():
            min_, max_ = sub_analyzer.get_non_reserved_positional_argument_range()
            
            if min_ > expected:
                raise TypeError(f'A `{name}` should accept `{expected!r}` arguments, meanwhile the given callable '
                    f'after instancing expects at least `{min_!r}`, got `{func!r}`.')
            
            if min_ == expected:
                func = analyzer.instance()
                return func
            
            # min < expected
            if max_ >= expected:
                func = analyzer.instance()
                return func
            
            if sub_analyzer.accepts_args():
                func = analyzer.instance()
                return func
            
            raise TypeError(f'A `{name}` should accept `{expected}` arguments, meanwhile the given callable after '
                f'instancing expects up to `{max_!r}`, got `{func!r}`.')
            
            func = analyzer.instance()
            return func
    
    if error_message is None:
        error_message = f'Not async callable type, or cannot be instance to async: `{func!r}`.'
    
    raise TypeError(error_message)

def compare_converted(converted, non_converted):
    # function, both should be functions
    if isinstance(non_converted, FunctionType):
        return (converted is non_converted)
    
    # method, both should be methods
    if isinstance(non_converted, MethodLike):
        return (converted is non_converted)
    
    # callable object, both should be the same
    if not isinstance(non_converted, type) and hasattr(type(non_converted), '__call__'):
        return (converted is non_converted)
    
    # type, but not metaclass
    if not issubclass(non_converted, type) and isinstance(non_converted, type):
        
        # async initializer, both is type
        if is_coroutine_function(non_converted.__new__):
            return (converted is non_converted)
        
        # async call -> should be initialized already, compare the converted's type
        if hasattr(non_converted, '__call__'):
            return (type(converted) is non_converted)
    
    #meow?
    raise TypeError(f'Expected function, method or a callable object, got {non_converted!r}')




def _convert_unsafe_event_iterable(iterable, type_=None):
    """
    Converts an iterable to a list of ``EventListElement``-s. This function is called to generate a ``eventlist``
    compatible `list` to avoid handling the same cases everywhere.
    
    `iterable`'s element's can be:
    - ``EventListElement`` instance.
    - `type_` instance if given.
    - `tuple` of `1`-`3` elements (`func`, `name`, `kwargs`).
    - `dict` of keyword arguments, what contains at least 1 key: `'func'`.
    - `func` itself.
    
    Parameters
    ----------
    iterable : `iterable`
        The iterable, what's elements will be checked.
    type_ : `None `or `type`
        If `type_` was passed, then each element is pre-validated with the given type. Some extension classes might
        support behaviour.
        
        The given `type_` should implement a `from_kwargs` constructor.
    
    Returns
    -------
    result : `list` of (``EventListElement`` or ``type_``)
    
    Raises
    ------
    ValueError
        If an element of the received iterable does not matches any of the expected formats.
    """
    result = []
    for element in iterable:
        if type(element) is EventListElement:
            if (type_ is not None):
                element = type_.from_kwargs(element.func, element.name, element.kwargs)
        if type(element) is type_:
            pass
        else:
            if isinstance(element, tuple):
                element_len = len(element)
                if element_len > 3 or element_len == 0:
                    raise ValueError(f'Expected `tuple` with length 1 or 2, got `{element!r}`.')
                
                func = element[0]
                if element_len == 1:
                    name = None
                    kwargs = None
                else:
                    name = element[1]
                    if (name is not None) and (type(name) is not str):
                        raise ValueError(f'Expected `None` or `str` instance at index 1 at element: `{element!r}`')
                    
                    if element_len == 2:
                        kwargs = None
                    else:
                        kwargs = element[2]
                        if (kwargs is not None):
                            if (type(kwargs) is not dict):
                                raise ValueError(f'Expected `None` or `dict` instance at index 1 at element: '
                                    f'`{element!r}`')
                            
                            if not kwargs:
                                kwargs = None
            
            elif isinstance(element, dict):
                try:
                    func = element.pop('func')
                except KeyError:
                    raise ValueError(f'Expected all `dict` elements to contain `\'func\'` key, but was not found at '
                        f'`{element!r}`') from None
                
                name = element.pop('name', None)
                
                if element:
                    kwargs = element
                else:
                    kwargs = None
            
            else:
                func = element
                name = None
                kwargs = None
            
            if type_ is None:
                element = EventListElement(func, name, kwargs)
            else:
                element = type_.from_kwargs(func, name, kwargs)
            
        result.append(element)
        continue
    
    return result

class _EventHandlerManager:
    """
    Gives a decorator functionality to an event handler, because 'rich' event handlers still can not be used a
    decorator, their `__call__` is already allocated for handling their respective event.
    
    This class is familiar to ``eventlist``, but it directly works with the respective event handler giving an
    easy API to do operations with it.
    
    Attributes
    ----------
    parent : `Any`
        The ``_EventHandlerManager``'s parent event handler.
    _supports_from_class : `bool`
        Whether `.parent` implements `__setevent_from_class__` method.
    """
    __slots__ = ('parent', '_supports_from_class')
    
    def __init__(self, parent):
        """
        Creates an ``_EventHandlerManager`` from the given event handler.
        
        The `parent` event handler should implement the following methods:
        - `.__setevent__(func, name, **kwargs)`
        - `.__delevent__(func, name)`
        And optionally:
        - `.__setevent_from_class__(klass)`
        
        Parameters
        ----------
        parent : `Any`
            The respective event handler.
        """
        self.parent = parent
        self._supports_from_class = hasattr(type(parent), '__setevent_from_class__')
    
    def __repr__(self):
        """Returns the representation of the event handler manager."""
        return f'<{self.__class__.__name__} of {self.parent!r}>'
    
    def __call__(self, func=..., name=None, **kwargs):
        """
        Adds the given `func` to the event handler manager's parent. If `func` is not passed, then returns a
        ``._wrapper` to allow using the manager as a decorator with still passing keyword arguments.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the respective event handler.
        name : `str` or `None`, Optional
            A name to be used instead of the passed `func`'s.
        **kwargs : Keyword arguments
            Additionally passed keyword arguments to be passed with the given `func` to the event handler.
        
        Returns
        -------
        func : `callable`
            - The created instance by the respective event handler.
            - If `func` was not passed, then returns a ``._wrapper`` instance.
        """
        if func is ...:
            return self._wrapper(self, name, kwargs)
        
        # name = check_name(func, name)
        
        func = self.parent.__setevent__(func, name, **kwargs)
        return func
    
    def from_class(self, klass):
        """
        Allows the event handler manager to be able to capture a class and create add it to the parent event handler
        from it's attributes.
        
        Parameters
        ----------
        klass : `type`
            The class to capture.
        
        Returns
        -------
        func : `callable`
            The created instance by the respective event handler.
        
        Raises
        ------
        TypeError
            If the parent of the event handler manager has no support for `.from_class`.
        """
        if not self._supports_from_class:
            raise TypeError(f'`.from_class` is not supported by `{self.parent!r}`.')
        
        return self.parent.__setevent_from_class__(klass)
        
    def remove(self, func, name=None, **kwargs):
        """
        Removes the given `func` - `name` relation from the event handler manager's parent.
        
        Parameters
        ----------
        func : `callable`
            The event to be removed to the respective event handler.
        name : `str` or `None`, Optional
            A name to be used instead of the passed `func`'s.
        **kwargs : Keyword arguments
            Additional keyword arguments.
        """
        name = check_name(func, name)
        
        self.parent.__delevent__(func, name, **kwargs)
    
    class _wrapper:
        """
        When the parent ``_EventHandlerManager`` is called and `func` was not passed (so only keyword arguments were
        if any), then an instance of this class is returned to allow using ``_EventHandlerManager`` as a decorator with
        allowing passing additional keyword arguments at the same time.
        
        Attributes
        ----------
        parent : ``_EventHandlerManager``
            The owner event handler manager.
        name : `str` or `None`
            Passed `name` keyword argument, when the wrapper was created.
        kwargs : `None` or `dict` of (`str`, `Any`) items
            Additionally passed keyword arguments when the wrapper was created.
        """
        __slots__ = ('parent', 'name', 'kwargs')
        def __init__(self, parent, name, kwargs):
            """
            Creates an instance from the given parameters.
            
            Parameters
            ----------
            parent : ``_EventHandlerManager``
                The owner event handler manager.
            name : `str` or `None`
                Passed `name` keyword argument, when the wrapper was created.
            kwargs : `None` or `dict` of (`str`, `Any`) items
                Additionally passed keyword arguments when the wrapper was created.
            """
            self.parent = parent
            self.name = name
            self.kwargs = kwargs
        
        def __call__(self, func,):
            """
            Calls the wrapper's parent event handler manager with the given `func` and with the stored up name and
            with the other stored keyword arguments.
            
            Parameters
            ----------
            func : `callable`
                The function to added to the parent event handler manager's event handler.
            
            Returns
            -------
            func : `callable`
                The created instance by the respective event handler.
            
            Raises
            ------
            TypeError
                If `func` was not supplied.
            """
            if func is ...:
                raise TypeError('`func` was not supplied.')
            
            return self.parent(func, self.name, **self.kwargs)
    
    def __getattr__(self, name):
        """Returns the attribute of the event handler manager's parent."""
        return getattr(self.parent, name)
    
    def extend(self, iterable):
        """
        Extends the respective event handler with the given iterable of events.
        
        Parameters
        ----------
        iterable : `iterable`
        
        Raises
        ------
        TypeError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is not accepted by the parent
                event handler.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
        """
        if type(iterable) is eventlist:
            type_ = iterable.type
            if (type_ is not None):
                parent = self.parent
                supported_types = getattr(parent, 'SUPPORTED_TYPES', None)
                if (supported_types is None) or (type_ not in supported_types):
                    raise TypeError(f'`{parent!r}` does not supports elements of type `{type_!r}`.')
                
                for element in iterable:
                    parent.__setevent__(element, None)
                return
        else:
            iterable = _convert_unsafe_event_iterable(iterable)
        
        parent = self.parent
        for element in iterable:
            func = element.func
            name = element.name
            
            name = check_name(func, name)
            
            kwargs = element.kwargs
            if kwargs is None:
                parent.__setevent__(func, name)
            else:
                parent.__setevent__(func, name, **kwargs)
    
    def unextend(self, iterable):
        """
        Unextends the respective event handler with the given `iterable`.
        
        Parameters
        ----------
        iterable : `iterable`
        
        Raises
        ------
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute not accepted by the parent
                event handler.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
            - If any of the passed element is not stored by the parent event handler. At this case error is raised
                only at the end.
        """
        if type(iterable) is eventlist:
            type_ = iterable.type
            if (type_ is not None):
                parent = self.parent
                supported_types = getattr(parent, 'SUPPORTED_TYPES', None)
                if (supported_types is None) or (type_ not in supported_types):
                    raise TypeError(f'`{parent!r}` does not supports elements of type `{type_!r}`.')
                
                collected = []
                for element in iterable:
                    try:
                        parent.__delevent__(element, None)
                    except ValueError as err:
                        collected.append(err.args[0])

                if collected:
                    raise ValueError('\n'.join(collected)) from None
                return
        else:
            iterable = _convert_unsafe_event_iterable(iterable)
        
        collected = []
        parent = self.parent
        for element in iterable:
            func = element.func
            name = element.name
            
            name = check_name(func, name)
            
            kwargs = element.kwargs
            try:
                
                if kwargs is None:
                    parent.__delevent__(func, name)
                else:
                    parent.__delevent__(func, name, **kwargs)
            
            except ValueError as err:
                collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected)) from None


class _EventHandlerManagerRouter(_EventHandlerManager):
    """
    Wraps multiple `Client``'s ``_EventHandlerManager`` functionality together.
    
    Attributes
    ----------
    _getter : `callable`
        A callable what should return the ``_EventHandlerManager``-s of the `_EventHandlerManagerRouter`, on who the
        extension is applied.
        
        Should always get the following attributes:
        
        +-------------------------------+-----------------------------------+
        | Name                          | Value                             |
        +===============================+===================================+
        | event_handler_manager_router  | ``_EventHandlerManagerRouter``    |
        +-------------------------------+-----------------------------------+
        
        Should return the following value(s):
        
        +-------------------------------+-----------------------------------+
        | Name                          | Value                             |
        +===============================+===================================+
        | event_handlers                | `Any`                             |
        +-------------------------------+-----------------------------------+
    
    _from_class_constructor : `callable` or `None`
        Whether the extension supports `.from_class` method and how exactly it does. If set as `None`, means it not
        supports it.
        
        Should always get the following attributes:
        
        +-------------------------------+-----------------------------------+
        | Name                          | Value                             |
        +===============================+===================================+
        | klass                         | `klass`                           |
        +-------------------------------+-----------------------------------+
        
        Should returns the following value(s):
        
        +-------------------------------+-----------------------------------+
        | Name                          | Value                             |
        +===============================+===================================+
        | commands                      | `list` of `Any`                   |
        +-------------------------------+-----------------------------------+
    
    parent : ``ClientWrapper``
        The parent ``ClientWrapper``.
    """
    __slots__ = ('_getter', '_from_class_constructor', 'parent')
    
    def __init__(self, parent, getter, from_class_constructor):
        """
        Creates an ``_EventHandlerManagerRouter`` routing to all the clients of a ``ClientWrapper``.
        
        Parameters
        ----------
        parent : ``ClientWrapper``
            The respective routed client wrapper.
        getter : `callable`
            A callable what should return the ``_EventHandlerManager``-s of the `_EventHandlerManagerRouter`, on who the
            extension is applied.
            
            Should always get the following attributes:
            
            +-------------------------------+-----------------------------------+
            | Name                          | Value                             |
            +===============================+===================================+
            | event_handler_manager_router  | ``_EventHandlerManagerRouter``    |
            +-------------------------------+-----------------------------------+
            
            Should return the following value(s):
            
            +-------------------------------+-----------------------------------+
            | Name                          | Value                             |
            +===============================+===================================+
            | event_handlers                | `Any`                             |
            +-------------------------------+-----------------------------------+
        
        from_class_constructor : `None` or `callable`
            Whether the extension supports `.from_class` method and how exactly it does. If given as `None`, then it
            means it not supports it.
            
            Should always get the following attributes:
            
            +-------------------------------+-----------------------------------+
            | Name                          | Value                             |
            +===============================+===================================+
            | klass                         | `klass`                           |
            +-------------------------------+-----------------------------------+
            
            Should returns the following value(s):
            
            +-------------------------------+-----------------------------------+
            | Name                          | Value                             |
            +===============================+===================================+
            | commands                      | `list` of `Any`                   |
            +-------------------------------+-----------------------------------+
        """
        self.parent = parent
        self._getter = getter
        self._from_class_constructor = from_class_constructor
    
    def __call__(self, func=..., name=None, **kwargs):
        """
        Adds the given `func` to all of the represented client's respective event handler managers.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the respective event handler.
        name : `str` or `None` or `tuple` of `str`, optional
            A name to be used instead of the passed `func`'s.
        **kwargs : Keyword arguments
            Additionally passed keyword arguments to be passed with the given `func` to the event handler.
        
        Returns
        -------
        func : ``Routed``
           The added functions.
        """
        if func is ...:
            return self._wrapper(self, name, kwargs)
        
        handlers = self._getter(self)
        if not handlers:
            return
        
        count = len(handlers)
        
        routed_names = route_name(func, name, count)
        routed_kwargs = route_kwargs(kwargs, count)
        routed_func = maybe_route_func(func, count)
        routed = []
        for handler, func_, name, kwargs in zip(handlers, routed_func, routed_names, routed_kwargs):
            func = handler.__setevent__(func_, name, **kwargs)
            routed.append(func)
        
        return Router(routed)
    
    def from_class(self, klass):
        """
        Allows the event handler manager router to be able to capture a class and create and add it to the represented
        event handlers from it's attributes.
        
        Parameters
        ----------
        klass : `type`
            The class to capture.
        
        Returns
        -------
        routed : ``Router``
            The routed created instances.
        
        Raises
        ------
        TypeError
            If the parent of the event handler manager has no support for `.from_class`.
        BaseException
            Any exception raised by any of the event handler.
        """
        from_class_constructor = self._from_class_constructor
        if from_class_constructor is None:
            raise TypeError(f'`.from_class` is not supported by `{self.parent!r}`.')
        
        handlers = self._getter(self)
        count = len(handlers)
        if not count:
            return
        
        routed_maybe = from_class_constructor(klass)
        if isinstance(routed_maybe, Router):
            if len(routed_maybe) != count:
                raise ValueError(f'The given class is routed to `{len(routed_maybe)}`, meanwhile expected to be routed '
                    f'to `{count}` times, got {klass!r}.')
            routed = routed_maybe
        else:
            copy_method = getattr(type(routed_maybe), 'copy', None)
            if copy_method is None:
                routed = [routed_maybe for _ in range(count)]
            else:
                routed = [copy_method(routed_maybe) for _ in range(count)]
            
        for handler, event in zip(handlers, routed):
            handler.__setevent__(event, None)
        
        return routed
    
    def remove(self, func, name=None, **kwargs):
        """
        Removes the given `func` - `name` relation from the represented event handler managers.
        
        Parameters
        ----------
        func : ``Router``, `callable`
            The event to be removed to the respective event handlers.
        name : `str` or `None`
            A name to be used instead of the passed `func`'s.
        **kwargs : Keyword arguments
            Additional keyword arguments.
        """
        handlers = self._getter(self)
        
        count = len(handlers)
        if not count:
            return
        
        if isinstance(func, Router):
            name = None
        else:
            name = check_name(func, name)
        
        if isinstance(func, Router):
            if len(func) != count:
                raise ValueError(f'The given `func` is routed `{len(func)}` times, meanwhile expected to be routed '
                    f'to `{count}` times, got {func!r}.')
            
            for func, handler in zip(func, handlers):
                handler.__delevent__(func, name, **kwargs)
        
        else:
            for handler in handlers:
                handler.__delevent__(func, name, **kwargs)
    
    def extend(self, iterable):
        """
        Extends the event handler manager router's respective managers with the given iterable of events.
        
        Parameters
        ----------
        iterable : `iterable`
        
        Raises
        ------
        TypeError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is not accepted by the parent
                event handler.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
        """
        handlers = self._getter(self)
        
        count = len(handlers)
        if not count:
            return
        
        if type(iterable) is eventlist:
            type_ = iterable.type
            if (type_ is not None):
                parent = self.parent
                supported_types = getattr(handlers[0], 'SUPPORTED_TYPES', None)
                if (supported_types is None) or (type_ not in supported_types):
                    raise TypeError(f'`{parent!r}` does not supports elements of type `{type_!r}`.')
                
                for element in iterable:
                    if isinstance(element, Router):
                        if len(element) != count:
                            raise ValueError(f'The given `func` is routed `{len(element)}` times, meanwhile expected to be routed '
                                f'to `{count}` times, got {element!r}.')
                        
                        for func, handler in zip(element, handlers):
                            handler.__setevent__(func, None)
                    
                    else:
                        for handler in handlers:
                            handler.__setevent__(element, None)
                return
        else:
            iterable = _convert_unsafe_event_iterable(iterable)
        
        for element in iterable:
            name = element.name
            func = element.func
            kwargs = element.kwargs
            
            routed_names = route_name(func, name, count)
            routed_func = maybe_route_func(func, count)
            
            if kwargs is None:
                for handler, func_, name in zip(handlers, routed_func, routed_names):
                    handler.__setevent__(func_, name)
                
            else:
                routed_kwargs = route_kwargs(kwargs, count)
                for handler, func_, name, kwargs in zip(handlers, routed_func, routed_names, routed_kwargs):
                    handler.__setevent__(func_, name, **kwargs)
    
    def unextend(self, iterable):
        """
        Unextends the event handler router's represented event handlers with the given `iterable`.
        
        Parameters
        ----------
        iterable : `iterable`
        
        Raises
        ------
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute not accepted by the parent
                event handler.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
            - If any of the passed element is not stored by the parent event handler. At this case error is raised
                only at the end.
        """
        handlers = self._getter(self)
        
        count = len(handlers)
        if not count:
            return
        
        if type(iterable) is eventlist:
            type_ = iterable.type
            if (type_ is not None):
                parent = self.parent
                supported_types = getattr(handlers[0], 'SUPPORTED_TYPES', None)
                if (supported_types is None) or (type_ not in supported_types):
                    raise TypeError(f'`{parent!r}` does not supports elements of type `{type_!r}`.')
                
                collected = []
                for element in iterable:
                    if isinstance(element, Router):
                        if len(element) != count:
                            collected.append(f'The given `func` is routed `{len(element)}` times, meanwhile expected '
                                f'to be routed to `{count}` times, got {element!r}.')
                            continue
                        
                        for func, handler in zip(element, handlers):
                            try:
                                handler.__delevent__(func, None)
                            except ValueError as err:
                                collected.append(err.args[0])
                    else:
                        for handler in handlers:
                            try:
                                handler.__delevent__(element, None)
                            except ValueError as err:
                                collected.append(err.args[0])
                
                if collected:
                    raise ValueError('\n'.join(collected)) from None
                return
        else:
            iterable = _convert_unsafe_event_iterable(iterable)
        
        collected = []
        for element in iterable:
            func = element.func
            name = element.name
            kwargs = element.kwargs
            
            routed_names = route_name(func, name, count)
            routed_func = maybe_route_func(func, count)
            
            if kwargs is None:
                for handler, func_, name in zip(handlers, routed_func, routed_names):
                    try:
                        handler.__delevent__(func_, name)
                    except ValueError as err:
                        collected.append(err.args[0])
                
            else:
                routed_kwargs = route_kwargs(kwargs, count)
                for handler, func_, name, kwargs in zip(handlers, routed_func, routed_names, routed_kwargs):
                    try:
                        handler.__delevent__(func_, name, **kwargs)
                    except ValueError as err:
                        collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected)) from None
    
    def __repr__(self):
        return f'<{self.__class__.__name__} parent={self.parent!r}, getter={self._getter!r}, from_class_constructor=' \
               f'{self._from_class_constructor!r}>'

class EventListElement:
    """
    Represents an element of an ``eventlist``.
    
    Attributes
    ----------
    func : `callable`
        The event of the event-list element.
    name : `None` or `str`
        Alternative name to use instead of `func`'s.
    kwargs : `None` or `dict` of (`str`, `Any`) items
        Additional kwargs for `func`.
    """
    __slots__ = ('func', 'name', 'kwargs', )
    def __init__(self, func, name, kwargs):
        """
        Creates a ``EventListElement` from the given parameters.
        
        Parameters
        ----------
        func : `callable`
            The event of the eventlist element.
        name : `None` or `str`
            Alternative name to use instead of `func`'s.
        kwargs : `None` or `dict` of (`str`, `Any`) items
            Additional kwargs for `func`.
        """
        self.func = func
        self.name = name
        self.kwargs = kwargs
    
    def __repr__(self):
        """Returns the representation of the eventlist element."""
        return f'{self.__class__.__name__}({self.func!r}, {self.name!r}, kwargs={self.kwargs!r})'
    
    def __len__(self):
        """Additional information for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """
        Unpacks the eventlist element.
        
        This method is a generator.
        """
        yield self.func
        yield self.name
        yield self.kwargs


class Router(tuple):
    """
    Object used to describe multiple captured created command-like objects.
    """
    
    def __repr__(self):
        """Returns the router's representation."""
        result = [self.__class__.__name__, '(']
        
        limit = len(self)
        if limit:
            index = 0
            while True:
                element = self[index]
                result.append(repr(element))
                
                index += 1
                if index == limit:
                    break
                
                result.append(', ')
        
        result.append(')')
        
        return ''.join(result)

def route_value(to_route_value, count, default=None):
    """
    Routes only a single `name` - `value` pair.
    
    Parameters
    ----------
    to_route_value : `Any`
        The respective value to route
    count : `int`
        The expected amount of copies to generate.
    default : `Any`, Optional
        Optional default variable to use. Defaults to `None`.
    
    Returns
    -------
    result : `list` of `Any`
        A list of the routed values
    """
    result = []
    if isinstance(to_route_value, tuple):
        if len(to_route_value) != count:
            raise ValueError(f'The represented router has `{count}` applicable clients, meanwhile received only '
                f'`{len(to_route_value)}` routed values, got: {to_route_value!r}.')
        
        last = ...
        for value in to_route_value:
            if value is None:
                value = default
                last = default
            elif value is ...:
                if last is ...:
                    last = default
                value = last
            else:
                last = value
            
            result.append(value)
            continue
    else:
        if (to_route_value is None) or (to_route_value is ...):
            to_route_value = default
        
        for _ in range(count):
            result.append(to_route_value)
    
    return result


def route_kwargs(kwargs, count):
    """
    Routes the given `kwargs` to the given `count` amount of copies.
    
    If a value of a keyword is given as a `tuple` instance, then it will be routed by element for each applicable
    client.
    
    Parameters
    ----------
    kwargs : `dict` of (`str`, `Any`) items
        Keyword arguments to route.
    count : `int`
        The expected amount of copies to generate.

    Returns
    -------
    result : `list` of `dict` of (`str`, `Any) items
    
    Raises
    ------
    ValueError
        - A value of the given `kwargs` is given as `tuple` instance, but it's length is different from `count`.
        - If a value of `kwargs` is given as `tuple`, meanwhile it's 0th element is `Ellipsis`.
    """
    result = [{} for _ in range(count)]
    
    for name, to_route_value in kwargs.items():
        if isinstance(to_route_value, tuple):
            if len(to_route_value) != count:
                raise ValueError(f'The represented router has `{count}` applicable clients, meanwhile received only '
                    f'`{len(to_route_value)}` routed values, got: {to_route_value!r}.')
            
            last = ...
            for routed_kwargs, value in zip(result, to_route_value):
                if value is None:
                    last = None
                elif value is ...:
                    if last is ...:
                        last = None
                    value = last
                else:
                    last = value
                
                routed_kwargs[name] = value
                continue
        else:
            for routed_kwargs in result:
                routed_kwargs[name] = to_route_value
    
    return result

def route_name(func, name, count):
    """
    Routes the given `name` to the given `count` amount of copies.
    
    If `name` is given as `tuple`, then each element of it will be returned for each applicable client.
    
    Parameters
    ----------
    func : `None` or `callable`
        The respective callable to get name from if no name was passed.
    name : `None`, `Ellipsis`, `str`, `tuple` of (`None`, `Ellipsis`, `str`)
        The name to use instead of `func`'s real one.
    count : `int`
        The expected amount of names.
    
    Returns
    -------
    result : `list` of `str`
    
    Raises
    ------
    TypeError
        - If `name` was not given as `None`, `Ellipsis`, `str`, neither as `tuple` of (`None`, `Ellipsis`, `str`).
        - If both `name` and `func` are given as `None`.
    ValueError
        If `name` was given as `tuple` but it's length is different from the expected one.
    """
    result = []
    
    if isinstance(name, tuple):
        for index, name_value in enumerate(name):
            if (name_value is not None) and (name_value is not ...) and (not isinstance(name_value, str)):
                raise TypeError(f'`name` was given as a `tuple`, but it\'s {index}th element is not `None`, '
                    f'`Ellipsis`, neither `str` instance, got, {name_value.__class__.__name__}: {name_value}.')
        
        if len(name) != count:
            raise ValueError(f'`name` was given as `tuple`, but it\'s length ({len(name)!r}) not matches the expected '
                f'(`{count}`) one, got {name!r}.')
        
        last = ...
        for name_value in name:
            if name is None:
                name_value = check_name(func, None)
                last = None
            elif name_value is ...:
                if last is ...:
                    name_value = check_name(func, None)
                    last = name_value
                elif last is None:
                    name_value = check_name(func, None)
                else:
                    name_value = last
            else:
                last = name_value
            
            result.append(name_value)
    else:
        if name is None:
            name_value = check_name(func, None)
        elif isinstance(name, str):
            name_value = str(name)
        else:
            raise TypeError('`name` can be given as `None` or as `tuple` of (`None, `Ellipsis`, `str`), got: '
                f'{name.__class__.__name__}: {name!r}.')
        
        for _ in range(count):
            result.append(name_value)
    
    return result


def maybe_route_func(func, count):
    """
    Routes the given `func` `count` times if applicable.
    
    Parameters
    ----------
    Parameters
    ----------
    func : `callable`
        The respective callable to ass
    count : `int`
        The expected amount of functions to return.
    
    Returns
    -------
    result : `list` of `func`
    """
    copy_function = getattr(type(func), 'copy', None)
    result = []
    if copy_function is None:
        for _ in range(count):
            result.append(func)
    else:
        for _ in range(count):
            copied = copy_function(func)
            result.append(copied)
    
    return result


class eventlist(list):
    """
    Represents a container to store events before adding them to a client. Some extension classes might support this
    class as well.
    
    Attributes
    ----------
    _supports_from_class : `bool`
        If `type_` was passed when creating an eventlist and the it supports creation with a `from_class` class method.
    kwargs : `None` or `dict` of (`str`, `Any`) items
        Keyword arguments used for each element when extending the client's events with the event-list.
    type : `None` or `type`
        If `type_` was passed when creating the eventlist, then each added element is pre-validated with the given type
        before adding them. Some extension classes might support behaviour.
    
    Notes
    -----
    Hata's `commands` extension class supports collecting commands in ``eventlist`` and pre-validating as well with
    passing `type_` as `Command`.
    """
    insert = RemovedDescriptor()
    sort = RemovedDescriptor()
    pop = RemovedDescriptor()
    reverse = RemovedDescriptor()
    remove = RemovedDescriptor()
    index = RemovedDescriptor()
    count = RemovedDescriptor()
    __mul__ = RemovedDescriptor()
    __rmul__ = RemovedDescriptor()
    __imul__ = RemovedDescriptor()
    __add__ = RemovedDescriptor()
    __radd__ = RemovedDescriptor()
    __iadd__ = RemovedDescriptor()
    __setitem__ = RemovedDescriptor()
    __contains__ = RemovedDescriptor()
    
    __slots__ = ('_supports_from_class', 'kwargs', 'type')
    
    def __new__(cls, iterable=None, type_=None, **kwargs):
        """
        Creates a new eventlist from the the given parameters.
        
        Parameters
        ----------
        iterable : `iterable`, Optional
            An iterable of events to extend the eventlist with.
        type_ : `type`, Optional
            A type to validate each added element to the eventlist.
        **kwargs : Keyword arguments
            Additional keyword arguments to be used when adding each element.
        
        Raises
        ------
        TypeError
            If `type_` was passed as not as `type` instance, or if it has no `from_kwargs` method.
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is different.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
        """
        if (type_ is None):
            supports_from_class = False
        else:
            if not isinstance(type_, type):
                raise TypeError(f'`type_` should be `type` instance, got `{type!r}`.')
            
            if not hasattr(type_, 'from_kwargs'):
                raise TypeError('The passed `type_` has no method called `from_kwargs`.')
            
            supports_from_class = hasattr(type_, 'from_class')
        
        if not kwargs:
            kwargs = None
        
        self = list.__new__(cls)
        self.type = type_
        self._supports_from_class = supports_from_class
        self.kwargs = kwargs
        
        if (iterable is not None):
            self.extend(iterable)
        
        return self
    
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    
    class _wrapper:
        """
        When a parent ``eventlist`` is called and `func` was not passed (so only keyword arguments were if any), then
        an instance of this class is returned. It's main purpose is to enable using ``eventlist`` as a decorator with
        allowing passing additional keyword arguments at the same time.
        
        Attributes
        ----------
        parent : ``eventlist``
            The owner eventlist.
        name : `str` or `None`
            Passed `name` keyword argument, when the wrapper was created.
        kwargs : `None` or `dict` of (`str`, `Any`) items
            Additionally passed keyword arguments when the wrapper was created.
        """
        __slots__ = ('parent', 'name', 'kwargs')
        def __init__(self, parent, name, kwargs):
            """
            Creates an instance from the given parameters.
            
            Parameters
            ----------
            parent : ``eventlist``
                The owner eventlist.
            name : `str` or `None`
                Passed `name` keyword argument, when the wrapper was created by the parent ``eventlist``.
            kwargs : `None` or `dict` of (`str`, `Any`) items
                Additionally passed keyword arguments when the wrapper was created by it's parent.
            """
            self.parent = parent
            self.name = name
            self.kwargs = kwargs
        
        def __call__(self, func):
            """
            Calling an ``eventlist``'s wrapper adds the given `func` to it's parent ``eventlist``.
            
            Parameters
            ----------
            func : `callable`
                The function to add to the parent ``eventlist``.
            
            Returns
            -------
            func : `callable`
                The function if the parent  ``eventlist`` has no `.type` set. If it has then an instance of that type.
            
            Raises
            ------
            TypeError
                If `func` was not supplied.
            """
            if func is ...:
                raise TypeError('`func` was not supplied.')
            
            parent = self.parent
            type_ = parent.type
            
            if type_ is None:
                element = EventListElement(func, self.name, self.kwargs)
            else:
                element = func = type_.from_kwargs(func, self.name, self.kwargs)
            
            list.append(self.parent, element)
            return func
    
    def from_class(self, klass):
        """
        Allows the ``eventlist`` to be able to capture a class and create an element from it's attributes.
        
        Parameters
        ----------
        klass : `type`
            The class to capture.
        
        Returns
        -------
        element : `callable`
            The created instance from the eventlist's `.type`.
        
        Raises
        ------
        TypeError
            If the eventlist has no `.type` set, or if it's `.type` is not supporting this method.
        """
        type_ = self.type
        if not self._supports_from_class:
            if type_ is None:
                message = 'On `eventlist` without type `.from_class` method cannot be used.'
            else:
                message = f'The `eventlist`\'s type: `{type_!r}` is not supporting `.from_class`.'
            raise TypeError(message)
        
        # kwargs are gonna be emptied, so copy them if needed
        kwargs = self.kwargs
        if (kwargs is not None):
            kwargs = kwargs.copy()
        
        element = type_.from_class(klass, kwargs=kwargs)
        list.append(self, element)
        return element
    
    def extend(self, iterable):
        """
        Extends the ``eventlist`` with the given `iterable`.
        
        Parameters
        ----------
        iterable : `iterable`
            An iterable of events to extend the eventlist with.
        
        Raises
        ------
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is different.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
        """
        if type(iterable) is type(self):
            if self.type is not iterable.type:
                raise ValueError(f'Extending {self.__class__.__name__} with an other object of the same type, but with '
                    f'a different type, own: `{self.type!r}`, other\'s: `{iterable.type!r}`.')
        else:
            iterable = _convert_unsafe_event_iterable(iterable, self.type)
        
        list.extend(self, iterable)
    
    def unextend(self, iterable):
        """
        Unextends the eventlist with the given `iterable`.
        
        Parameters
        ----------
        iterable : `iterable`
            An iterable of events to unextend the eventlist with.
        
        Raises
        ------
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is different.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
            - If any of the passed elements is not at the ``eventlist``. At this case error is raised only at the end.
        """
        if type(iterable) is not type(self):
            iterable = _convert_unsafe_event_iterable(iterable, self.type)
        else:
            if self.type is not iterable.type:
                raise ValueError(f'Extending {self.__class__.__name__} with an other object of the same type, but with '
                    f'a different type, own: `{self.type!r}`, other\'s: `{iterable.type!r}`.')
        
        collected = []
        for element in iterable:
            try:
                self.remove(*element)
            except ValueError as err:
                collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected))
        
    def __call__(self, func=..., name = None, **kwargs):
        """
        Adds the given `func` to the ``eventlist`` with the other given keyword arguments. If `func` is not passed,
        then returns a ``._wrapper` to allow using the ``eventlist`` as a decorator with still passing keyword
        arguments.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the eventlist.
        name : `str` or `None`, Optional
            A name to be used instead of the passed `func`'s when adding it.
        **kwargs : Keyword arguments
            Additionally passed keyword arguments to be used when the passed `func` is used up.
        
        Returns
        -------
        func : `callable`
            - If `func` was passed and the eventlist has no `.type` then returns the passed `func`.
            - If `func` was passed and the eventlist has `.type` set, then returns an instance of that.
            - If `func` was not passed, then returns a ``._wrapper`` instance.
        
        Raises
        ------
        TypeError
            If `name` was passed with incorrect type.
        """
        if (name is not None):
            if type(name) is not str:
                raise TypeError(f'`name` should be `None`, or type `str`, got `{name!r}`.')
            
            if name:
                if not name.islower():
                    name = name.lower()
            else:
                name = None
        
        own_kwargs = self.kwargs
        if (own_kwargs is not None) and own_kwargs:
            for name_, value_ in own_kwargs.items():
                kwargs.setdefault(name_, value_)
        
        if func is ...:
            return self._wrapper(self, name, kwargs)
        
        type_ = self.type
        if type_ is None:
            element = EventListElement(func, name, kwargs)
        else:
            element = func = type_.from_kwargs(func, name, kwargs)
        
        list.append(self, element)
        return func
        
    def remove(self, func, name=None):
        """
        Removes an element of the eventlist.
        
        Parameters
        ----------
        func : `callable`
            The function to remove.
        name : `str`, Optional
            The name of the function to remove.

        Raises
        ------
        TypeError
            If `name` was passed with incorrect type.
        ValueError
            If the passed `func` - `name` combination was not found.
        """
        if (name is not None):
            if type(name) is not str:
                raise TypeError(f'`name` should be `None`, or type `str`, got `{name!r}`.')
            
            if name:
                if not name.islower():
                    name = name.lower()
            else:
                name = None
        
        # we might overwrite __iter__ later
        for element in list.__iter__(self):
            
            converted_name = element.name
            # `name` can be `None` or `str`
            if converted_name is None:
                if name is not None:
                    continue
            else:
                if name is None:
                    continue
                
                if converted_name != name:
                    continue
            
            if compare_converted(element.func, func):
                return
        
        raise ValueError(f'Did not find any element, what matched the passed func={func!r}, name={name!r} combination.')
    
    def __repr__(self):
        """Returns the representation of the eventlist."""
        result = [
            self.__class__.__name__,
            '([',
        ]
        
        limit = list.__len__(self)
        if limit != 0:
            index = 0
            
            while True:
                element=list.__getitem__(self, index)
                result.append(repr(element))
                index +=1
                
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        result.append(']')
        
        type_ = self.type
        if (type_ is not None):
            result.append(', type=')
            result.append(repr(type_))
        
        kwargs = self.kwargs
        if (kwargs is not None):
            result.append(', kwargs=')
            result.append(repr(kwargs))
        
        result.append(')')
        return ''.join(result)
    
    def add_kwargs(self, **kwargs):
        """
        Adds keyword arguments to the ``eventlist`'s.
        
        Parameters
        ----------
        **kwargs : Keyword arguments
            KeyWord arguments to extend the ``eventlist``'s with.
        """
        if not kwargs:
            return
        
        own_kwargs = self.kwargs
        if own_kwargs is None:
            self.kwargs = kwargs
        else:
            own_kwargs.update(kwargs)
    
    def remove_kwargs(self, *names):
        """
        Removes keyword arguments of the ``eventlist`` by their name.
        
        Parameters
        ----------
        *names : Arguments
            Keyword argument's name added to the ``eventlist``.
        """
        if not names:
            return
        
        own_kwargs = self.kwargs
        if own_kwargs is None:
            return
        
        for name in names:
            try:
                del own_kwargs[name]
            except KeyError:
                pass
        
        if not own_kwargs:
            self.kwargs = None
    
    def clear_kwargs(self):
        """
        Clears the kwargs of the eventlist.
        """
        self.kwargs = None

# This class is a placeholder for the `with` statement support also for the `shortcut` property as well.
class EventHandlerBase:
    """
    Base class for event handlers.
    """
    __slots__ = ()
    
    # subclasses should overwrite it
    async def __call__(self, *args):
        """
        The method what will be called by the respective parser. The first received argument is always a ``Client``
        meanwhile the rest depends on the dispatch event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        *args : Additional positional arguments
        """
        pass
    
    # subclasses should overwrite it
    def __setevent__(self, func, name):
        """
        Adds the specified event to the event handler. Subclasses might add additional keyword arguments as well.
        
        Parameters
        ----------
        func : `callable`
            The callable to be added.
        name : `str` or `None`
            The name of the event to use over the `func`'s.
        
        Returns
        -------
        func : `callable`
            The created event.
        """
        pass

    # subclasses should overwrite it
    def __delevent__(self, func, name):
        """
        Removes the specified event from the event handler. Subclasses might add additional keyword arguments as well.
        
        Parameters
        ----------
        func : `callable`
            The callable to be removed.
        name : `str` or `None`
            The name of the event when searching for `func`. When `func` was added with `name` passed as non `None`,
            then here `name` should be passed with the same name.
        
        Raises
        ------
        ValueError
            The event handler not contains the given `func` - `name` combination.
        """
        pass

    @property
    def shortcut(self):
        """
        Shortcuts the event handler's event adding and removing functionality to make those operations easier.
        
        Returns
        -------
        event_handler_manager : ``_EventHandlerManager``
        """
        return _EventHandlerManager(self)

class EventWaitforMeta(type):
    """
    Metaclass for `waitfor` event handlers
    
    The defaultly supported events are the following:
    - `message_create`
    - `message_edit`
    - `message_delete`
    - `channel_create`
    - `channel_edit`
    - `channel_delete`
    - `role_create`
    - `role_edit`
    - `role_delete`
    - `guild_delete`
    - `guild_edit`
    - `emoji_edit`
    - `emoji_delete`
    - `reaction_add`
    - `reaction_delete`
    
    See Also
    --------
    ``EventWaitforBase`` : Base class to inherit instead of meta-classing ``EventWaitforMeta``.
    """
    def __call__(cls, *args, **kwargs):
        """
        Instances the type.
        
        Auto-adds a `.waitfors` instance attribute to them and also sets it as a `WeakKeyDictionary`, so you would not
        need to bother with that.
        
        Parameters
        ----------
        *args : Additional positional arguments
        **kwargs : Additional keyword arguments
        
        Returns
        -------
        object_ : `Any`
        """
        object_ = cls.__new__(cls, *args, **kwargs)
        if type(object_) is not cls:
            return object_
        
        object_.waitfors = WeakKeyDictionary()
        cls.__init__(object_, *args, **kwargs)
        return object_
    
    _call_waitfors = {}
    
    async def _call_message_create(self, client, message):
        args = (client, message)
        channel = message.channel
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
        
    _call_waitfors['message_create'] = _call_message_create
    del _call_message_create
    
    async def _call_message_edit(self, client, message, old_attributes):
        args = (client, message, old_attributes)
        channel = message.channel
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['message_edit'] = _call_message_edit
    del _call_message_edit
    
    async def _call_message_delete(self, client, message,):
        args = (client, message)
        channel = message.channel
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['message_delete'] = _call_message_delete
    del _call_message_delete
    
    async def _call_typing(self, client, channel, user, timestamp):
        args = (client, channel, user, timestamp)
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['typing'] = _call_typing
    del _call_typing
    
    async def _call_channel_create(self, client, channel):
        guild = channel.guild
        if guild is None:
            return
        args = (client, channel)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['channel_create'] = _call_channel_create
    del _call_channel_create
    
    async def _call_channel_edit(self, client, channel, old_attributes):
        args = (client, channel, old_attributes)
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['channel_edit'] = _call_channel_edit
    del _call_channel_edit
    
    async def _call_channel_delete(self, client, channel, guild):
        args = (client, channel, guild)
        self._run_waitfors_for(channel, args)
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['channel_delete'] = _call_channel_delete
    del _call_channel_delete
    
    async def _call_role_create(self, client, role):
        args = (client, role)
        guild = role.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_create'] = _call_role_create
    del _call_role_create
    
    async def _call_role_edit(self, client, role, old_attributes):
        args = (client, role, old_attributes)
        self._run_waitfors_for(role, args)
        guild = role.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_edit'] = _call_role_edit
    del _call_role_edit

    async def _call_role_delete(self, client, role, guild):
        args = (client, role, guild)
        self._run_waitfors_for(role, args)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_delete'] = _call_role_delete
    del _call_role_delete
    
    async def _call_guild_delete(self, client, guild, profile):
        args = (client, guild, profile)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['guild_delete'] = _call_guild_delete
    del _call_guild_delete
    
    async def _call_guild_edit(self, client, guild, old_attributes):
        args = (client, guild, old_attributes)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['guild_edit'] = _call_guild_edit
    del _call_guild_edit
    
    async def _call_emoji_create(self, client, emoji):
        args = (client, emoji)
        guild = emoji.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_create'] = _call_emoji_create
    del _call_emoji_create
    
    async def _call_emoji_edit(self, client, emoji, old_attributes):
        args = (client, emoji, old_attributes)
        self._run_waitfors_for(emoji, args)
        guild = emoji.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_edit'] = _call_emoji_edit
    del _call_emoji_edit

    async def _call_emoji_delete(self, client, emoji, guild):
        args = (client, emoji, guild)
        self._run_waitfors_for(emoji, args)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_delete'] = _call_emoji_delete
    del _call_emoji_delete
    
    async def _call_reaction_add(self, client, event):
        message = event.message
        if not isinstance(message, Message):
            return
        
        args = (client, event)
        self._run_waitfors_for(message, args)
    
    _call_waitfors['reaction_add'] = _call_reaction_add
    del _call_reaction_add
    
    async def _call_reaction_delete(self, client, event):
        message = event.message
        if not isinstance(message, Message):
            return
        
        args = (client, event)
        self._run_waitfors_for(message, args)
    
    _call_waitfors['reaction_delete'] = _call_reaction_delete
    del _call_reaction_delete

class EventWaitforBase(EventHandlerBase, metaclass=EventWaitforMeta):
    """
    Base class for event handlers, which implement waiting for a specified action to occur.
    
    Attributes
    ----------
    waitfors : `WeakValueDictionary` of (``DiscordEntity``, `async-callable`) items
        An auto-added container to store `entity` - `async-callable` pairs.
    
    Class Attributes
    ----------------
    __event_name__ : `None` or `str` = `None`
        Predefined name to what the event handler will be added.
    call_waitfors : `None` or `async callable` = `None`
        An added method to subclasses to ensure the waitfors if overwrite `__call__` is overwritten. Subclasses can
        also overwrite `call_waitfors` method as well.
    """
    __slots__ = ('waitfors', )
    __event_name__ = None
    call_waitfors = None
    
    def append(self, target, waiter):
        """
        Adds a new relation to `.waitfors`.
        
        When the respective event is received with the specified `target` entity, then `waiter` will be ensured.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
            The target entity, to what relative waiters will be called.
        waiter : `async callable`
            Waiter to call every time a respective event to `target` is received.
        """
        try:
            actual = self.waitfors[target]
            if type(actual) is asynclist:
                list.append(actual, waiter)
            else:
                self.waitfors[target] = container = asynclist()
                list.append(container, actual)
                list.append(container, waiter)
        except KeyError:
            self.waitfors[target] = waiter
    
    def remove(self, target, waiter):
        """
        Removes the specified relation from `.waitfors`.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
            The entity on what the given waiter waits for the respective event.
        waiter : `async callable`
            The waiter, what is called with the respective parameters if the respective event occurs related to the
            given `target`.
        """
        try:
            container = self.waitfors.pop(target)
        except KeyError:
            return
        
        if type(container) is not asynclist:
            return
        
        try:
            list.remove(container, waiter)
        except ValueError:
            pass
        else:
            if len(container) == 1:
                self.waitfors[target] = container[0]
                return
        
        self.waitfors[target] = container
    
    def get_waiter(self, target, waiter, by_type = False, is_method=False):
        """
        Looks up whether any of the given `target` - `waiter` relation is stored inside of `.waiters` and if there is any,
        then returns the first find. If non, then returns `None`.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
            The target entity.
        waiter : `Any`
            The waiter. `by_type` and `is_method` overwrite the behaviour of checking it.
        by_type : `bool`, Optional
            Whether `waiter` was given as the type of the real waiter. Defaults to `False`.
        is_method : `bool`, Optional
            Whether the real waiter is a method-like, and you want to check it's "self". Applied before `by_type` and
            defaults to `False`.
        
        Returns
        -------
        waiter : `Any`
        """
        try:
            element = self.waitfors[target]
        except KeyError:
            return None
        
        if type(element) is asynclist:
            for element in element:
                if is_method:
                    if not isinstance(element, MethodLike):
                        continue
                    
                    element = element.__self__
                
                if by_type:
                    if type(element) is waiter:
                        return element
                    else:
                        continue
                else:
                    if element == waiter:
                        return element
                    else:
                        continue
            
            return None
        
        else:
            if is_method:
                if not isinstance(element, MethodLike):
                    return None
                
                element = element.__self__
            
            if by_type:
                if type(element) is waiter:
                    return element
                else:
                    return None
            else:
                if element == waiter:
                    return element
                else:
                    return None

    def get_waiters(self, target, waiter, by_type=False, is_method=False):
        """
        Looks up the waiters of `target` - `waiter` relation stored inside of `.waiters` and returns all the matched
        one.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
            The target entity.
        waiter : `Any`
            The waiter. `by_type` and `is_method` overwrite the behaviour of checking it.
        by_type : `bool`, Optional
            Whether `waiter` was given as the type of the real waiter. Defaults to `False`.
        is_method : `bool`, Optional
            Whether the real waiter is a method-like, and you want to check it's "self". Applied before `by_type` and
            defaults to `False`.
        
        Returns
        -------
        waiters : `list` of `Any`
        """
        result = []
        
        try:
            element = self.waitfors[target]
        except KeyError:
            return result
        
        if type(element) is asynclist:
            for element in element:
                if is_method:
                    if not isinstance(element, MethodLike):
                        continue
                    
                    element = element.__self__
                
                if by_type:
                    if type(element) is not waiter:
                        continue
                else:
                    if element != waiter:
                        continue
                
                result.append(element)
                continue
        
        else:
            if is_method:
                if not isinstance(element, MethodLike):
                    return result
                
                element = element.__self__
            
            if by_type:
                if type(element) is waiter:
                    result.append(element)
            else:
                if element == waiter:
                    result.append(element)
        
        return result
    
    def _run_waitfors_for(self, target, args):
        """
        Runs the waitfors of the given target.
        
        Parameters
        ----------
        target : ``DiscordEntity`` instance
            The target entity.
        args : `tuple` of `Any`
            Arguments to ensure the waitfors with.
        """
        try:
            event = self.waitfors[target]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                for event in event:
                    Task(event(*args), KOKORO)
            else:
                Task(event(*args), KOKORO)

def EventWaitforMeta__new__(cls, class_name, class_parents, class_attributes):
    """
    Subclasses ``EventWaitforBase``.
    
    Parameters
    ----------
    class_name : `str`
        The created class's name.
    class_parents : `tuple` of `type` instances
        The superclasses of the creates type.
    class_attributes : `dict` of (`str`, `Any`) items
        The class attributes of the created type.
    
    Returns
    -------
    type : ``EventWaitforMeta`` instance
        The created type.
    
    Raises
    ------
    TypeError
        - If the class do not inherits ``EventWaitforBase``.
        - If `.__event_name__` was not set or was no set correctly. (Note that if was not ste, then the class's name
            is used instead.)
        - If there is no predefined `call_waitfors` for the class and it does not defines one either.
    """
    for base in class_parents:
        if issubclass(base,EventWaitforBase):
            break
    else:
        raise TypeError(f'`{cls.__name__} should be only the metaclass of `{EventWaitforBase.__name__}`.')
    
    event_name = class_attributes.get('__event_name__', None)
    if event_name is None:
        event_name = class_name
    
    if event_name not in EVENT_HANDLER_NAME_TO_PARSER_NAMES:
        raise TypeError(f'`{class_name}.__event_name__` is not set, or not set correctly.')
    
    if (class_attributes.get('call_waitfors', None) is None):
        try:
            call_waitfors = cls._call_waitfors[event_name]
        except KeyError:
            raise TypeError(f'The following event name: `{event_name!r}` has no auto `call_waitfor` added. Please '
                'define one.')
        
        class_attributes['call_waitfors'] = call_waitfors
        
        try:
            call = class_attributes.get('__call__', None)
        except KeyError:
            call = None
        
        if (call is None) or (call is EventHandlerBase.__call__):
            class_attributes['__call__'] = call_waitfors
    
    return type.__new__(cls, class_name, class_parents, class_attributes)

EventWaitforMeta.__new__ = EventWaitforMeta__new__
del EventWaitforMeta__new__

class ChunkWaiter(EventHandlerBase):
    __slots__ = ('waiters',)
    __event_name__ = 'guild_user_chunk'
    def __init__(self):
        self.waiters = {}
    
    # Interact directly with `self.waiters` instead.
    def __setevent__(self, waiter, nonce):
        """
        Raises
        ------
        RuntimeError
            Interact with self.waiters instead.
        """
        raise RuntimeError('Interact with self.waiters instead.')
    
    def __delevent__(self, waiter, nonce):
        """
        Raises
        ------
        RuntimeError
            Interact with self.waiters instead.
        """
        raise RuntimeError('Interact with self.waiters instead.')
    
    async def __call__(self, client, event):
        """
        Ensures that the chunk waiter for the specified nonce is called and if it returns `True` it is removed from the
        waiters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client, who received the respective dispatch event.
        event : ``GuildUserChunkEvent``
            The received guild user chunk event.
        """
        nonce = event.nonce
        if nonce is None:
            return
        
        waiters = self.waiters
        try:
            waiter = waiters[nonce]
        except KeyError:
            return
        
        if waiter(event):
            del waiters[nonce]


async def default_error_event(client, name, err):
    """
    Defaults error event for client. Renders the given exception to `sys.stderr`.
    
    This function is a generator.
    
    Parameters
    ----------
    client : ``client``
        The client who caught the error.
    name : `str`
        Identifier name of the place where the error occurred.
    err : `Any`
        The caught exception. Can be given as non `BaseException` instance as well.
    """
    extracted = [
        client.full_name,
        ' ignores occurred exception at ',
        name,
        '\n',
    ]
    
    if isinstance(err, BaseException):
        await KOKORO.render_exc_async(err, extracted)
        return
    
    if not isinstance(err, str):
        err = repr(err)
    
    extracted.append(err)
    extracted.append('\n')
    
    sys.stderr.write(''.join(extracted))

class asynclist(list):
    """
    Container used by events to call more events and by waitfor events to call more waiters.
    """
    __slots__ = ()
    
    def __init__(self, iterable=None):
        """
        Creates a new asynclist from the given iterable.
        
        Parameters
        ----------
        iterable : `iterable`, Optional
        """
        if (iterable is not None):
            list.extend(self, iterable)
    
    async def __call__(self, *args):
        """
        Ensures the contained async callables on the client's loop.
        
        This method is a coroutine.
        
        Parameters
        ----------
        *args : Additional position arguments
            Arguments to call with the contained async callables.
        """
        for coro in list.__iter__(self):
            Task(coro(*args), KOKORO)
    
    def __repr__(self):
        """Returns the asynclist's representation."""
        result = [
            self.__class__.__name__,
            '([']
        
        
        limit = list.__len__(self)
        if limit:
            index = 0
            while True:
                element = list.__getitem__(self, index)
                result.append(repr(element))
                
                index += 1
                if index == limit:
                    break
                
                result.append(', ')
                continue
        
        result.append('])')
        
        return ''.join(result)
    
    def __getattribute__(self, name):
        """Gets the given attribute from the elements of the asynclist."""
        if not isinstance(name, str):
            raise TypeError(f'Attribute name must be string, not `{name.__class__.__name__}`.')
        
        try:
            attribute = object.__getattribute__(self, name)
        except AttributeError:
            pass
        else:
            if attribute is not ...:
                return attribute
        
        for coro in list.__iter__(self):
            attribute = getattr(coro, name, ...)
            if attribute is ...:
                continue
            
            return attribute
        
        raise AttributeError(f'`{self.__class__.__name__}` object has no attribute `{name}`.')
    
    append = ...
    clear = ...
    copy = ...
    count = ...
    extend = ...
    index = ...
    insert = ...
    pop = ...
    remove = ...
    reverse = ...
    sort = ...


async def _with_error(client, task):
    """
    Runs the given awaitable and if it raises, calls `client.events.error` with the exception.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client, who's `client.events.error` will be called.
    task : `awaitable`
        The awaitable to run.
    """
    try:
        await task
    except BaseException as err:
        await client.events.error(client, repr(task), err)
