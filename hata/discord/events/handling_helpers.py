__all__ = ('EventHandlerBase', 'EventWaitforBase', 'eventlist', )

from functools import partial as partial_func
from types import FunctionType

from scarletio import (
    CallableAnalyzer, MethodLike, RemovedDescriptor, RichAttributeErrorBaseType, Task, TaskGroup, WeakKeyDictionary,
    is_coroutine_function
)
from scarletio.utils.compact import NEEDS_DUMMY_INIT

from ..core import KOKORO
from ..message import Message

from .core import DEFAULT_EVENT_HANDLER, EVENT_HANDLER_NAME_TO_PARSER_NAMES


def _check_name_should_break(name):
    """
    Checks whether the passed `name` is type `str`.
    
    Used inside of ``check_name`` to check whether the given variable is usable, so we should stop checking
    other alternative cases.
    
    Parameters
    ----------
    name : `object`
    
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
        raise TypeError(
            f'`name` can be `None`, `str`, got {name.__class__.__name__}; {name!r}.'
        )
        
    if name:
        return True
    
    return False


def check_name(func, name):
    """
    Tries to find the given `func`'s preferred name. The check order is the following:
    - Passed `name` parameter.
    - `func.__event_name__`.
    - `func.__name__`.
    - `func.__class__.__name__`.
    
    If any of these is set (or passed at the case of `name`) as `None` or as an empty string, then those are ignored.
    
    Parameters
    ----------
    func : `None`, `callable`
        The function, what preferred name we are looking for.
    name : `None`, `str`
        A directly given name value by the user. Defaults to `None` by caller (or at least sit should).
    
    Returns
    -------
    name : `str`
        The preferred name of `func` with lower case characters only.
    
    Raises
    ------
    TypeError
        - If a checked name is not `None`, `str`.
        - If a metaclass was given.
        - If both `name` and `func` are given as `None`.
    """
    if None is func is name:
        raise TypeError(
            f'Both `func` and `name` parameters are `None`'
        )
    
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
        
        raise TypeError(
            f'Meta-classes are not allowed, got {func!r}.'
        )
    
    if not name.islower():
        name = name.lower()
    
    return name


def check_parameter_count_and_convert(
    func, expected, *, name = 'event', can_be_async_generator = False, error_message = None
):
    """
    If needed converts the given `func` to an async callable and then checks whether it expects the specified
    amount of non reserved positional parameters.
    
    `func` can be either:
    - An async `callable`.
    - A class with non async `__new__` (neither `__init__` of course) accepting no non reserved parameters,
        meanwhile it's `__call__` is async. This is the convert (or instance) case and it causes the final parameter
        count check to be applied on the type's `__call__`.
    - A class with async `__new__`.
    
    After the callable was chosen, then the amount of positional parameters are checked what it expects. Reserved
    parameters, like `self` are ignored and if the callable accepts keyword only parameter, then it is a no-go.
    
    If every check passed, then at the convert case instances the type and returns that, meanwhile at the other cases
    it returns the received `func`.
    
    Parameters
    ----------
    func : `callable`
        The callable, what's type and parameter count will checked.
    expected : `int`
        The amount of parameters, what would be passed to the given `func` when called at the future.
    name : `str` = `'event'`, Optional (Keyword only)
        The event's name, what is checked and converted. Defaults to `'event'`.
    can_be_async_generator : `bool` = `False`, Optional (Keyword only)
        Whether async generators are accepted as well.
    error_message : `None`, `str` = `None`, Optional (Keyword only)
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
        - If `func` expects less or more non reserved positional parameters as `expected` is.
    """
    analyzer = CallableAnalyzer(func)
    if analyzer.is_async() or (analyzer.is_async_generator() if can_be_async_generator else False):
        min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
        if min_ > expected:
            raise TypeError(
                f'`{name}` should accept `{expected!r}` parameters, meanwhile the given callable expects '
                f'at least `{min_!r}`, got {func!r}.'
            )
        
        if min_ == expected:
            return func
        
        # min < expected
        if max_ >= expected:
            return func
        
        if analyzer.accepts_args():
            return func
        
        raise TypeError(
            f'`{name}` should accept `{expected}` parameters, meanwhile the given callable expects up to '
            f'`{max_!r}`, got {func!r}.'
        )
    
    if (
        analyzer.can_instance_to_async_callable() or
        (analyzer.can_instance_to_async_generator() if can_be_async_generator else False)
    ):
        sub_analyzer = CallableAnalyzer(func.__call__, as_method=True)
        if sub_analyzer.is_async():
            min_, max_ = sub_analyzer.get_non_reserved_positional_parameter_range()
            
            if min_ > expected:
                raise TypeError(
                    f'`{name}` should accept `{expected!r}` parameters, meanwhile the given callable '
                    f'after instancing expects at least `{min_!r}`, got {func!r}.'
                )
            
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
            
            raise TypeError(
                f'`{name}` should accept `{expected}` parameters, meanwhile the given callable after '
                f'instancing expects up to {max_!r}, got `{func!r}`.'
            )
            
            func = analyzer.instance()
            return func
    
    if error_message is None:
        error_message = f'Not async callable type, or cannot be instance to async: `{func!r}`.'
    
    raise TypeError(error_message)


def compare_converted(converted, non_converted):
    """
    Compares a maybe instance-able type to an instanced object.
    
    Parameters
    ----------
    converted : `object`
        The already converted object.
    non_converted : `object`
        The not yet converted instance to match `converted` on.
    
    Returns
    -------
    matches : `bool`
        Whether `converted` is matched by `non_converted.
    """
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
    
    # meow?
    raise TypeError(
        f'Expected function, method or a callable object, got {non_converted!r}'
    )


def _convert_unsafe_event_iterable(iterable, type_ = None):
    """
    Converts an iterable to a list of ``EventListElement``-s. This function is called to generate a ``eventlist``
    compatible `list` to avoid handling the same cases everywhere.
    
    `iterable`'s element's can be:
    - ``EventListElement``.
    - `type_` if given.
    - `tuple` of `1`-`3` elements (`func`, `args`, `kwargs`).
    - `func` itself.
    
    Parameters
    ----------
    iterable : `iterable`
        The iterable, what's elements will be checked.
    type_ : `None`, `type` = `None`, Optional
        If `type_` was passed, then each element is pre-validated with the given type. Some extension classes might
        support behaviour.
        
        The given `type_` should implement a `from_args_kwargs` constructor.
    
    Returns
    -------
    result : `list` of (``EventListElement``, ``type_``)
    
    Raises
    ------
    ValueError
        If an element of the received iterable does not matches any of the expected formats.
    """
    result = []
    for element in iterable:
        if type(element) is EventListElement:
            if (type_ is not None):
                element = type_.from_args_kwargs(element.func, element.args, element.kwargs)
        
        if isinstance(element, type_):
            pass
        
        else:
            if isinstance(element, tuple):
                element_length = len(element)
                if element_length > 3 or element_length == 0:
                    raise ValueError(
                        f'Expected `tuple` with length 1 or 2, got {element_length!r}; {element!r}.'
                    )
                
                func = element[0]
                if element_length == 1:
                    args = None
                    kwargs = None
                else:
                    args = element[1]
                    if (args is not None) and not isinstance(args, tuple):
                        raise ValueError(
                            f'Expected `None`, `tuple` at index 1 of an element, got {element!r}.'
                        )
                    
                    if element_length == 2:
                        kwargs = None
                    else:
                        kwargs = element[2]
                        if (kwargs is not None):
                            if (type(kwargs) is not dict):
                                raise ValueError(
                                    f'Expected `None`, `dict` at index 2 of an element: got {element!r}.'
                                )
                            
                            if not kwargs:
                                kwargs = None
            
            else:
                func = element
                args = None
                kwargs = None
            
            if type_ is None:
                element = EventListElement(func, args, kwargs)
            else:
                element = type_.from_args_kwargs(func, args, kwargs)
        
        result.append(element)
        continue
    
    return result


def create_event_from_class(constructor, klass, parameter_names, name_name, event_name):
    """
    Creates an event passing trough a constructor.
    
    Parameters
    ----------
    klass : `type`
        The type to work with.
    parameter_names : `tuple` of `str`
        The parameters names to pass to the constructor.
    name_name : `None`, `str`
        The event's name's name.
    event_name : `str`
        The event's name. If event is not found, then defaults to `name_name`'s found value if any.
    
    Returns
    -------
    instance : `object`
        The created instance.
    
    Raises
    ------
    BasesException
        object occurred exception.
    """
    if not isinstance(klass, type):
        raise TypeError(
            f'`klass` can be `type`, got {klass.__class__.__name__}; {klass!r}.'
        )
    
    parameters_by_name = {}
    for parameter_name in parameter_names:
        try:
            parameter = getattr(klass, parameter_name)
        except AttributeError:
            found = False
            parameter = None
        else:
            found = True
        
        parameters_by_name[parameter_name] = (parameter, found)
    
    name = klass.__name__
    if (name_name is not None) and (not parameters_by_name[name_name][1]):
        parameters_by_name[name_name] = (name, True)
    
    if not parameters_by_name[event_name][1]:
        try:
            parameter = getattr(klass, name)
        except AttributeError:
            pass
        else:
            parameters_by_name[event_name] = (parameter, True)
    
    return constructor(*(parameters_by_name[parameter_name][0] for parameter_name in parameter_names))


class _EventHandlerManager(RichAttributeErrorBaseType):
    """
    Gives a decorator functionality to an event handler, because 'rich' event handlers still can not be used a
    decorator, their `__call__` is already allocated for handling their respective event.
    
    This class is familiar to ``eventlist``, but it directly works with the respective event handler giving an
    easy API to do operations with it.
    
    Attributes
    ----------
    parent : `object`
        The ``_EventHandlerManager``'s parent event handler.
    """
    __slots__ = ('parent',)
    
    def __init__(self, parent):
        """
        Creates an ``_EventHandlerManager`` from the given event handler.
        
        The `parent` event handler should implement the following methods:
        - `.create_event(func, *args, **kwargs)`
        - `.delete_event(func)`
        And optionally:
        - `.create_event_from_class(klass)`
        
        Parameters
        ----------
        parent : `object`
            The respective event handler.
        """
        self.parent = parent
    
    
    def __repr__(self):
        """Returns the representation of the event handler manager."""
        return f'<{self.__class__.__name__} of {self.parent!r}>'
    
    
    def __call__(self, func = ..., *args, **kwargs):
        """
        Adds the given `func` to the event handler manager's parent. If `func` is not passed, then returns a
        ``._wrapper` to allow using the manager as a decorator with still passing keyword parameters.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the respective event handler.
        *args : Positional parameters
            Additionally passed positional parameters to be passed with the given `func` to the event handler.
        **kwargs : Keyword parameters
            Additionally passed keyword parameters to be passed with the given `func` to the event handler.
        
        Returns
        -------
        func : `callable`
            - The created instance by the respective event handler.
            - If `func` was not passed, then returns a ``._wrapper``.
        """
        if func is ...:
            return partial_func(self, *args, **kwargs)
        
        func = self.parent.create_event(func, *args, **kwargs)
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
        from_class_constructor = getattr(type(self.parent), 'create_event_from_class', None)
        if (from_class_constructor is None):
            raise TypeError(
                f'`.from_class` is not supported by {self.parent!r}.'
            )
        
        return from_class_constructor(self.parent, klass)
    
    
    def remove(self, func, *args, **kwargs):
        """
        Removes the given `func` from the event handler manager's parent.
        
        Parameters
        ----------
        func : `callable`
            The event to be removed to the respective event handler.
        *args : Positional parameters
            Additional positional parameters.
        **kwargs : Keyword parameters
            Additional keyword parameters.
        """
        self.parent.delete_event(func, *args, **kwargs)
    
    
    def __getattr__(self, name):
        """Returns the attribute of the event handler manager's parent."""
        try:
            return getattr(self.parent, name)
        except AttributeError:
            pass
        
        # pass at exception handling to remove cause
        RichAttributeErrorBaseType.__getattr__(self, name)
    
    
    def __dir__(self):
        """Returns the attribute names of the object."""
        return sorted(set(object.__dir__(self)) | set(dir(self.parent)))
        
    
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
                    raise TypeError(
                        f'`{parent!r}` does not support elements of type {type_!r}; got {iterable!r}.'
                    )
                
                for element in iterable:
                    parent.create_event(element)
                return
        else:
            iterable = _convert_unsafe_event_iterable(iterable)
        
        parent = self.parent
        for element in iterable:
            func = element.func
            args = element.args
            kwargs = element.kwargs
            if args is None:
                if kwargs is None:
                    parent.create_event(func,)
                else:
                    parent.create_event(func, **kwargs)
            else:
                if kwargs is None:
                    parent.create_event(func, *args)
                else:
                    parent.create_event(func, *args, **kwargs)
    
    
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
                    raise TypeError(
                        f'`{parent!r}` does not support elements of type {type_!r}; got {iterable!r}.'
                    )
                
                collected = []
                for element in iterable:
                    try:
                        parent.delete_event(element, None)
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
            args = element.args
            kwargs = element.kwargs
            try:
                
                if args is None:
                    if kwargs is None:
                        parent.delete_event(func)
                    else:
                        parent.delete_event(func, **kwargs)
                else:
                    if kwargs is None:
                        parent.delete_event(func, *args)
                    else:
                        parent.delete_event(func, *args, **kwargs)
            
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
        | event_handlers                | `object`                          |
        +-------------------------------+-----------------------------------+
    
    _from_class_constructor : `callable`, `None`
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
        | commands                      | `list` of `object`                |
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
            | event_handlers                | `object`                          |
            +-------------------------------+-----------------------------------+
        
        from_class_constructor : `None`, `callable`
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
            | commands                      | `list` of `object`                |
            +-------------------------------+-----------------------------------+
        """
        self.parent = parent
        self._getter = getter
        self._from_class_constructor = from_class_constructor
    
    
    def __call__(self, func=..., *args, **kwargs):
        """
        Adds the given `func` to all of the represented client's respective event handler managers.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the respective event handler.
        *args : Positional parameter
            Additionally passed positional parameters to be passed with the given `func` to the event handler.
        **kwargs : Keyword parameters
            Additionally passed keyword parameters to be passed with the given `func` to the event handler.
        
        Returns
        -------
        func : ``Routed``
           The added functions.
        """
        if func is ...:
            return partial_func(self, *args, **kwargs)
        
        handlers = self._getter(self)
        if not handlers:
            return
        
        count = len(handlers)
        
        routed_args = route_args(args, count)
        routed_kwargs = route_kwargs(kwargs, count)
        routed_func = maybe_route_func(func, count)
        routed = []
        
        for handler, func_, args, kwargs in zip(handlers, routed_func, routed_args, routed_kwargs):
            func = handler.create_event(func_, *args, **kwargs)
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
            object exception raised by any of the event handler.
        """
        from_class_constructor = self._from_class_constructor
        if from_class_constructor is None:
            raise TypeError(
                f'`.from_class` is not supported by {self.parent!r}.'
            )
        
        handlers = self._getter(self)
        count = len(handlers)
        if not count:
            return
        
        routed_maybe = from_class_constructor(klass)
        if isinstance(routed_maybe, Router):
            if len(routed_maybe) != count:
                raise ValueError(
                    f'The given class is routed to `{len(routed_maybe)}`, meanwhile expected to be routed '
                    f'to `{count}` times, got {klass!r}.'
                )
            
            routed = routed_maybe
        
        else:
            copy_method = getattr(type(routed_maybe), 'copy', None)
            if copy_method is None:
                routed = [routed_maybe for _ in range(count)]
            else:
                routed = [copy_method(routed_maybe) for _ in range(count)]
            
        for handler, event in zip(handlers, routed):
            handler.create_event(event)
        
        return routed
    
    
    def remove(self, func, *args, **kwargs):
        """
        Removes the given `func` from the represented event handler managers.
        
        Parameters
        ----------
        func : ``Router``, `callable`
            The event to be removed to the respective event handlers.
        *args : `None`, `str`
            Additional positional parameters.
        **kwargs : Keyword parameters
            Additional keyword parameters.
        """
        handlers = self._getter(self)
        
        count = len(handlers)
        if not count:
            return
        
        if isinstance(func, Router):
            if len(func) != count:
                raise ValueError(
                    f'The given `func` is routed `{len(func)}` times, meanwhile expected to be routed '
                    f'to `{count}` times, got {func!r}.'
                )
            
            for func, handler in zip(func, handlers):
                handler.delete_event(func, *args, **kwargs)
        
        else:
            for handler in handlers:
                handler.delete_event(func, *args, **kwargs)
    
    
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
                    raise TypeError(
                        f'`{parent!r}` does not support elements of type {type_!r}; got {iterable!r}.'
                    )
                
                for element in iterable:
                    if isinstance(element, Router):
                        if len(element) != count:
                            raise ValueError(
                                f'The given `func` is routed `{len(element)}` times, meanwhile expected to be routed '
                                f'to `{count}` times, got {element!r}.'
                            )
                        
                        for func, handler in zip(element, handlers):
                            handler.create_event(func, None)
                    
                    else:
                        for handler in handlers:
                            handler.create_event(element, None)
                return
        else:
            iterable = _convert_unsafe_event_iterable(iterable)
        
        for element in iterable:
            func = element.func
            args = element.args
            kwargs = element.kwargs
            
            routed_args = route_args(args, count)
            routed_func = maybe_route_func(func, count)
            routed_kwargs = route_kwargs(kwargs, count)
            
            for handler, func_, args, kwargs in zip(handlers, routed_func, routed_args, routed_kwargs):
                handler.create_event(func_, *args, **kwargs)
    
    
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
                    raise TypeError(
                        f'`{parent!r}` does not support elements of type {type_!r}; got {iterable!r}.'
                    )
                
                collected = []
                for element in iterable:
                    if isinstance(element, Router):
                        if len(element) != count:
                            collected.append(
                                f'The given `func` is routed `{len(element)}` times, meanwhile expected '
                                f'to be routed to `{count}` times, got {element!r}.'
                            )
                            continue
                        
                        for func, handler in zip(element, handlers):
                            try:
                                handler.delete_event(func, None)
                            except ValueError as err:
                                collected.append(err.args[0])
                    else:
                        for handler in handlers:
                            try:
                                handler.delete_event(element, None)
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
            args = element.args
            kwargs = element.kwargs
            
            routed_func = maybe_route_func(func, count)
            
            if kwargs is None:
                for handler, func_ in zip(handlers, routed_func):
                    try:
                        handler.delete_event(func_)
                    except ValueError as err:
                        collected.append(err.args[0])
                
            else:
                routed_kwargs = route_kwargs(kwargs, count)
                routed_args = route_args(args, count)
                
                for handler, func_, args, kwargs in zip(handlers, routed_func, routed_args, routed_kwargs):
                    try:
                        handler.delete_event(func_, *args, **kwargs)
                    except ValueError as err:
                        collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected)) from None
    
    def __repr__(self):
        return (
            f'<{self.__class__.__name__} '
            f'parent = {self.parent!r}, '
            f'getter = {self._getter!r}, '
            f'from_class_constructor={self._from_class_constructor!r}'
            f'>'
        )

