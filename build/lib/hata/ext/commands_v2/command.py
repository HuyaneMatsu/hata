__all__ = ('Command', )

from ...backend.export import export
from ...backend.utils import WeakReferer
from ...discord.events.handling_helpers import route_value, check_name, Router, route_name, _EventHandlerManager, \
    create_event_from_class
from ...discord.preconverters import preconvert_bool

from .wrappers import CommandWrapper, CommandCheckWrapper
from .category import Category
from .utils import  raw_name_to_display, normalize_description
from .command_helpers import test_error_handler, validate_checks, validate_error_handlers
from .content_parser import CommandContentParser

COMMAND_PARAMETER_NAMES = ('command', 'name', 'description', 'aliases', 'category', 'checks', 'error_handlers',
    'separator', 'assigner', 'hidden', 'hidden_if_checks_fail')

COMMAND_NAME_NAME = 'name'
COMMAND_COMMAND_NAME = 'command'

def _check_maybe_route(variable_name, variable_value, route_to, validator):
    """
    Helper class of ``Command`` parameter routing.
    
    Parameters
    ----------
    variable_name : `str`
        The name of the respective variable
    variable_value : `str`
        The respective value to route maybe.
    route_to : `int`
        The value how much times the routing should happen. by default should be given as `0` if no routing was
        done yet.
    validator : `callable` or `None`
        A callable, what validates the given `variable_value`'s value and converts it as well if applicable.
    
    Returns
    -------
    processed_value : `str`
        Processed value returned by the `validator`. If routing is happening, then a `tuple` of those values is
        returned.
    route_to : `int`
        The amount of values to route to.
    
    Raises
    ------
    ValueError
        Value is routed but to a bad count amount.
    BaseException
        Any exception raised by `validator`.
    """
    if (variable_value is not None) and isinstance(variable_value, tuple):
        route_count = len(variable_value)
        if route_count == 0:
            processed_value = None
        elif route_count == 1:
            variable_value = variable_value[0]
            if variable_value is ...:
                variable_value = None
            
            if validator is None:
                processed_value = variable_value
            else:
                processed_value = validator(variable_value)
        else:
            if route_to == 0:
                route_to = route_count
            elif route_to == route_count:
                pass
            else:
                raise ValueError(f'`{variable_name}` is routed to `{route_count}`, meanwhile something else is '
                    f'already routed to `{route_to}`.')
            
            if validator is None:
                processed_value = variable_value
            else:
                processed_values = []
                for value in variable_value:
                    if (value is not ...):
                        value = validator(value)
                    
                    processed_values.append(value)
                
                processed_value = tuple(processed_values)
    
    else:
        if validator is None:
            processed_value = variable_value
        else:
            processed_value = validator(variable_value)
    
    return processed_value, route_to


def _validate_hidden(hidden):
    """
    Validates the given `is_global` value.
    
    Parameters
    ----------
    hidden : `None` or `bool`
        The `hidden` value to validate.
    
    Returns
    -------
    hidden : `bool`
        The validated `hidden` value.
    
    Raises
    ------
    TypeError
        If `hidden` was not given as `None` nor as `bool` instance.
    """
    if hidden is None:
        hidden = False
    else:
        hidden = preconvert_bool(hidden, 'hidden')
    
    return hidden


def _validate_hidden_if_checks_fail(hidden_if_checks_fail):
    """
    Validates the given `hidden_if_checks_fail` value.
    
    Parameters
    ----------
    hidden_if_checks_fail : `None` or `bool`
        The `hidden_if_checks_fail` value to validate.
    
    Returns
    -------
    hidden_if_checks_fail : `bool`
        The validated `hidden` value.
    
    Raises
    ------
    TypeError
        If `hidden_if_checks_fail` was not given as `None` nor as `bool` instance.
    """
    if hidden_if_checks_fail is None:
        hidden_if_checks_fail = True
    else:
        hidden_if_checks_fail = preconvert_bool(hidden_if_checks_fail, 'hidden_if_checks_fail')
    
    return hidden_if_checks_fail


def _validate_name(name):
    """
    Validates the given name.
    
    Parameters
    ----------
    name : `None` or `str`
        A command's respective name.
    
    Returns
    -------
    name : `None` or `str`
        The validated name.
    
    Raises
    ------
    TypeError
        If `name` is not given as `str` instance.
    """
    if name is not None:
        name_type = name.__class__
        if name_type is str:
            pass
        elif issubclass(name_type, str):
            name = str(name)
        else:
            raise TypeError(f'`name` can be only given as `None` or as `str` instance, got {name_type.__name__}; '
                f'{name!r}.')
    
    return name


def _validate_aliases(aliases):
    """
    Validates the given aliases.
    
    Parameters
    ----------
    aliases : `None`, `str` or `list` of `str`
        Command aliases.
    
    Returns
    -------
    aliases : `None` or `set` of `str`
        The validated aliases.
    
    Raises
    ------
    TypeError
        `aliases` was not given as `None`, `str`, neither as `list` of `str` instances.
    ValueError
        `aliases` contains an empty string.
    """
    if (aliases is not None):
        if isinstance(aliases, list):
            for alias in aliases:
                if not isinstance(alias, str):
                    raise TypeError(f'A non `str` instance alias is given: {alias!r}, got {aliases!r}.')
                
                if not alias:
                    raise ValueError(f'An alias cannot be empty string, got {aliases!r}.')
            
            aliases_processed = set()
            for alias in aliases:
                alias = raw_name_to_display(alias)
                aliases_processed.add(alias)
            
            if aliases_processed:
                aliases = aliases_processed
            else:
                aliases = None
        
        elif isinstance(aliases, str):
            if not aliases:
                raise ValueError(f'An alias cannot be empty string, got {aliases!r}.')
            
            aliases = raw_name_to_display(aliases)
            aliases = {aliases}
        else:
            raise TypeError('Aliases can be given as `str`, or `list` of `str` instances, got '
                f'{aliases.__class__.__name__}; {aliases!r}')
    
    return aliases


