__all__ = ('Command',)

from scarletio import RichAttributeErrorBaseType, WeakReferer

from ..constants import REGISTERED_COMMANDS, REGISTERED_COMMANDS_BY_NAME

from .helpers import normalize_aliases, normalize_command_name
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
    aliases : `None`, `set` of `str`
        Alternative names for the command.
    available : `bool`
        Whether the command is available.
    name : `str`
        The command's name.
    """
    __slots__ = ('__weakref__', '_command_category', '_self_reference', 'aliases', 'available', 'name')
    
    def __new__(cls, name, aliases, available):
        """
        Creates a new command line command.
        
        Parameters
        ----------
        name : `str`
            The command's name.
        aliases : `None`, `str`, `iterable` of `str`
            Alternative names for the command.
        available : `bool`
            Whether the command is available.
        
        Raises
        ------
        TypeError
            Type of `aliases` is unaccepted.
        """
        name = normalize_command_name(name)
        aliases = normalize_aliases(aliases, name)
        
        self = object.__new__(cls)
        self._command_category = None
        self.aliases = aliases
        self.available = available
        self.name = name
        self._self_reference = None
        
        self._self_reference = WeakReferer(self)
        self._command_category = CommandCategory(self, None)
        
        REGISTERED_COMMANDS.add(self)
        
        names = [name]
        if (aliases is not None):
            names.extend(aliases)
        
        for name_ in names:
            
            try:
                already_registered_command = REGISTERED_COMMANDS_BY_NAME[name_]
            except KeyError:
                pass
            else:
                already_registered_command._unregister_name(name_)
            
            REGISTERED_COMMANDS_BY_NAME[name_] = self
        
        return self
    
    
    def __repr__(self):
        """Returns the command's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        command_category = self._command_category
        if (command_category is not None):
            repr_parts.append(', command_category = ')
            repr_parts.append(repr(command_category))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
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
        
        Returns
        -------
        name : `str`
        """
        name = self.name
        yield name
        return name
    
    
    def get_direct_usage(self, *sub_command_stack):
        """
        Returns the direct usage of the command for the given sub-command stack.
        
        Parameters
        ----------
        *sub_command_stack : `str`
            Sub command stack to get the direct usage for.
        
        Returns
        -------
        usage : `str`
        """
        return ''.join(self.render_direct_usage_into([], *sub_command_stack))
    
    
    def render_direct_usage_into(self, into, *sub_command_stack):
        """
        Renders the direct usage of the command for the given sub-command stack.
        
        Parameters
        ----------
        into : `list` of `str`
            The list to render the usage into.
        *sub_command_stack : `str`
            Sub command stack to get the direct usage for.
        
        Returns
        -------
        into : `list` of `str`
        """
        return self._command_category.render_direct_usage_into(into, *sub_command_stack)
    
    
    def iter_command_functions(self, *, sort = False):
        """
        Iterates over the command functions of the command category.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        sort : `bool` = `False`, Optional (Keyword only)
            Whether the commands should be iterated in a sorted way.
        
        Yields
        ------
        command_function : ``CommandFunction``
        """
        yield from self._command_category.iter_command_functions(sort = sort)
    
    
    def _unregister_name(self, name):
        """
        Unregisters the command for the given name.
        
        Parameters
        ----------
        name : `str`
            The name to unregister.
        """
        if self.name == name:
            self._unregister()
        else:
            self._unregister_alter(name)
    
    
    def _unregister(self):
        """
        Unregisters the command. Fully.
        """
        REGISTERED_COMMANDS.discard(self)
        
        names = [self.name]
        aliases = self.aliases
        if (aliases is not None):
            names.extend(aliases)
        
        for name in names:
            if REGISTERED_COMMANDS_BY_NAME.get(name) is self:
                del REGISTERED_COMMANDS_BY_NAME[name]
    
    
    def _unregister_alter(self, name):
        """
        Removes an alternative name of the command.
        
        Parameters
        ----------
        name : `str`
            The alternative name to unregister.
        """
        if REGISTERED_COMMANDS_BY_NAME.get(name) is self:
            del REGISTERED_COMMANDS_BY_NAME[name]
        
        aliases = self.aliases
        try:
            aliases.remove(name)
        except KeyError:
            pass
        else:
            if not aliases:
                self.aliases = None