class EventListElement:
    """
    Represents an element of an ``eventlist``.
    
    Attributes
    ----------
    func : `callable`
        The event of the event-list element.
    args : `None`, `tuple` of `object`
        Additional positional parameters for `func`.
    kwargs : `None`, `dict` of (`str`, `object`) items
        Additional key word parameters for `func`.
    """
    __slots__ = ('func', 'args', 'kwargs', )
    
    def __init__(self, func, args, kwargs):
        """
        Creates a ``EventListElement` from the given parameters.
        
        Parameters
        ----------
        func : `callable`
            The event of the eventlist element.
        args : `None`, `str`
            Additional positional parameters for `func`.
        kwargs : `None`, `dict` of (`str`, `object`) items
            Additional key word parameters for `func`.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def __repr__(self):
        """Returns the representation of the eventlist element."""
        return f'{self.__class__.__name__}({self.func!r}, args={self.args!r}, kwargs={self.kwargs!r})'
    
    def __len__(self):
        """Additional information for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """
        Unpacks the eventlist element.
        
        This method is a generator.
        """
        yield self.func
        yield self.args
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


def route_value(to_route_value, count, default = None):
    """
    Routes only a single `name` - `value` pair.
    
    Parameters
    ----------
    to_route_value : `object`
        The respective value to route
    count : `int`
        The expected amount of copies to generate.
    default : `None`, `object` = `None`, Optional
        Optional default variable to use. Defaults to `None`.
    
    Returns
    -------
    result : `list` of `object`
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


def route_parameter(parameter, count):
    """
    Routes a parameter to `count` amount of copies.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    parameter : `object`
        The parameter to route.
    count : `int`
        The expected amount of copies to generate.
    
    Yields
    ------
    result : `object`
    
    Raises
    ------
    ValueError
        A value is a `tuple`, but it's length is different from `count`.
    """
    if isinstance(parameter, tuple):
        if len(parameter) != count:
            raise ValueError(
                f'The represented router has `{count}` applicable clients, meanwhile received only '
                f'`{len(parameter)}` routed values, got: {parameter!r}.'
            )
        
        last = None
        for value in parameter:
            if value is None:
                last = None
            elif value is ...:
                value = last
            else:
                last = value
            
            yield value
            continue
    else:
        for _ in range(count):
            yield parameter
    
    
def route_kwargs(kwargs, count):
    """
    Routes the given `kwargs` to the given `count` amount of copies.
    
    If a value of a keyword is given as a `tuple`, then it will be routed by element for each applicable
    client.
    
    Parameters
    ----------
    kwargs : `dict` of (`str`, `object`) items
        Keyword parameter to route.
    count : `int`
        The expected amount of copies to generate.
    
    Returns
    -------
    result : `tuple` of `dict` of (`str`, `object) items
    
    Raises
    ------
    ValueError
        A value is a `tuple`, but it's length is different from `count`.
    """
    result = tuple({} for _ in range(count))
    
    if (kwargs is not None):
        for parameter_name, parameter_value in kwargs.items():
            for route_to, parameter in zip(result, route_parameter(parameter_value, count)):
                route_to[parameter_name] = parameter
    
    return result


def route_args(args, count):
    """
    Routes the given `args` to the given `count` amount of copies.
    
    Parameters
    ----------
    args : `tuple` of `object`
        Positional parameter to route.
    count : `int`
        The expected amount of copies to generate.
    
    Returns
    -------
    result : `tuple` of `tuple` of `object`
    
    Raises
    ------
    ValueError
        A value is a `tuple`, but it's length is different from `count`.
    """
    if (args is None):
        result = tuple(tuple() for _ in range(count))
    else:
        result = tuple([] for _ in range(count))
        
        for parameter_value in args:
            for route_to, parameter in zip(result, route_parameter(parameter_value, count)):
                route_to.append(parameter)
    
        result = tuple(tuple(routed_to) for routed_to in result)
    
    return result


def route_name(name, count):
    """
    Routes the given `name` to the given `count` amount of copies.
    
    If `name` is given as `tuple`, then each element of it will be returned for each applicable client.
    
    Parameters
    ----------
    name : `None`, `Ellipsis`, `str`, `tuple` of (`None`, `Ellipsis`, `str`)
        The name to use instead of `func`'s real one.
    count : `int`
        The expected amount of names.
    
    Returns
    -------
    result : `list` of (`None`, `str`)
    
    Raises
    ------
    TypeError
        - If `name` was not given as `None`, `Ellipsis`, `str`, neither as `tuple` of (`None`, `Ellipsis`, `str`).
    ValueError
        If `name` was given as `tuple` but it's length is different from the expected one.
    """
    result = []
    
    if isinstance(name, tuple):
        for index, name_value in enumerate(name):
            if (name_value is not None) and (name_value is not ...) and (not isinstance(name_value, str)):
                raise TypeError(
                    f'`name` was given as a `tuple`, but it\'s {index}th element is not `None`, '
                    f'`Ellipsis`, `str`, got, {name_value.__class__.__name__}: {name_value!r}.'
                )
        
        if len(name) != count:
            raise ValueError(
                f'`name` was given as `tuple`, but it\'s length ({len(name)!r}) not matches the expected '
                f'(`{count}`) one, got {name!r}.'
            )
        
        last = None
        for name_value in name:
            if name is None:
                name_value = None
                last = None
            elif name_value is ...:
                name_value = last
            else:
                last = name_value
            
            result.append(name_value)
    else:
        if name is None:
            name_value = None
        elif isinstance(name, str):
            name_value = str(name)
        else:
            raise TypeError(
                '`name` can be given `None`, `tuple` of (`None, `Ellipsis`, `str`), got '
                f'{name.__class__.__name__}; {name!r}.'
            )
        
        for _ in range(count):
            result.append(name_value)
    
    return result