def _validate_category(category):
    """
    Validates the given category.
    
    Parameters
    ----------
    category : `None`, `str`  instance or ``Category``
        The category to validate.
    
    Returns
    -------
    category : `str` or ``Category``
        The validated category.
    
    Raises
    ------
    TypeError
        Category is not given either as `None`, `str` instance, or ``Category``.
    """
    if (category is not None):
        category_type = category.__class__
        if category_type is Category:
            pass
        elif category_type is str:
            pass
        elif issubclass(category_type, str):
            category = str(category)
        else:
            raise TypeError(f'`category` should be `None`, type `str` or `{Category.__name__}`, got '
                f'{category_type.__name__}.')
    
    return category


def _generate_description_from(command, description):
    """
    Generates description from the command and it's maybe given description.
    
    Parameters
    ----------
    command : `str`
        The command's function.
    description : `Any`
        The command's description.
    
    Returns
    -------
    description : `str`
        The generated description.
    """
    if description is None:
        description = getattr(command, '__doc__', None)
    
    if (description is not None) and isinstance(description, str):
        description = normalize_description(description)
    
    return description


def _generate_category_hint_from(category):
    """
    Generates category hint from the given category.
    
    Parameters
    ----------
    category : `None`, `str` or ``Category``
        The respective category.
    
    Returns
    -------
    category_hint : `None` or `str`
        The category's string representation if applicable.
    
    Raises
    ------
    TypError
        Category is not given as `None`, `str`, neither as ``Category`` instance.
    """
    if category is None:
        category_hint = None
    else:
        category_type = category.__class__
        if category_type is Category:
            category_hint = category.name
        elif category_type is str:
            category_hint = category
        elif issubclass(category_type, str):
            category_hint = str(category)
        else:
            raise TypeError(f'`category` should be `None`, type `str` or `{Category.__name__}`, got '
                f'{category_type.__name__}.')
    
    return category_hint


def _fetch_check_from_wrappers(wrappers):
    """
    Gets the check wrappers from the given ones.
    
    Parameters
    ----------
    wrappers : `None` or `list` of ``CommandWrapper``
        Command wrappers.
    
    Returns
    -------
    checks : `None` or `list` of ``CheckBase``
        The fetched down checks.
    """
    checks = None
    if (wrappers is not None):
        for wrapper in wrappers:
            if isinstance(wrapper, CommandCheckWrapper):
                if checks is None:
                    checks = []
                
                checks.append(wrapper._check)
    
    return checks


def _iter_merge_checks(checks_1, checks_2):
    """
    Iterates the given checks.
    
    This function is a generator.
    
    Parameters
    ----------
    checks_1 : `None` or `list` of ``CheckBase``
        Checks to merge.
    checks_2: `None` or`list` of ``CheckBase``
        Checks to merge.
    
    Yields
    ------
    check : ``CheckBase``
    """
    if (checks_1 is not None):
        yield from checks_1
    
    if (checks_2 is not None):
        yield from checks_2


def _merge_checks(checks_1, checks_2):
    """
    Merges the two checks.
    
    Parameters
    ----------
    checks_1 : `None` or `list` of ``CheckBase``
        Checks to merge.
    checks_2: `None` or`list` of ``CheckBase``
        Checks to merge.
    
    Returns
    -------
    checks : `None` or `tuple` of ``CheckBase``
        The fetched down checks.
    """
    if (checks_1 is None) and (checks_2 is None):
        return None
    
    return tuple(_iter_merge_checks(checks_1, checks_2))

