__all__ = ('Category',)

from ...backend.utils import WeakReferer

from .command_helpers import validate_checks, normalize_description, raw_name_to_display, test_error_handler


class Category:
    """
    Category of commands.
    
    Parameters
    ----------
    _checks : `None` or `tuple` of ``CheckBase``
        The checks of the category.
    _command_processor_reference : `None` or ``WeakReferer`` to ``CommandProcessor``.
        Weak reference to the category's command processor.
    _error_handlers : `None` or `list` of `function`
        Error handlers bind to the category.
    _self_reference : `None` or ``WeakReferer`` to ``Category``
        Reference to the command processor itself.
    registered_commands : `set` of ``Command``
        The registered commands to the category.
    display_name : `str`
        The category's display name.
    description : `Any`
        The category's description.
    name : `str`
        The category's name. Always lower case.
    Notes
    -----
    ``Category`` supports weakreferencing.
    """
    __slots__ = ('__weakref__', '_checks', '_command_processor_reference', '_error_handlers', '_self_reference',
        'registered_commands', 'description', 'display_name', 'name')
    
    def __new__(cls, name, *, checks=None, description=None):
        """
        Creates a new category with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The category's name.
        checks : `None`, ``CheckBase``, ``CommandCheckWrapper`` or (`list`, `tuple` or `set`) of \
                (``CheckBase`` or ``CommandCheckWrapper``), Optional (Keyword only)
            The checks of the category.
        description : `Any`
            Description of the category.
        
        Raises
        ------
        TypeError
            - If `name` is not `str` instance.
            - If `checks`'s type is incorrect.
            - If a `check`'s type is incorrect.
        """
        name_type = type(name)
        if name_type is str:
            pass
        elif issubclass(name_type, str):
            name = str(name)
        else:
            raise TypeError(f'`name` can be give as `str` instance, got {name_type.__name__}.')
        
        name = raw_name_to_display(name)
        
        checks = validate_checks(checks)
        description = normalize_description(description)
        
        self = object.__new__(cls)
        self._checks = checks
        self._command_processor_reference = None
        self._error_handlers = None
        self._self_reference = None
        self.registered_commands = {}
        self.display_name = name
        self.description = description
        self.name = name
        
        self._self_reference = WeakReferer(self)
        
        return self
    
    
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
        if (other_category is None) or (self is not other_category):
            other_category.unlink()
        
        category_name_to_category[name] = self
        
        command_name_rule = command_processor._command_name_rule
        if (command_name_rule is not None):
            self.display_name = command_name_rule(self.name)
        
        for command in self.registered_commands:
            command.set_command_processor(command_processor)
    
    
    def unlink(self):
        """
        Unlinks the category from it's command processor if applicable.
        
        """
        command_processor = self.get_command_processor()
        self._command_processor_reference = None
        
        if (command_processor is not None):
            registered_commands = list(self.registered_commands)
            for command in registered_commands:
                command.unlink()
        
        category_name_to_category = command_processor.category_name_to_category
        name = self.name
        
        other_category = category_name_to_category.get(name, None)
        if (other_category is not None) and (other_category is self):
            del category_name_to_category[name]
    
    
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
            - If `error_handler` accepts bad amount of arguments.
            - If `error_handler` is not async.
        """
        test_error_handler(error_handler)
        
        error_handlers = self._error_handlers
        if error_handlers is None:
            error_handlers = self._error_handlers = []
            
            error_handlers.append(error_handler)
        
        return error_handler