def maybe_route_func(func, count):
    """
    Routes the given `func` `count` times if applicable.
    
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
    kwargs : `None`, `dict` of (`str`, `object`) items
        Keyword parameters used for each element when extending the client's events with the event-list.
    type : `None`, `type`
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
    
    __slots__ = ('kwargs', 'type')
    
    def __new__(cls, iterable=None, type_=None, **kwargs):
        """
        Creates a new eventlist from the the given parameters.
        
        Parameters
        ----------
        iterable : `None`, `iterable` = `None`, Optional
            An iterable of events to extend the eventlist with.
        type_ : `None`, `type` = `None`, Optional
            A type to validate each added element to the eventlist.
        **kwargs : Keyword parameters
            Additional keyword parameters to be used when adding each element.
        
        Raises
        ------
        TypeError
            If `type_` was passed as not as `type`, or if it has no `from_args_kwargs` method.
        ValueError
            - If `iterable` was passed as ``eventlist`` and it's `.type` attribute is different.
            - If `iterable` was not passed as type ``eventlist`` and any of it's element's format is incorrect.
        """
        if (type_ is not None) and (not isinstance(type_, type)):
            raise TypeError(
                f'`type_` can be `None`, `type`, got {type_!r}.'
            )
        
        if not kwargs:
            kwargs = None
        
        self = list.__new__(cls)
        self.type = type_
        self.kwargs = kwargs
        
        if (iterable is not None):
            self.extend(iterable)
        
        return self
    
    if NEEDS_DUMMY_INIT:
        def __init__(self, *args, **kwargs):
            pass
    else:
        __init__ = object.__init__
    
    
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
            The created instance from the event-list's `.type`.
        
        Raises
        ------
        TypeError
            If the eventlist has no `.type` set, or if it's `.type` is not supporting this method.
        """
        type_ = self.type
        if type_ is None:
            raise TypeError(
                '`.from_class` method cannot be used on `eventlist` without type.'
            )
        
        from_class = getattr(type_, 'from_class', None)
        if from_class is None:
            raise TypeError(
                f'`.from_class`. is not supported by the `eventlist`\'s type: {type_!r}.'
            )
        
        element = from_class(klass)
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
                raise ValueError(
                    f'Extending {self.__class__.__name__} with an other object of the same type, is not allowed if '
                    f'their `.type` is different. Own: {self.type!r}; other: {iterable.type!r}.'
                )
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
                raise ValueError(
                    f'Extending {self.__class__.__name__} with an other object of the same type, is not allowed if '
                    f'their `.type` is different. Own: {self.type!r}; other: {iterable.type!r}.'
                )
        
        collected = []
        for element in iterable:
            try:
                self.remove(*element)
            except ValueError as err:
                collected.append(err.args[0])
        
        if collected:
            raise ValueError('\n'.join(collected))
    
    
    def __call__(self, func = ..., *args, **kwargs):
        """
        Adds the given `func` to the ``eventlist`` with the other given keyword parameters. If `func` is not passed,
        then returns a ``._wrapper` to allow using the ``eventlist`` as a decorator with still passing keyword
        parameters.
        
        Parameters
        ----------
        func : `callable`, Optional
            The event to be added to the eventlist.
        *args : Positional parameter
            Additionally passed positional parameters to be used when the passed `func` is used up.
        **kwargs : Keyword parameters
            Additionally passed keyword parameters to be used when the passed `func` is used up.
        
        Returns
        -------
        func : `callable`
            - If `func` was passed and the eventlist has no `.type` then returns the passed `func`.
            - If `func` was passed and the eventlist has `.type` set, then returns an instance of that.
            - If `func` was not passed, then returns a ``._wrapper``.
        """
        own_kwargs = self.kwargs
        if (own_kwargs is not None) and own_kwargs:
            for name_, value_ in own_kwargs.items():
                kwargs.setdefault(name_, value_)
        
        if func is ...:
            return partial_func(self, *args, **kwargs)
        
        type_ = self.type
        if type_ is None:
            element = EventListElement(func, *args, **kwargs)
        else:
            element = func = type_(func, *args, **kwargs)
        
        list.append(self, element)
        return func
    
    
    def remove(self, func):
        """
        Removes an element of the eventlist.
        
        Parameters
        ----------
        func : `callable`
            The function to remove.

        Raises
        ------
        ValueError
            If the passed `func` - `name` combination was not found.
        """
        # we might overwrite __iter__ later
        for element in list.__iter__(self):
            if compare_converted(element.func, func):
                return
        
        raise ValueError(
            f'Could not match any element by func={func!r}.'
        )
    
    
    def __repr__(self):
        """Returns the representation of the eventlist."""
        repr_parts = [
            self.__class__.__name__,
            '([',
        ]
        
        limit = list.__len__(self)
        if limit != 0:
            index = 0
            
            while True:
                element=list.__getitem__(self, index)
                repr_parts.append(repr(element))
                index +=1
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']')
        
        type_ = self.type
        if (type_ is not None):
            repr_parts.append(', type=')
            repr_parts.append(repr(type_))
        
        kwargs = self.kwargs
        if (kwargs is not None):
            repr_parts.append(', kwargs=')
            repr_parts.append(repr(kwargs))
        
        repr_parts.append(')')
        return ''.join(repr_parts)
    
    
    def add_kwargs(self, **kwargs):
        """
        Adds keyword parameters to the ``eventlist`'s.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            KeyWord parameters to extend the ``eventlist``'s with.
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
        Removes keyword parameters of the ``eventlist`` by their name.
        
        Parameters
        ----------
        *names : Positional parameters
            Keyword parameter's name added to the ``eventlist``.
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
class EventHandlerBase(RichAttributeErrorBaseType):
    """
    Base class for event handlers.
    """
    __slots__ = ()
    
    # subclasses should overwrite it
    async def __call__(self, *args):
        """
        The method what will be called by the respective parser. The first received parameter is always a ``Client``
        meanwhile the rest depends on the dispatch event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        *args : Additional positional parameters
        """
        pass
    
    # subclasses should overwrite it
    def create_event(self, func, *args, **kwargs):
        """
        Adds the specified event to the event handler. Subclasses might add additional keyword parameters as well.
        
        Parameters
        ----------
        func : `callable`
            The callable to be added.
        *args : Positional parameters
            Positional parameters to pass to the created event.
        **kwargs : Keyword parameters
            Keyword parameters to pass to the created event.
        
        Returns
        -------
        func : `callable`
            The created event.
        """
        pass

    # subclasses should overwrite it
    def delete_event(self, func):
        """
        Removes the specified event from the event handler. Subclasses might add additional keyword parameters as well.
        
        Parameters
        ----------
        func : `callable`
            The callable to be removed.
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
    
    The supported events by default are the following:
    - `message_create`
    - `message_update`
    - `message_delete`
    - `channel_create`
    - `channel_update`
    - `channel_delete`
    - `role_create`
    - `role_update`
    - `role_delete`
    - `guild_delete`
    - `guild_update`
    - `emoji_update`
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
        
        Auto-adds a `.waitfors` attribute to them and also sets it as a `WeakKeyDictionary`, so you would not
        need to bother with that.
        
        Parameters
        ----------
        *args : Additional positional parameters
        **kwargs : Additional keyword parameters
        
        Returns
        -------
        object_ : `object`
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
    
    async def _call_message_update(self, client, message, old_attributes):
        args = (client, message, old_attributes)
        channel = message.channel
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['message_edit'] = _call_message_update
    _call_waitfors['message_update'] = _call_message_update
    del _call_message_update
    
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
    
    async def _call_channel_update(self, client, channel, old_attributes):
        args = (client, channel, old_attributes)
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if guild is None:
            return
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['channel_edit'] = _call_channel_update
    _call_waitfors['channel_update'] = _call_channel_update
    del _call_channel_update
    
    async def _call_channel_delete(self, client, channel):
        args = (client, channel)
        self._run_waitfors_for(channel, args)
        guild = channel.guild
        if (guild is not None):
            self._run_waitfors_for(guild, args)
    
    _call_waitfors['channel_delete'] = _call_channel_delete
    del _call_channel_delete
    
    async def _call_role_create(self, client, role):
        args = (client, role)
        
        guild = role.guild
        if (guild is not None):
            self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_create'] = _call_role_create
    del _call_role_create
    
    async def _call_role_update(self, client, role, old_attributes):
        args = (client, role, old_attributes)
        self._run_waitfors_for(role, args)
        
        guild = role.guild
        if (guild is not None):
            self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_edit'] = _call_role_update
    _call_waitfors['role_update'] = _call_role_update
    del _call_role_update

    async def _call_role_delete(self, client, role):
        args = (client, role)
        self._run_waitfors_for(role, args)
        
        guild = role.guild
        if (guild is not None):
            self._run_waitfors_for(guild, args)
    
    _call_waitfors['role_delete'] = _call_role_delete
    del _call_role_delete
    
    async def _call_guild_delete(self, client, guild, profile):
        args = (client, guild, profile)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['guild_delete'] = _call_guild_delete
    del _call_guild_delete
    
    async def _call_guild_update(self, client, guild, old_attributes):
        args = (client, guild, old_attributes)
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['guild_edit'] = _call_guild_update
    _call_waitfors['guild_update'] = _call_guild_update
    del _call_guild_update
    
    async def _call_emoji_create(self, client, emoji):
        args = (client, emoji)
        guild = emoji.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_create'] = _call_emoji_create
    del _call_emoji_create
    
    async def _call_emoji_update(self, client, emoji, old_attributes):
        args = (client, emoji, old_attributes)
        self._run_waitfors_for(emoji, args)
        guild = emoji.guild
        self._run_waitfors_for(guild, args)
    
    _call_waitfors['emoji_edit'] = _call_emoji_update
    _call_waitfors['emoji_update'] = _call_emoji_update
    del _call_emoji_update

    async def _call_emoji_delete(self, client, emoji):
        args = (client, emoji)
        self._run_waitfors_for(emoji, args)
        
        guild = emoji.guild
        if (guild is not None):
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