@export
class Command:
    """
    Represents a command.
    
    Attributes
    ----------
    _category_hint : `None` or `str`
        Hint for the command processor to detect under which category the command should go.
    _category_reference : `None` or ``WeakReferer`` to ``Category``.
        Weak reference to the command's category.
    _checks : `None` or `tuple` of ``CheckBase``
        The checks of the commands.
    _command_categories : `None` or `set` of ``CommandCategory``
        Sub command categories of the command.
    _command_function : `None` or ``CommandFunction``
        The actual command of the command to maybe call.
    _command_processor_reference : `None` or ``WeakReferer`` to ``CommandProcessor``.
        Weak reference to the command's command processor.
    _error_handlers : `None` or `list` of `FunctionType`
        Error handlers bind to the command.
    _self_reference = `None` or ``WeakReferer`` to ``Command``
        Reference to the command itself.
    _wrappers : `None`, `list` of `async-callable`
        Additional wrappers, which run before the command is executed.
    aliases : `None` or `tuple` of `str`
        Name aliases of the command if any. They are always lower case.
    command_category_name_to_command_category : `None` or `dict` of (`str`, ``CommandCategory``) items
        Sub-command categories by name.
    description : `Any`
        The command's description if any.
    display_name : `str`
        The command's display name.
    hidden : `bool`
        Whether the command should be hidden from help commands.
    hidden_if_checks_fail : `bool`
        Whether the command should be hidden from help commands if the user's checks fail.
    name : `str`
        The command's name. Always lower case.
    """
    __slots__ = ('__weakref__', '_category_hint', '_category_reference', '_checks', '_command_categories',
        '_command_function', '_command_processor_reference', '_error_handlers', '_self_reference', '_wrappers',
        'aliases', 'command_category_name_to_command_category', 'description', 'display_name', 'hidden',
        'hidden_if_checks_fail', 'name')
    
    def _iter_checks(self):
        """
        Iterates over all the checks applied to the command.
        
        This method is an iterable generator.
        
        Yields
        ------
        check : ``CheckBase``
        """
        checks = self._checks
        if (checks is not None):
            yield from checks
        
        category_reference = self._category_reference
        if (category_reference is not None):
            category = category_reference()
            if (category is not None):
                checks = category._checks
                if (checks is not None):
                    yield from checks
    
    
    def _iter_own_checks(self):
        """
        Iterates over the checks only of the command, excluding it's category's.
        
        This method is an iterable generator.
        
        Yields
        ------
        check : ``CheckBase``
        """
        checks = self._checks
        if (checks is not None):
            yield from checks
    
    
    def _iter_error_handlers(self):
        """
        Iterates over all the error handlers applied to the command.
        
        This method is an iterable generator.
        
        Yields
        ------
        error_handler : `FunctionType`
        """
        error_handlers = self._error_handlers
        if (error_handlers is not None):
            yield from error_handlers
        
        category_reference = self._category_reference
        if (category_reference is not None):
            category = category_reference()
            if (category is not None):
                error_handlers = category._error_handlers
                if (error_handlers is not None):
                    yield from error_handlers
        
        command_processor_reference = self._command_processor_reference
        if (command_processor_reference is not None):
            command_processor = command_processor_reference()
            if (command_processor is not None):
                error_handlers = command_processor._error_handlers
                if (error_handlers is not None):
                    yield from error_handlers
    
    
    def _iter_names(self):
        """
        Iterates overt he command's names.

        This method is an iterable generator.
        
        Yields
        ------
        command_name : `str`
        """
        yield self.name
        aliases = self.aliases
        if (aliases is not None):
            yield from aliases
    
    
    def _iter_wrappers(self):
        """
        Iterates over the wrappers of the command.
        
        This method is an iterable generator.
        
        Yields
        ------
        wrappers : `Any`
        """
        wrappers = self._wrappers
        if (wrappers is not None):
            yield from wrappers
    
    
    def get_category(self):
        """
        Returns the command's category if has any.
        
        Returns
        -------
        category : `None` or ``Category``
        """
        category_reference = self._category_reference
        if category_reference is None:
            category = None
        else:
            category = category_reference()
        
        return category
    
    
    def unlink_category(self):
        """
        Unlinks the command from it's category and of it's command processor as well.
        """
        command_processor = self.get_command_processor()
        self._command_processor_reference = None
        if (command_processor is not None):
            command_name_to_command = command_processor.command_name_to_command
            for name in self._iter_names():
                try:
                    command = command_name_to_command[name]
                except KeyError:
                    pass
                else:
                    if command is self:
                        del command_name_to_command[name]
            
            command_processor.commands.discard(self)
        
        
        category = self.get_category()
        self._category_reference = None
        if (category is not None):
            category.command_instances.discard(self)
    
    
    def set_category(self, category):
        """
        Sets the command's category.
        
        Parameters
        ----------
        category : ``Category``
            The new category of the command.
        
        Raises
        ------
        RuntimeError
            - The command is bound to a category of an other command processor.
            - The command would only partially overwrite
        """
        self.unlink_category()
        
        category.command_instances.add(self)
        self._category_hint = category.name
        self._category_reference = category._self_reference
        
        command_processor = category.get_command_processor()
        if (command_processor is not None):
            self.set_command_processor(command_processor)
    
    
    def set_command_processor(self, command_processor):
        """
        Sets the command's command processor.
        
        Parameters
        ----------
        command_processor : ``CommandProcessor``
            The command processor to set.
        
        Raises
        ------
        RuntimeError
            - The command is bound to a category of an other command processor.
            - The command would only partially overwrite
        """
        names = set(self._iter_names())
        command_name_to_command = command_processor.command_name_to_command
        
        would_overwrite_commands = set()
        for name in names:
            added_command = command_name_to_command.get(name, None)
            if added_command is None:
                continue
            
            would_overwrite_commands.add(added_command)
        
        for would_overwrite_command in would_overwrite_commands:
            if not names.issubset(would_overwrite_command._iter_names()):
                raise RuntimeError(f'{Command.__name__}: {self!r} would partially overwrite an other command: '
                    f'{would_overwrite_command!r}.')
        
        for name in names:
            command_name_to_command[name] = self
    
    
    def get_command_processor(self):
        """
        Returns the command's command processor if has any.
        
        Returns
        -------
        command_processor : `None` or ``CommandProcessor``
        """
        command_processor_reference = self._command_processor_reference
        if command_processor_reference is None:
            command_processor = None
        else:
            command_processor = command_processor_reference()
        
        return command_processor
    
    
    def error(self, error_handler):
        """
        Adds na error handler to the command.
        
        Parameters
        ----------
        error_handler : `async-callable`
            The error handler to add.
            
            The following parameters are passed to each error handler:
            
            +-------------------+-----------------------+
            | Name              | Type                  |
            +===================+=======================+
            | command_context   | ``CommandContext``    |
            +-------------------+-----------------------+
            | exception         | `BaseException`       |
            +-------------------+-----------------------+
            
            Should return the following parameters:
            
            +-------------------+-----------+
            | Name              | Type      |
            +===================+===========+
            | handled           | `bool`    |
            +-------------------+-----------+
        
        Returns
        -------
        error_handler : `async-callable`
        
        Raises
        ------
        TypeError
            - If `error_handler` accepts bad amount of parameters.
            - If `error_handler` is not async.
        """
        test_error_handler(error_handler)
        
        error_handlers = self._error_handlers
        if error_handlers is None:
            error_handlers = self._error_handlers = []
            
            error_handlers.append(error_handler)
        
        return error_handler
    
    
    @classmethod
    def from_class(cls, klass, kwargs=None):
        """
        The method used, when creating a ``Command`` object from a class.
        
        Extra `kwargs` are supported as well for special the use cases.
        
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        self : ``Command`` or ``Router``
        
        Raises
        ------
        TypeError
            If any attribute's or value's type is incorrect.
        ValueError
            If any attribute's or value's type is correct, but it's type isn't.
        """
        return create_event_from_class(cls, klass, COMMAND_PARAMETER_NAMES, COMMAND_NAME_NAME,
            COMMAND_COMMAND_NAME)
    
    
    def __new__(cls, command, name=None, description=None, aliases=None, category=None, checks=None,
            error_handlers=None, separator=None, assigner=None, hidden=None, hidden_if_checks_fail=None):
        """
        Creates a new ``Command`` object.
        
        Parameters
        ----------
        command : `None`, `async-callable`
            The async callable added as the command itself.
        name : `None`, `str` or `tuple` of (`None`, `Ellipsis`, `str`), Optional
            The name to be used instead of the passed `command`'s.
        description : `None`, `Any` or `tuple` of (`None`, `Ellipsis`, `Any`), Optional
            Description added to the command. If no description is provided, then it will check the commands's
            `.__doc__` attribute for it. If the description is a string instance, then it will be normalized with the
            ``normalize_description`` function. If it ends up as an empty string, then `None` will be set as the
            description.
        aliases : `None`, `str`, `list` of `str` or `tuple` of (`None, `Ellipsis`, `str`, `list` of `str`), Optional
            The aliases of the command.
        category : `None`, ``Category``, `str` or `tuple` of (`None`, `Ellipsis`, ``Category``, `str`), Optional
            The category of the command. Can be given as the category itself, or as a category's name. If given as
            `None`, then the command will go under the command processer's default category.
        checks : `None`, ``CommandCheckWrapper``, ``CheckBase``, `list` of ``CommandCheckWrapper``, ``CheckBase`` \
                instances or `tuple` of (`None`, `Ellipsis`, ``CommandCheckWrapper``, ``CheckBase`` or `list` of \
                ``CommandCheckWrapper``, ``CheckBase``), Optional
            Checks to decide in which circumstances the command should be called.
        error_handlers : `None`, `async-callable`, `list` of `async-callable`, `tuple` of (`None`, `async-callable`, \
                `list` of `async-callable`), Optional
            Error handlers for the command.
        separator : `None`, `str` or `tuple` (`str`, `str`), Optional
            The parameter separator of the command's parser.
        assigner : `None`, `str`, Optional
            Parameter assigner sign of the command's parser.
        hidden : `None`, `bool`, `tuple` (`None`, `Ellipsis`, `bool`), Optional
            Whether the command should be hidden from the help commands.
        hidden_if_checks_fail : `None`, `bool`, `tuple` (`None`, `Ellipsis`, `bool`), Optional
            Whether the command should be hidden from the help commands if any check fails.
        """
        if command is None:
            function = None
            wrappers = None
        elif isinstance(command, CommandWrapper):
            function, wrappers = command.fetch_function_and_wrappers_back()
        else:
            function = command
            wrappers = None
        
        fetched_checks = _fetch_check_from_wrappers(wrappers)
        
        route_to = 0
        name, route_to = _check_maybe_route('name', name, route_to, _validate_name)
        description, route_to = _check_maybe_route('description', description, route_to, None)
        aliases, route_to = _check_maybe_route('aliases', aliases, route_to, _validate_aliases)
        category, route_to = _check_maybe_route('category', category, route_to, _validate_category)
        checks, route_to = _check_maybe_route('checks', checks, route_to, validate_checks)
        error_handlers, route_to = _check_maybe_route('error_handlers', error_handlers, route_to,
            validate_error_handlers)
        hidden, route_to = _check_maybe_route('hidden', hidden, route_to, _validate_hidden)
        hidden_if_checks_fail, route_to = _check_maybe_route('hidden_if_checks_fail', hidden_if_checks_fail, route_to,
            _validate_hidden_if_checks_fail)
        
        
        if route_to:
            name = route_name(name, route_to)
            name = [check_name(command, name) for name in name]
            name = [raw_name_to_display(name) for name in name]
            default_description = _generate_description_from(command, None)
            description = route_value(description, route_to, default=default_description)
            aliases = route_value(aliases, route_to)
            category = route_value(category, route_to)
            checks = route_value(checks, route_to)
            error_handlers = route_value(error_handlers, route_to)
            hidden = route_value(hidden, route_to)
            hidden_if_checks_fail = route_value(hidden_if_checks_fail, route_to)
            
            category_hint = [_generate_category_hint_from(category) for category in category]
            
            description = [
                _generate_description_from(function, description)
                    if ((description is None) or (description is not default_description)) else default_description
                for description in description]
        else:
            name = check_name(function, name)
            name = raw_name_to_display(name)
            
            description = _generate_description_from(function, description)
            category_hint = _generate_category_hint_from(category)
        
        if function is None:
            command_function = None
        else:
            content_parser, function = CommandContentParser(function, separator, assigner)
            
            command_function = CommandFunction(function, content_parser)
        
        if route_to:
            router = []
            
            for name, aliases, description, category_hint, checks, error_handlers, hidden, hidden_if_checks_fail \
                    in zip(name, aliases, description, category_hint, checks, error_handlers, hidden,
                        hidden_if_checks_fail):
                
                if (aliases is not None):
                    aliases = tuple(aliases)
                
                self = object.__new__(cls)
                self._category_hint = category_hint
                self._category_reference = None
                self._checks = _merge_checks(checks, fetched_checks)
                self._command_function = command_function
                self._command_processor_reference = None
                self._error_handlers = error_handlers
                self._command_categories = None
                self.aliases = aliases
                self.description = description
                self.display_name = name
                self.hidden = hidden
                self.hidden_if_checks_fail = hidden_if_checks_fail
                self.name = name
                self.command_category_name_to_command_category = None
                self._wrappers = None
                self._self_reference = None
                
                self_reference = WeakReferer(self)
                self._self_reference = self_reference
                
                if (command_function is not None):
                    command_function._command_category_reference = self_reference
                
                
                if (wrappers is not None):
                    for wrapper in wrappers:
                        wrapper.apply(self)
                
                router.append(self)
            
            return Router(router)
        else:
            if (aliases is not None):
                aliases = tuple(aliases)
            
            self = object.__new__(cls)
            self._category_hint = category_hint
            self._category_reference = None
            self._checks = _merge_checks(checks, fetched_checks)
            self._command_function = command_function
            self._command_processor_reference = None
            self._error_handlers = error_handlers
            self._command_categories = None
            self.aliases = aliases
            self.description = description
            self.display_name = name
            self.hidden = hidden
            self.hidden_if_checks_fail = hidden_if_checks_fail
            self.name = name
            self.command_category_name_to_command_category = None
            self._wrappers = None
            self._self_reference = None
            
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
            
            if (command_function is not None):
                command_function._command_category_reference = self_reference
            
            if (wrappers is not None):
                for wrapper in wrappers:
                    wrapper.apply(self)
            
            return self
    
    def __repr__(self):
        """Returns the command's representation."""
        repr_parts = ['<', self.__class__.__name__, ' name=', repr(self.name)]
        
        aliases = self.aliases
        if (aliases is not None):
            repr_parts.append(' aliases=')
            repr_parts.append(repr(aliases))
        
        category_hint = self._category_hint
        if (category_hint is not None):
            repr_parts.append(' category=')
            repr_parts.append(repr(category_hint))
        
        command_function = self._command_function
        if (command_function is not None):
            repr_parts.append(' command_function=')
            repr_parts.append(repr(command_function))
        
        command_categories = self._command_categories
        if (command_categories is not None):
            repr_parts.append(' command_categories=')
            repr_parts.append(repr(command_categories))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    def copy(self):
        """
        Copies the command.
        
        Returns
        -------
        new : ``Command``
        """
        new = object.__new__(type(self))
        new._category_hint = self._category_hint
        new._category_reference = None
        
        checks = self._checks
        if (checks is not None):
            checks = tuple(checks)
        new._checks = checks
        
        command_function = self._command_function
        if (command_function is not None):
            command_function = command_function.copy()
        new._command_function = command_function
        
        new._command_processor_reference = None
        
        error_handlers = self._error_handlers
        if (error_handlers is not None):
            error_handlers = error_handlers.copy()
        new._error_handlers = error_handlers
        
        command_categories  = self._command_categories
        if (command_categories is not None):
            command_categories = {command_category.copy() for command_category in command_categories}
        new._command_categories = command_categories
        
        if (command_categories is None):
            command_category_name_to_command_category = None
        else:
            command_category_name_to_command_category = {}
            for command_category in command_categories:
                for name in command_category._iter_names():
                    command_category_name_to_command_category[name] = command_category
        
        new.command_category_name_to_command_category = command_category_name_to_command_category
        
        aliases = self.aliases
        if (aliases is not None):
            aliases = tuple(aliases)
        new.aliases = aliases
        
        new.description = self.description
        new.display_name = self.display_name
        new.hidden = self.hidden
        new.hidden_if_checks_fail = self.hidden_if_checks_fail
        new.name = self.name
        
        wrappers = self._wrappers
        if (wrappers is not None):
            wrappers = wrappers.copy()
        new._wrappers = wrappers
        
        new._self_reference = None
        
        self_reference = WeakReferer(new)
        self._self_reference = self_reference
        
        if (command_function is not None):
            command_function._command_category_reference = self_reference
        
        if (command_categories is not None):
            for command_category in command_categories:
                command_category._command_category_reference = self_reference
        
        return new
    
    
    def __hash__(self):
        """Returns the hash value of the command."""
        hash_value = 0
        
        category_hint = self._category_hint
        if (category_hint is not None):
            hash_value ^= hash(category_hint)
        
        checks = self._checks
        if (checks is not None):
            hash_value ^= len(checks)<<6
            for check in checks:
                hash_value ^= hash(check)
        
        command_function = self._command_function
        if (command_function is not None):
            try:
                command_function_hash = hash(command_function)
            except TypeError:
                command_function_hash = object.__hash__(command_function)
            hash_value ^= command_function_hash
        
        error_handlers = self._error_handlers
        if (error_handlers is not None):
            hash_value ^= len(error_handlers)<<12
            for error_handler in error_handlers:
                hash_value ^= hash(error_handler)
        
        command_categories = self._command_categories
        if (command_categories is not None):
            hash_value ^= len(command_categories)<<18
            for command_category in command_categories:
                hash_value ^= hash(command_category)
        
        aliases = self.aliases
        if (aliases is not None):
            hash_value ^= len(aliases)<<24
            for alias in aliases:
                hash_value ^= hash(alias)
        
        description = self.description
        if (description is not None):
            try:
                description_hash = hash(description)
            except KeyError:
                description_hash = object.__hash__(description)
            
            hash_value ^= description_hash
        
        hash_value ^= self.hidden<<30
        hash_value ^= self.hidden_if_checks_fail<<31
        hash_value ^= hash(self.name)
        
        wrappers = self._wrappers
        if (wrappers is not None):
            hash_value ^= len(wrappers)<<28
            for wrapper in wrappers:
                try:
                    wrapper_hash = hash(wrapper)
                except TypeError:
                    wrapper_hash = object.__hash__(wrapper)
                hash_value ^= wrapper_hash
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two commands are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._category_hint != other._category_hint:
            return False
        
        if self._checks != other._checks:
            return False
        
        if self._command_function != other._command_function:
            return False
        
        if self._error_handlers != other._error_handlers:
            return False
        
        if self._command_categories != other._command_categories:
            return False
        
        if self.aliases != other.aliases:
            return False
        
        if self.description != other.description:
            return False
        
        if self.hidden != other.hidden:
            return False
        
        if self.hidden_if_checks_fail != other.hidden_if_checks_fail:
            return False
        
        if self.name != other.name:
            return False
        
        if self._wrappers != other._wrappers:
            return False
        
        return True
    
    
    def _add_command_category(self, command_category):
        """
        Adds a command category to the command.
        
        Parameters
        ----------
        command_category : ``CommandCategory``
        """
        command_categories = self._command_categories
        command_category_name_to_command_category = self.command_category_name_to_command_category
        if command_categories is None:
            command_categories = self._command_categories = set()
            command_category_name_to_command_category = self.command_category_name_to_command_category = {}
        else:
            for name in command_category._iter_names():
                if name in command_category_name_to_command_category:
                    raise RuntimeError(f'Duped `{CommandCategory.__name__}` name: {name!r}.')
        
        command_categories.add(command_category)
        for name in command_category._iter_names():
            command_category_name_to_command_category[name] = command_category
        
        command_category._command_category_reference = self._self_reference
    
    
    def create_event(self, command, *args, **kwargs):
        """
        Adds a sub-command to the command.
        
        Parameters
        ----------
        command : ``Command``, ``Router``, `None`, `async-callable`
            Async callable to add as a command.
        *args : Positional parameters
            Positional parameters to pass to the command's constructor.
        **kwargs : Keyword parameters
            Keyword parameters to pass to the command's constructor.
        
        Returns
        -------
        command_category : ``CommandCategory``
            The added command category instance.
        """
        if isinstance(command, (Command, Router)):
            raise TypeError(f'`{Command.__name__}` and `{Router.__name__}` instances cannot be added as sub-commands, '
                f'got {command!r}.')
        
        command = Command(command, *args, **kwargs)
        
        command_category = CommandCategory._from_command(command)
        self._add_command_category(command_category)
        return command_category
    
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command.
    
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        command : ``Command``
            The added command instance.
        """
        command = Command.from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        command_category = CommandCategory._from_command(command)
        self._add_command_category(command_category)
        return command_category
    
    
    @property
    def commands(self):
        """
        Enables you to add sub-commands or sub-categories to the command.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        """
        return _EventHandlerManager(self)
    
    
    def add_wrapper(self, command_wrapper):
        """
        Adds a wrapper to run before the command is executed.
        
        Parameters
        ----------
        command_wrapper : `async-callable`
            Command wrapper to add.
        """
        wrappers = self._wrappers
        if (wrappers is None):
            wrappers = self._wrappers = []
        
        wrappers.append(command_wrapper)
    
    def add_check(self, check):
        """
        Adds a check to the command.
        
        Parameters
        ----------
        check : ``CheckBase``
        """
        checks = self._checks
        if checks is None:
            checks = (check,)
        else:
            checks = (*checks, check)
        
        self._checks = checks

class CommandFunction:
    """
    Command function.
    
    Attributes
    ----------
    _command_category_reference : `None` or ``WeakReferer`` to (``Command`` or ``CommandCategory``)
        Reference to the command function's parent.
    _function : `Any`
        The command's function to call.
    _content_parser : ``CommandContentParser``
        Content parser for the command.
    """
    __slots__ = ('_command_category_reference', '_content_parser', '_function', )
    def __new__(cls, function, content_parser):
        """
        Creates a new ``CommandFunction`` with the given parameters.
        
        Parameters
        ----------
        function : `Any`
            Content parser for the command.
        content_parser : ``CommandContentParser``
            The command's function to call.
        """
        self = object.__new__(cls)
        self._function = function
        self._content_parser = content_parser
        self._command_category_reference = None
        return self
    
    def __repr__(self):
        """Returns the command function's representation."""
        return f'<{self.__class__.__name__} content_parser={self._content_parser!r} function={self._function!r}>'
    
    def copy(self):
        """
        Copying a command function returns itself.
        
        Returns
        -------
        new : ``CommandFunction``
        """
        return self
    
    def __hash__(self):
        """Returns the hash value of the command function."""
        return hash(self._content_parser)^hash(self._function)
    
    def __eq__(self, other):
        """Returns whether the wo command functions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self is other:
            return True
        
        if self._function != other._function:
            return False
        
        if self._content_parser != other._content_parser:
            return False
        
        return True

    def _iter_wrappers(self):
        """
        Iterates over the wrappers of the command function and of it's parent categories.
        
        This method is an iterable generator.
        
        Yields
        ------
        wrapper : `Any`
        """
        command_category_reference = self._command_category_reference
        if (command_category_reference is not None):
            command_category = command_category_reference()
            if (command_category is not None):
                yield from command_category._iter_wrappers()
    
    
    def _iter_error_handlers(self):
        """
        Iterates over all the error handlers applied to the command function's parent categories..
        
        This method is an iterable generator.
        
        Yields
        ------
        error_handler : `FunctionType`
        """
        command_category_reference = self._command_category_reference
        if (command_category_reference is not None):
            command_category = command_category_reference()
            if (command_category is not None):
                yield from command_category._iter_error_handlers()


class CommandCategory:
    """
    Folder for sub-commands of a ``Command``.
    
    Attributes
    ----------
    _command_categories : `None` or `set` of ``CommandCategory``
        Sub command categories of the command.
    _command_category_reference : `None` or ``WeakReferer`` to (``Command`` or ``CommandCategory``)
        Reference to the command category's parent.
    _command_function : `None` or ``CommandFunction``
        The actual command of the command to maybe call.
    _self_reference : `None` or ``WeakReferer`` to ``CommandCategory``
        Reference to the command category itself.
    _error_handlers : `None` or `list` of `FunctionType`
        Error handlers bind to the command.
    _wrappers : `None`, `list` of `async-callable`
        Additional wrappers, which run before the command is executed.
    aliases : `None` or `tuple` of `str`
        Name aliases of the command category.
    command_category_name_to_command_category : `None` of `dict` of (`str`, `Any`) items
        Command categories by name.
    description : `Any`
        The command's description if any.
    display_name : `str`
        The command's display name.
    name : `str`
        The command's name. Always lower case.
    """
    __slots__ = ('__weakref__', '_command_categories', '_command_category_reference', '_command_function',
        '_error_handlers', '_self_reference', '_wrappers', 'aliases', 'command_category_name_to_command_category',
        'description', 'display_name', 'name',)
    
    @classmethod
    def _from_command(cls, source_command):
        """
        Creates command category from the given command.
        
        Parameters
        ----------
        source_command : ``Command``
            The command to turn into command category.
        
        Returns
        -------
        self : ``CommandCategory``
        """
        self = object.__new__(cls)
        self.aliases = source_command.aliases
        self.name = source_command.name
        self.display_name = source_command.display_name
        self.description = source_command.description
        command_function = source_command._command_function
        self._command_function = command_function
        self._command_categories = source_command._command_categories
        self.command_category_name_to_command_category = None
        self._command_category_reference = None
        self._self_reference = None
        
        wrappers = source_command._wrappers
        if (wrappers is not None):
            wrappers = wrappers.copy()
        self._wrappers = wrappers
        
        error_handlers = source_command._error_handlers
        if (error_handlers is not None):
            error_handlers = error_handlers.copy()
        self._error_handlers = error_handlers
        
        self_reference = WeakReferer(self)
        self._self_reference = self_reference
        
        if (command_function is not None):
            command_function._command_category_reference = self_reference
        
        return self
    
    def copy(self):
        """
        Copies the command category.
        
        Returns
        -------
        new : ``CommandCategory``
        """
        new = object.__new__(type(self))
        
        command_function = self._command_function
        if (command_function is not None):
            command_function = command_function.copy()
        new._command_function = command_function
        
        error_handlers = self._error_handlers
        if (error_handlers is not None):
            error_handlers = error_handlers.copy()
        new._error_handlers = error_handlers
        
        command_categories  = self._command_categories
        if (command_categories is not None):
            command_categories = {command_category.copy() for command_category in command_categories}
        new._command_categories = command_categories
        
        if (command_categories is None):
            command_category_name_to_command_category = None
        else:
            command_category_name_to_command_category = {}
            for command_category in command_categories:
                for name in command_category._iter_names():
                    command_category_name_to_command_category[name] = command_category
        
        new.command_category_name_to_command_category = command_category_name_to_command_category
        
        aliases = self.aliases
        if (aliases is not None):
            aliases = tuple(aliases)
        new.aliases = aliases
        
        new.description = self.description
        new.display_name = self.display_name
        new.name = self.name
        
        wrappers = self._wrappers
        if (wrappers is not None):
            wrappers = wrappers.copy()
        new._wrappers = wrappers
        
        new._command_category_reference = self._command_category_reference
        
        new._self_reference = None
        
        self_reference = WeakReferer(new)
        self._self_reference = self_reference
        
        if (command_function is not None):
            command_function._command_category_reference = self_reference
        
        if (command_categories is not None):
            for command_category in command_categories:
                command_category._command_category_reference = self_reference
        
        return new
    
    
    def __repr__(self):
        """Returns the command category's representation."""
        repr_parts = ['<', self.__class__.__name__, ' name=', repr(self.name)]
        
        command_function = self._command_function
        if (command_function is not None):
            repr_parts.append(' command_function=')
            repr_parts.append(repr(command_function))
        
        command_categories = self._command_categories
        if (command_categories is not None):
            repr_parts.append(' command_categories=')
            repr_parts.append(repr(command_categories))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    def __hash__(self):
        """Returns the command category's hash value."""
        hash_value = 0
        
        command_function = self._command_function
        if (command_function is not None):
            try:
                command_function_hash = hash(command_function)
            except TypeError:
                command_function_hash = object.__hash__(command_function)
            hash_value ^= command_function_hash
        
        error_handlers = self._error_handlers
        if (error_handlers is not None):
            hash_value ^= len(error_handlers)<<12
            for error_handler in error_handlers:
                hash_value ^= hash(error_handler)
        
        command_categories = self._command_categories
        if (command_categories is not None):
            hash_value ^= len(command_categories)<<18
            for command_category in command_categories:
                hash_value ^= hash(command_category)
        
        aliases = self.aliases
        if (aliases is not None):
            hash_value ^= len(aliases)<<24
            for alias in aliases:
                hash_value ^= hash(alias)
        
        description = self.description
        if (description is not None):
            try:
                description_hash = hash(description)
            except KeyError:
                description_hash = object.__hash__(description)
            
            hash_value ^= description_hash
        
        wrappers = self._wrappers
        if (wrappers is not None):
            hash_value ^= len(wrappers)<<28
            for wrapper in wrappers:
                try:
                    wrapper_hash = hash(wrapper)
                except TypeError:
                    wrapper_hash = object.__hash__(wrapper)
                hash_value ^= wrapper_hash
        
        hash_value ^= hash(self.name)
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two command categories are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._command_function != other._command_function:
            return False
        
        if self._error_handlers != other._error_handlers:
            return False
        
        if self._command_categories != other._command_categories:
            return False
        
        if self.description != other.description:
            return False
        
        if self.name != other.name:
            return False
        
        if self._wrappers != other._wrappers:
            return False
        
        return True
    
    
    def _iter_names(self):
        """
        Iterates over the command category's names.
        
        This method is a generator.
        
        Yields
        ------
        name : `str`
        """
        yield self.name
        
        aliases = self.aliases
        if (aliases is not None):
            yield from aliases
    
    
    def _iter_wrappers(self):
        """
        Iterates over the wrappers of the command category and of parent categories.
        
        This method is an iterable generator.
        
        Yields
        ------
        wrapper : `Any`
        """
        wrappers = self._wrappers
        if (wrappers is not None):
            yield from wrappers
        
        command_category_reference = self._command_category_reference
        if (command_category_reference is not None):
            command_category = command_category_reference()
            if (command_category is not None):
                yield from command_category._iter_wrappers()
    
    
    def _iter_error_handlers(self):
        """
        Iterates over all the error handlers applied to the command categories's parent categories..
        
        This method is an iterable generator.
        
        Yields
        ------
        error_handler : `FunctionType`
        """
        error_handlers = self._error_handlers
        if (error_handlers is not None):
            yield from error_handlers
        
        command_category_reference = self._command_category_reference
        if (command_category_reference is not None):
            command_category = command_category_reference()
            if (command_category is not None):
                yield from command_category._iter_error_handlers()
    
    
    def _add_command_category(self, command_category):
        """
        Adds a command category to the command.
        
        Parameters
        ----------
        command_category : ``CommandCategory``
        """
        command_categories = self._command_categories
        command_category_name_to_command_category = self.command_category_name_to_command_category
        if command_categories is None:
            command_categories = self._command_categories = set()
            command_category_name_to_command_category = self.command_category_name_to_command_category = {}
        else:
            for name in command_category._iter_names():
                if name in command_category_name_to_command_category:
                    raise RuntimeError(f'Duped `{CommandCategory.__name__}` name: {name!r}.')
        
        command_categories.add(command_category)
        for name in command_category._iter_names():
            command_category_name_to_command_category[name] = command_category
        
        command_category._command_category_reference = self._self_reference
    
    
    def create_event(self, command, *args, **kwargs):
        """
        Adds a sub-command to the command.
        
        Parameters
        ----------
        command : ``Command``, ``Router``, `None`, `async-callable`
            Async callable to add as a command.
        *args : Positional parameters
            Positional parameters to pass to the command's constructor.
        **kwargs : Keyword parameters
            Keyword parameters to pass to the command's constructor.
        
        Returns
        -------
        command_category : ``CommandCategory``
            The added command category instance.
        """
        if isinstance(command, (Command, Router)):
            raise TypeError(f'`{Command.__name__}` and `{Router.__name__}` instances cannot be added as sub-commands, '
                f'got {command!r}.')
        
        command = Command(command, *args, **kwargs)
        
        command_category = CommandCategory._from_command(command)
        self._add_command_category(command_category)
    
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a sub-command.
    
        Parameters
        ----------
        klass : `type`
            The class, from what's attributes the command will be created.
        
        Returns
        -------
        command : ``Command``
            The added command instance.
        """
        command = Command.from_class(klass)
        if isinstance(command, Router):
            command = command[0]
        
        command_category = CommandCategory._from_command(command)
        self._add_command_category(command_category)
        return command_category
    
    
    @property
    def commands(self):
        """
        Enables you to add sub-commands or sub-categories to the command.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        """
        return _EventHandlerManager(self)
    
    
    def error(self, error_handler):
        """
        Adds na error handler to the command.
        
        Parameters
        ----------
        error_handler : `async-callable`
            The error handler to add.
            
            The following parameters are passed to each error handler:
            
            +-------------------+-----------------------+
            | Name              | Type                  |
            +===================+=======================+
            | command_context   | ``CommandContext``    |
            +-------------------+-----------------------+
            | exception         | `BaseException`       |
            +-------------------+-----------------------+
            
            Should return the following parameters:
            
            +-------------------+-----------+
            | Name              | Type      |
            +===================+===========+
            | handled           | `bool`    |
            +-------------------+-----------+
        
        Returns
        -------
        error_handler : `async-callable`
        
        Raises
        ------
        TypeError
            - If `error_handler` accepts bad amount of parameters.
            - If `error_handler` is not async.
        """
        test_error_handler(error_handler)
        
        error_handlers = self._error_handlers
        if error_handlers is None:
            error_handlers = self._error_handlers = []
            
            error_handlers.append(error_handler)
        
        return error_handler
