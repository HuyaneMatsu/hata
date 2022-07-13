__all__ = ('WeakReferer',)

from scarletio import RichAttributeErrorBaseType, WeakReferer

from .function import CommandFunction
from .helpers import normalize_command_name
from .result import (
    COMMAND_RESULT_CODE_CATEGORY_EMPTY, COMMAND_RESULT_CODE_CATEGORY_REQUIRES_PARAMETER,
    COMMAND_RESULT_CODE_CATEGORY_UNKNOWN_SUB_COMMAND, CommandResult
)


class CommandCategory(RichAttributeErrorBaseType):
    """
    Command line command category.
    
    Attributes
    ----------
    _command_categories : `None`, `dict` of (`str`, ``CommandCategory``) items
        Sub commands of the command.
    _command_function : `None`, ``CommandFunction``
        Command to call, if sub command could not be detected.
    _parent_reference : `None`, ``WeakReferer``
        Weakreference to the command category's parent.
    _self_reference : `None`, ``WeakReferer``
        Weakreference to the category itself.
    name : `None`, `str`
        The sub command category's name.
    """
    __slots__ = (
        '__weakref__', '_command_categories', '_command_function', '_parent_reference', '_self_reference', 'name'
    )
    
    def __new__(cls, parent, name):
        """
        Creates a new command line command category.
        
        Parameters
        ----------
        parent : ``Command``, ``CommandCategory``
            The parent command or command category.
        name : `None`, `str`
            The command category's name.
        """
        if (name is not None):
            name = normalize_command_name(name)
        
        self = object.__new__(cls)
        self.name = name
        self._command_function = None
        self._command_categories = None
        self._self_reference = None
        self._parent_reference = parent._self_reference
        
        self._self_reference = WeakReferer(self)
        
        return self
    
    
    def register_command_category(self, name):
        """
        Registers a sub command to the command.
        
        Parameters
        ----------
        name : `str`
            The name of the sub-command.
        
        Returns
        -------
        sub_command : ``CommandCategory``
        """
        sub_command = CommandCategory(self, name)
        sub_commands = self._command_categories
        if (sub_commands is None):
            sub_commands = {}
            self._command_categories = sub_commands
        
        sub_commands[sub_command.name] = sub_command
        return sub_command
    
    
    def register_command_function(self, function, name, description):
        """
        Parameters
        ----------
        function : `callable`
            The function to call when the command is used.
        name : `str`
            The command's name.
        description : `None`, `str`
            The command's description.
        
        Returns
        -------
        command_function : CommandFunction
        """
        command_function = CommandFunction(self, function, name, description)
        self._command_function = command_function
        return command_function
    
    
    def _trace_back_name(self):
        """
        Traces back to the source name of the command.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
        """
        parent_reference = self._parent_reference
        if (parent_reference is not None):
            parent = parent_reference()
            if (parent is not None):
                yield from parent._trace_back_name()
        
        name = self.name
        if (name is not None):
            yield name
    
    
    def invoke(self, parameters, index):
        """
        Calls the command line command category.
        
        Parameters
        ----------
        parameters : `list` of `str`
            Command line parameters.
        index : `int`
            The index of the first parameter trying to process.
        
        Returns
        -------
        command_result : ``CommandResult``
        """
        command_categories = self._command_categories
        if (command_categories is None):
            command_function = self._command_function
            if (command_function is None):
                return CommandResult(
                    COMMAND_RESULT_CODE_CATEGORY_EMPTY,
                    self,
                )
            
            else:
                return command_function.invoke(parameters, index)
        
        else:
            if index >= len(parameters):
                command_function = self._command_function
                if (command_function is None):
                    return CommandResult(
                        COMMAND_RESULT_CODE_CATEGORY_REQUIRES_PARAMETER,
                        self,
                    )
                else:
                    return command_function(parameters, index)
            
            command_name = parameters[index]
            command_name = normalize_command_name(command_name)
            
            try:
                command_category = command_categories[command_name]
            except KeyError:
                command_function = self._command_function
                if (command_function is None):
                    return CommandResult(
                        COMMAND_RESULT_CODE_CATEGORY_UNKNOWN_SUB_COMMAND,
                        self,
                        command_name,
                    )
                else:
                    return command_function.invoke(parameters, index)
            
            else:
                return command_category.invoke(parameters, index + 1)