class EventWaitforBase(EventHandlerBase, metaclass = EventWaitforMeta):
    """
    Base class for event handlers, which implement waiting for a specified action to occur.
    
    Attributes
    ----------
    waitfors : `WeakValueDictionary` of (``DiscordEntity``, `async-callable`) items
        An auto-added container to store `entity` - `async-callable` pairs.
    
    Class Attributes
    ----------------
    __event_name__ : `None`, `str` = `None`
        Predefined name to what the event handler will be added.
    call_waitfors : `None`, `async callable` = `None`
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
        target : ``DiscordEntity``
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
        target : ``DiscordEntity``
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
    
    def get_waiter(self, target, waiter, by_type=False, is_method=False):
        """
        Looks up whether any of the given `target` - `waiter` relation is stored inside of `.waiters` and if there is
        any, then returns the first find. If non, then returns `None`.
        
        Parameters
        ----------
        target : ``DiscordEntity``
            The target entity.
        waiter : `object`
            The waiter. `by_type` and `is_method` overwrite the behaviour of checking it.
        by_type : `bool` = `False`, Optional
            Whether `waiter` was given as the type of the real waiter. Defaults to `False`.
        is_method : `bool` = `False`, Optional
            Whether the real waiter is a method-like, and you want to check it's "self". Applied before `by_type` and
            defaults to `False`.
        
        Returns
        -------
        waiter : `object`
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
        target : ``DiscordEntity``
            The target entity.
        waiter : `object`
            The waiter. `by_type` and `is_method` overwrite the behaviour of checking it.
        by_type : `bool` = `False`, Optional
            Whether `waiter` was given as the type of the real waiter. Defaults to `False`.
        is_method : `bool` = `False`, Optional
            Whether the real waiter is a method-like, and you want to check it's "self". Applied before `by_type` and
            defaults to `False`.
        
        Returns
        -------
        waiters : `list` of `object`
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
        target : ``DiscordEntity``
            The target entity.
        args : `tuple` of `object`
            Parameters to ensure the waitfors with.
        """
        try:
            event = self.waitfors[target]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                for event in event:
                    Task(KOKORO, event(*args))
            else:
                Task(KOKORO, event(*args))


def EventWaitforMeta__new__(cls, class_name, class_parents, class_attributes):
    """
    Subclasses ``EventWaitforBase``.
    
    Parameters
    ----------
    class_name : `str`
        The created class's name.
    class_parents : `tuple` of `type`
        The superclasses of the creates type.
    class_attributes : `dict` of (`str`, `object`) items
        The class attributes of the created type.
    
    Returns
    -------
    type : ``EventWaitforMeta``
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
        raise TypeError(
            f'`{cls.__name__} should be only the metaclass of `{EventWaitforBase.__name__}`.'
        )
    
    event_name = class_attributes.get('__event_name__', None)
    if event_name is None:
        event_name = class_name
    
    if event_name not in EVENT_HANDLER_NAME_TO_PARSER_NAMES:
        raise TypeError(
            f'`{class_name}.__event_name__` is not set, or is not set correctly.'
        )
    
    if (class_attributes.get('call_waitfors', None) is None):
        try:
            call_waitfors = cls._call_waitfors[event_name]
        except KeyError:
            raise TypeError(
                f'Event: `{event_name!r}` has no auto `call_waitfor` added. Please define one.'
            )
        
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

