__all__ = ('Command',)

import warnings

from scarletio import RichAttributeErrorBaseType

from .constants import COMMAND_IMPORT_ROUTE, COMMANDS, COMMAND_NAME_TO_COMMAND


class Command(RichAttributeErrorBaseType):
    """
    Command class for command lookup.
    
    Attributes
    ----------
    alters : `None` or `frozenset` of `str`
        Alternative names of the command.
    description : `str`
        The command's description.
    file_name : `str`
        The command's file's name.
    diretcory_name : `str`
        The command's diretcory_name.
    name : `str`
        The command's name.
    usage : `str`
        The command's usage.
    """
    __slots__ = ('alters', 'description', 'file_name', 'diretcory_name', 'name', 'usage')
    
    def __new__(cls, diretcory_name, file_name, name, alters, usage, description):
        """
        Parameters
        ----------
        diretcory_name : `str`
            The command's diretcory_name.
        file_name : `str`
            The command's file's name.
        name : `str`
            The command's name.
        alters : `None` or `list` of `str`
            Alternative names of the command.
        usage : `str`
            The command's usage.
        description : `str`
            The command's description.
        """
        if file_name.endswith('.py'):
            file_name = file_name[:-3]
        
        if (alters is not None):
            if alters:
                alters = frozenset(alters)
            else:
                alters = None
        
        self = object.__new__(cls)
        self.alters = alters
        self.description = description
        self.file_name = file_name
        self.diretcory_name = diretcory_name
        self.name = name
        self.usage = usage
        
        COMMANDS.add(self)
        
        try:
            old_command = COMMAND_NAME_TO_COMMAND[name]
        except KeyError:
            pass
        else:
            if old_command.name == name:
                warnings.warn(
                    RuntimeError,
                    (
                        f'Multiple commands with name: {name}\n'
                        f'- {old_command.diretcory_name}.{old_command.name}\n'
                        f'- {diretcory_name}.{name}'
                    ),
                )
        
        COMMAND_NAME_TO_COMMAND[name] = self
        if (alters is not None):
            for alter in alters:
                COMMAND_NAME_TO_COMMAND.setdefault(alter, self)
        
        return self
    
    
    def __hash__(self):
        """Returns the command's hash value."""
        hash_value = 0
        
        # alters
        alters = self.alters
        if (alters is not None):
            hash_value ^= hash(alters)
        
        # description
        hash_value ^= hash(self.description)
        
        # file_name
        file_name = self.file_name
        try:
            file_name_hash_value = hash(file_name)
        except (NotImplementedError, RuntimeError, TypeError):
            file_name_hash_value = object.__hash__(file_name)
        hash_value ^= file_name_hash_value
        
        # diretcory_name
        hash_value ^= hash(self.diretcory_name)
        
        # name
        hash_value ^= hash(self.name)
        
        # usage
        hash_value ^= hash(self.usage)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two commands are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # alters
        if self.alters != other.alters:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # file_name
        if self.file_name != other.file_name:
            return False
        
        # diretcory_name
        if self.diretcory_name != other.diretcory_name:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # usage
        if self.usage != other.usage:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the command's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' ')
        repr_parts.append(self.name)
        repr_parts.append(' from ')
        
        repr_parts.append(self.diretcory_name)
        repr_parts.append('.')
        repr_parts.append(self.file_name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_command_function(self):
        """
        Returns the command function of the command.
        
        Returns
        -------
        command_function : `FunctionType`
        """
        access_path_parts = [*COMMAND_IMPORT_ROUTE, self.diretcory_name, self.file_name]
        module = __import__('.'.join(access_path_parts))
        
        for access_path_part in access_path_parts[1:]:
            module = getattr(module, access_path_part)
        
        return module.__main__
