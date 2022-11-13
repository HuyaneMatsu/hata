__all__ = ('Category',)

from scarletio import WeakReferer, include

from ...discord.events.handling_helpers import Router, _EventHandlerManager

from .command_helpers import test_error_handler, validate_checks
from .utils import normalize_description, raw_name_to_display


Command = include('Command')

class Category:
    """
    Category of commands.
    
    Attributes
    ----------
    _checks : `None`, `tuple` of ``CheckBase``
        The checks of the category.
    _command_processor_reference : `None`, ``WeakReferer`` to ``CommandProcessor``.
        Weak reference to the category's command processor.
    _error_handlers : `None`, `list` of `FunctionType`
        Error handlers bind to the category.
    _self_reference : `None`, ``WeakReferer`` to ``Category``
        Reference to the command processor itself.
    command_instances : `set` of ``Command``
        The registered commands to the category.
    display_name : `str`
        The category's display name.
    description : `Any`
        The category's description.
    hidden : `bool`
        Whether the category should be hidden from help commands.
    hidden_if_checks_fail : `bool`
        Whether the category should be hidden from help commands if it's checks fail.
    name : `str`
        The category's name. Always lower case.
    
    Notes
    -----
    ``Category`` supports weakreferencing.
    """
    __slots__ = (
        '__weakref__', '_checks', '_command_processor_reference', '_error_handlers', '_self_reference',
        'command_instances', 'description', 'display_name', 'hidden', 'hidden_if_checks_fail', 'name'
    )
    
    def __new__(cls, name, *, checks=None, description = None, hidden=False, hidden_if_checks_fail=True):
        """
        Creates a new category with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The category's name.
        checks : `None`, ``CheckBase``, ``CommandCheckWrapper`` or (`list`, `tuple`, `set`) of \
                (``CheckBase``, ``CommandCheckWrapper``) = `None`, Optional (Keyword only)
            The checks of the category.
        description : `Any` = `None`, Optional (Keyword only)
            Description of the category.
        hidden : `bool` = `False`, Optional (Keyword only)
            Whether the category should be hidden from help commands.
        hidden_if_checks_fail : `bool` = `True`, Optional (Keyword only)
            Whether the category should be hidden from help commands if it's checks fail. Defaults to `True`.
        
        Raises
        ------
        TypeError
            - If `name` is not `str`.
            - If `checks`'s type is incorrect.
            - If a `check`'s type is incorrect.
            - If `hidden` was not given as `bool`.
            - If `hidden_if_checks_fail` was not given as `bool`.
        """
        name_type = type(name)
        if name_type is str:
            pass
        elif issubclass(name_type, str):
            name = str(name)
        else:
            raise TypeError(
                f'`name` can be `str`, got {name_type.__name__}; {name!r}.'
            )
        
        if not isinstance(hidden, bool):
            raise TypeError(
                f'`hidden` can be `bool`, got {hidden.__class__.__name__}; {hidden!r}.'
            )
        
        if not isinstance(hidden_if_checks_fail, bool):
            raise TypeError(
                f'`hidden_if_checks_fail` can be `bool`, got '
                f'{hidden_if_checks_fail.__class__.__name__}; {hidden_if_checks_fail!r}.'
            )
        
        name = raw_name_to_display(name)
        
        checks = validate_checks(checks)
        description = normalize_description(description)
        
        self = object.__new__(cls)
        self._checks = checks
        self._command_processor_reference = None
        self._error_handlers = None
        self._self_reference = None
        self.command_instances = set()
        self.display_name = name
        self.description = description
        self.name = name
        self.hidden = hidden
        self.hidden_if_checks_fail = hidden_if_checks_fail
        
        self._self_reference = WeakReferer(self)
        
        return self
    
    
    def get_command_processor(self):
        """
        Returns the command's command processor if has any.
        
        Returns
        -------
        command_processor : `None`, ``CommandProcessor``
        """
        command_processor_reference = self._command_processor_reference
        if command_processor_reference is None:
            command_processor = None
        else:
            command_processor = command_processor_reference()
        
        return command_processor
    
    
    def set_command_processor(self, command_processor):
        """
        Sets the command processor to the category.
        
        Parameters
        ----------
        command_processor : ``CommandProcessor``
            The parent command processor.
        """
        self._command_processor_reference = command_processor._self_reference
        
        category_name_to_category = command_processor.category_name_to_category
        name = self.name
        other_category = category_name_to_category.get(name, None)
        if (other_category is not None) and (self is not other_category):
            other_category.unlink()
        
        category_name_to_category[name] = self
        command_processor.categories.add(self)
        
        command_name_rule = command_processor._command_name_rule
        if (command_name_rule is not None):
            self.display_name = command_name_rule(self.name)
        
        for command in self.command_instances:
            command.set_command_processor(command_processor)
    
    
    def unlink(self):
        """
        Unlinks the category from it's command processor if applicable.
        """
        command_processor = self.get_command_processor()
        self._command_processor_reference = None
        
        if (command_processor is not None):
            commands = list(self.command_instances)
            for command in commands:
                command.unlink_category()
        
        category_name_to_category = command_processor.category_name_to_category
        name = self.name
        
        other_category = category_name_to_category.get(name, None)
        if (other_category is not None) and (other_category is self):
            del category_name_to_category[name]
        
        command_processor.categories.discard(self)
    
    
    def error(self, error_handler):
        """
        Adds na error handler to the category.
        
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
    
    
    def _iter_own_checks(self):
        """
        Iterates over the checks of the category.
        
        This method is a generator, which should be used inside of a for loop.
        
        Yields
        ------
        check : ``CheckBase``
        """
        checks = self._checks
        if (checks is not None):
            yield from checks
    
    
    @property
    def checks(self):
        """
        A get-set-del property to modify the category's checks.
        """
        return self._checks
    
    @checks.setter
    def checks(self, checks):
        checks = validate_checks(checks)
        self._checks = checks
    
    @checks.deleter
    def checks(self):
        self._checks = None
    
    
    @property
    def commands(self):
        """
        Enables you to add sub-commands or sub-categories to the command.
        
        Returns
        -------
        handler : ``_EventHandlerManager``
        """
        return _EventHandlerManager(self)


    def create_event(self, command, name=None, description = None, aliases=None, category=None, checks=None,
            error_handlers=None, separator=None, assigner=None, hidden=None, hidden_if_checks_fail=None):
        """
        Adds a command to the command processor.
        
        Parameters
        ----------
        command : ``Command``, ``Router``, `None`, `async-callable`
            Async callable to add as a command.
        name : `None`, `str` = `None`, Optional
            The command's name.
        name : `None`, `str`, `tuple` of (`None`, `Ellipsis`, `str`) = `None`, Optional
            The name to be used instead of the passed `command`'s.
        description : `None`, `Any`, `tuple` of (`None`, `Ellipsis`, `Any`) = `None`, Optional
            Description added to the command. If no description is provided, then it will check the commands's
            `.__doc__` attribute for it. If the description is a string instance, then it will be normalized with the
            ``normalize_description`` function. If it ends up as an empty string, then `None` will be set as the
            description.
        aliases : `None`, `str`, `list` of `str`, `tuple` of (`None, `Ellipsis`, `str`, `list` of `str`) = `None`
                , Optional
            The aliases of the command.
        category : `None`, ``Category``, `str`, `tuple` of (`None`, `Ellipsis`, ``Category``, `str`) = `None`
                , Optional
            The category of the command. Can be given as the category itself, or as a category's name. If given as
            `None`, then the command will go under the command processor's default category.
        checks : `None`, ``CommandCheckWrapper``, ``CheckBase``, `list` of ``CommandCheckWrapper``, ``CheckBase`` \
                instances or `tuple` of (`None`, `Ellipsis`, ``CommandCheckWrapper``, ``CheckBase``, `list` of \
                ``CommandCheckWrapper``, ``CheckBase``) = `None`, Optional
            Checks to decide in which circumstances the command should be called.
        error_handlers : `None`, `async-callable`, `list` of `async-callable`, `tuple` of (`None`, `async-callable`, \
                `list` of `async-callable`) = `None`, Optional
            Error handlers for the command.
        separator : `None`, `str`, `tuple` (`str`, `str`) = `None`, Optional
            The parameter separator of the command's parser.
        assigner : `None`, `str` = `None`, Optional
            Parameter assigner sign of the command's parser.
        hidden : `None`, `bool`, `tuple` (`None`, `Ellipsis`, `bool`) = `None`, Optional
            Whether the command should be hidden from the help commands.
        hidden_if_checks_fail : `None`, `bool`, `tuple` (`None`, `Ellipsis`, `bool`) = `None`, Optional
            Whether the command should be hidden from the help commands if any check fails.
        
        Returns
        -------
        command : ``Command``
            The added command instance.
        """
        if isinstance(command, Command):
            pass
        elif isinstance(command, Router):
            command = command[0]
        else:
            command = Command(command, name, description, aliases, category, checks, error_handlers, separator,
                assigner, hidden, hidden_if_checks_fail)
        
        command._category_hint = self.name
        
        self._add_command(command)
        return command
    
    
    def create_event_from_class(self, klass):
        """
        Breaks down the given class to it's class attributes and tries to add it as a command.
    
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
        
        command._category_hint = self.name
        
        self._add_command(command)
        return command
    
    
    def _add_command(self, command):
        """
        Adds the command to the category.
        
        Parameters
        ----------
        command : ``Command``
            The command to add to the category.
        
        Raises
        ------
        RuntimeError
            - The category is not linked to a command processor.
            - The command is bound to an other command processor.
            - The command would only partially overwrite
        """
        command_processor_reference = self._command_processor_reference
        if (command_processor_reference is not None):
            command_processor = command_processor_reference()
            if (command_processor is not None):
                command_processor._add_command(command)
                return
        
        raise RuntimeError(
            f'The category: {self!r} is not linked to a command processor.'
        )