class ChunkWaiter(RichAttributeErrorBaseType):
    """
    Guild user chunk waiter.
    
    Attributes
    ----------
    waiters : `dict` of (`int`, ``SingleUserChunker`` | ``MassUserChunker``) items.
        User chunk waiters.
    """
    __slots__ = ('waiters',)
    
    __event_name__ = 'guild_user_chunk'
    
    def __init__(self):
        self.waiters = {}
    
    
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



class WaitForHandler:
    """
    O(n) event waiter. Added as an event handler by ``Client.wait_for``.
    
    Attributes
    ----------
    waiters : `dict` of (``Future``, `callable`) items
        A dictionary which contains the waiter futures and the respective checks.
    """
    __slots__ = ('waiters', )
    
    def __init__(self):
        """
        Creates a new ``WaitForHandler``.
        """
        self.waiters = {}
    
    async def __call__(self, client, *args):
        """
        Runs the checks of the respective event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective events.
        args : `tuple` of `object`
            Other received parameters by the event.
        """
        for future, check in self.waiters.items():
            try:
                result = check(*args)
            except GeneratorExit as err:
                future.set_exception_if_pending(err)
                raise
            
            except BaseException as err:
                future.set_exception_if_pending(err)
            
            else:
                if isinstance(result, bool):
                    if result:
                        if len(args) == 1:
                            args = args[0]
                    else:
                        return
                else:
                    args = (*args, result)
                
                future.set_result_if_pending(args)


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
        iterable : `None`, `iterable` = `None`, Optional
        """
        if (iterable is not None):
            list.extend(self, iterable)
    
    async def __call__(self, *args):
        """
        Ensures the contained async callables on the client's loop.
        
        This method is a coroutine.
        
        Parameters
        ----------
        *args : Additional position parameters
            Parameters to call with the contained async callables.
        """
        for coroutine_function in list.__iter__(self):
            Task(KOKORO, coroutine_function(*args))
    
    
    def __repr__(self):
        """Returns the async-list's representation."""
        repr_parts = [
            self.__class__.__name__,
            '(['
        ]
        
        
        limit = list.__len__(self)
        if limit:
            index = 0
            while True:
                element = list.__getitem__(self, index)
                repr_parts.append(repr(element))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append('])')
        
        return ''.join(repr_parts)
    
    
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
        
        for coroutine_function in list.__iter__(self):
            attribute = getattr(coroutine_function, name, ...)
            if attribute is ...:
                continue
            
            return attribute
        
        raise AttributeError(f'`{self.__class__.__name__}` object has no attribute `{name}`.')
    
    append = RemovedDescriptor()
    clear = RemovedDescriptor()
    copy = RemovedDescriptor()
    count = RemovedDescriptor()
    extend = RemovedDescriptor()
    index = RemovedDescriptor()
    insert = RemovedDescriptor()
    pop = RemovedDescriptor()
    remove = RemovedDescriptor()
    reverse = RemovedDescriptor()
    sort = RemovedDescriptor()


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
    except GeneratorExit:
        raise
    
    except BaseException as err:
        await client.events.error(client, repr(task), err)
    
    finally:
        task = None # clear references


