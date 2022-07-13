__all__ = ('Command',)

from scarletio import RichAttributeErrorBaseType, WeakReferer

from ..constants import REGISTERED_COMMANDS, REGISTERED_COMMANDS_BY_NAME

from .helpers import normalize_alters, normalize_command_name
from .category import CommandCategory
from .result import COMMAND_RESULT_CODE_COMMAND_UNINITIALIZED, CommandResult


class Command(RichAttributeErrorBaseType):
    """
    Represents a command line command.
    
    Attributes
    ----------
    _command_category : `None`, ``CommandCategory``
        Command category of the command.
    _self_reference : `None`, ``WeakReferer``
        Reference to itself.
    alters : `None`, `set` of `str`
        Alternative names for the command.
    description : `None`, `str`
        Command description.
    name : `str`
        The command's name.
    """
    __slots__ = ('__weakref__', '_command_category', '_self_reference', 'alters', 'description', 'name')
    
    
    def __new__(cls, name, description, alters):
        """
        Creates a new command line command.
        
        Parameters
        ----------
        name : `str`
            The command's name.
        description : `str`
            The command's description message.
        alters : `None`, `str`, `iterable` of `str`
            Alternative names for the command.
        
        Raises
        ------
        TypeError
            Type of `alters` is unaccepted.
        """
        name = normalize_command_name(name)
        alters = normalize_alters(alters, name)
        
        self = object.__new__(cls)
        self._command_category = None
        self.alters = alters
        self.name = name
        self.description = None
        self._self_reference = None
        
        self._self_reference = WeakReferer(self)
        self._command_category = CommandCategory(self, '')
        
        REGISTERED_COMMANDS.add(self)
        REGISTERED_COMMANDS_BY_NAME[name] = self
        
        if (alters is not None):
            for alter in alters:
                REGISTERED_COMMANDS_BY_NAME.setdefault(alter, self)
        
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
        return self._command_category.register_command_category(name)
    
    
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
        command_function : ``CommandFunction``
        """
        return self._command_category.register_command_function(function, name, description)
    
    
    def invoke(self, parameters, index):
        """
        Calls the command line command.
        
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
        command_category = self._command_category
        if (command_category is None):
            return CommandResult(
                COMMAND_RESULT_CODE_COMMAND_UNINITIALIZED,
                self,
            )
        else:
            return command_category.invoke(parameters, index)
    
    
    def _trace_back_name(self):
        """
        Traces back to the source name of the command.
        
        This method is an iterable generator.
        
        Yields
        ------
        name : `str`
        """
        yield self.name
    
    
    def get_usage(self):
        """
        Returns teh usage of the command.
        
        TODO
        
        Returns
        -------
        usage : `str`
        """
        return ''