async def ensure_shutdown_event_handlers(client):
    """
    Ensures the client's shutdown event handlers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    """
    # call client.events.shutdown if has any.
    return await ensure_event_handlers(client, client.events.shutdown)


async def ensure_voice_client_shutdown_event_handlers(client):
    """
    Ensures the client's voice client shutdown event handlers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    """
    return await ensure_event_handlers(client, client.events.voice_client_shutdown)


async def ensure_event_handlers(client, event_handlers):
    """
    Ensures the given event handlers. Used by ``ensure_shutdown_event_handlers`` and
    ``ensure_voice_client_shutdown_event_handlers``.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    event_handlers : `async-callable`
        The event handlers to ensure.
    """
    if (event_handlers is not DEFAULT_EVENT_HANDLER):
        # We use `TaskGroup.wait_all` even for 1 task, since we do not want any raised exceptions to be forwarded.
        tasks = []
        
        if type(event_handlers) is asynclist:
            for event_handler in list.__iter__(event_handlers):
                tasks.append(Task(KOKORO, _with_error(client, event_handler(client))))
        
        else:
            tasks.append(Task(KOKORO, _with_error(client, event_handlers(client))))
        
        event_handlers = None # clear references
        
        future = TaskGroup(KOKORO, tasks).wait_all()
        tasks = None # clear references
        await future


def call_unknown_dispatch_event_event_handler(client, name, data):
    """
    Calls `client.events.unknown_dispatch_event`.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    name : `str`
        The name of an event.
    data : `object`
        The received data.
    """
    event_handler = client.events.unknown_dispatch_event
    if (event_handler is not DEFAULT_EVENT_HANDLER):
        Task(KOKORO, event_handler(client, name, data))


IGNORED_EVENT_HANDLER_TYPES = frozenset((
    WaitForHandler,
    ChunkWaiter,
))

def should_ignore_event_handler(event_handler):
    """
    Returns whether the given `event_handler` should be ignored from snapshotting.
    
    Parameters
    ----------
    event_handler : `async-callable`
        The respective event handler.
    
    Returns
    -------
    should_ignore : `bool`
    """
    if event_handler is DEFAULT_EVENT_HANDLER:
        return True
    
    if type(event_handler) in IGNORED_EVENT_HANDLER_TYPES:
        return True
    
    return False


def _iterate_event_handler(event_handler):
    """
    Iterates over the given event handler, yielding each valuable handler.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    event_handler : `object`
        Event handler to iterate trough.
    
    Yields
    ------
    event_handler : `sync-callable`
        Valuable event handlers.
    """
    if isinstance(event_handler, asynclist):
        for iterated_event_handler in list.__iter__(event_handler):
            if not should_ignore_event_handler(iterated_event_handler):
                yield iterated_event_handler
    else:
        if not should_ignore_event_handler(event_handler):
            yield event_handler
