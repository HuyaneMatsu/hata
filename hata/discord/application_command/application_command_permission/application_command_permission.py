__all__ = ('ApplicationCommandPermission',)

import warnings

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_application_command_id, parse_application_id, parse_guild_id, parse_permission_overwrites,
    put_application_command_id_into, put_application_id_into, put_guild_id_into, put_permission_overwrites_into,
    validate_application_command_id, validate_permission_overwrites
)


class ApplicationCommandPermission(RichAttributeErrorBaseType):
    """
    Stores am ``ApplicationCommand``'s overwrites.
    
    Attributes
    ----------
    application_command_id : `int`
        The identifier of the respective ``ApplicationCommand``.
    
    application_id : `int`
        The application command's application's identifier.
    
    guild_id : `int`
        The identifier of the respective guild.
    
    permission_overwrites : `None`, `list` of ``ApplicationCommandPermissionOverwrite``
        The application command permissions overwrites relating to the respective application command in the guild.
    """
    __slots__ = ('application_command_id', 'application_id', 'guild_id', 'permission_overwrites')
    
    def __new__(cls, application_command_id, *, permission_overwrites = ...):
        """
        Creates a new ``ApplicationCommandPermission`` from the given parameters.
        
        Parameters
        ----------
        application_command_id : ``ApplicationCommand``, `int`
            The application command's identifier.
        
        permission_overwrites : `None`, `iterable` of ``ApplicationCommandPermissionOverwrite`, Optional (Keyword only)
            Overwrites for the application command.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # application_command
        application_command_id = validate_application_command_id(application_command_id)
        
        # application_id
        # Internal attribute
        
        # guild_id
        # Internal attribute
        
        # permission_overwrites
        if permission_overwrites is ...:
            permission_overwrites = None
        else:
            permission_overwrites = validate_permission_overwrites(permission_overwrites)
        
        self = object.__new__(cls)
        self.application_command_id = application_command_id
        self.application_id = 0
        self.guild_id = 0
        self.permission_overwrites = permission_overwrites
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandPermission``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application command data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.application_command_id = parse_application_command_id(data)
        self.application_id = parse_application_id(data)
        self.guild_id = parse_guild_id(data)
        self.permission_overwrites = parse_permission_overwrites(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the application command permission to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_application_command_id_into(self.application_command_id, data, defaults)
        put_permission_overwrites_into(self.permission_overwrites, data, defaults)
        
        if include_internals:
            put_application_id_into(self.application_id, data, defaults)
            put_guild_id_into(self.guild_id, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the application command permission's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # application_command_id
        repr_parts.append(' application_command_id = ')
        repr_parts.append(repr(self.application_command_id))
        
        # application_id
        # Unique by application_command_id
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # permission_overwrites
        permission_overwrites = self.permission_overwrites
        if permission_overwrites is None:
            permission_overwrite_count = '0'
        else:
            permission_overwrite_count = repr(len(permission_overwrites))
        repr_parts.append(', permission overwrite count: ')
        repr_parts.append(permission_overwrite_count)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two application command permission's are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # application_command_id
        if self.application_command_id != other.application_command_id:
            return False
        
        # application_id
        # Unique by application_command_id
        
        # guild_id
        # Unique by application_command_id
        
        # permission_overwrites
        if self.permission_overwrites != other.permission_overwrites:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the application command overwrite's hash value."""
        hash_value = 0
        
        # application_command_id
        hash_value ^= self.application_command_id
        
        # application_id
        # Unique by application_command_id
        
        # guild_id
        # Unique by application_command_id
        
        # permission_overwrites
        permission_overwrites = self.permission_overwrites
        if (permission_overwrites is not None):
            hash_value ^= len(permission_overwrites) << 4
            
            for permission_overwrite in permission_overwrites:
                hash_value ^= hash(permission_overwrite)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the application command permission.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # application_command_id
        new.application_command_id = self.application_command_id
        
        # application_id
        new.application_id = 0
        
        # guild_id
        new.guild_id = 0
        
        # permission_overwrites
        permission_overwrites = self.permission_overwrites
        if (permission_overwrites is not None):
            permission_overwrites = (*permission_overwrites,)
        new.permission_overwrites = permission_overwrites
        
        return new
    
    
    def copy_with(self, application_command_id = ..., permission_overwrites = ...):
        """
        Copies the application command permission with the given fields.
        
        Parameters
        ----------
        application_command_id : ``ApplicationCommand``, `int`, Optional (Keyword only)
            The application command's identifier.
        
        permission_overwrites : `None`, `iterable` of ``ApplicationCommandPermissionOverwrite`, Optional (Keyword only)
            Overwrites for the application command.
            
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        if application_command_id is ...:
            application_command_id = self.application_command_id
        else:
            application_command_id = validate_application_command_id(application_command_id)
        
        if permission_overwrites is ...:
            permission_overwrites = self.permission_overwrites
            if (permission_overwrites is not None):
                permission_overwrites = (*permission_overwrites,)
        else:
            permission_overwrites = validate_permission_overwrites(permission_overwrites)
        
        new = object.__new__(type(self))
        new.application_command_id = application_command_id
        new.application_id = 0
        new.guild_id = 0
        new.permission_overwrites = permission_overwrites
        return new
    
    
    def iter_permission_overwrites(self):
        """
        Iterates over the permission overwrites of the application command permission.
        
        This method is an iterable generator.
        
        Yields
        ------
        permission_overwrite : ``ApplicationCommandPermissionOverwrite``
        """
        permission_overwrites = self.permission_overwrites
        if (permission_overwrites is not None):
            yield from permission_overwrites
    
    
    def add_permission_overwrite(self, permission_overwrite):
        """
        Deprecated and will be removed in 2023 Jun.
        """
        warnings.warn(
            (
                f'{self.__class__.__name__} is deprecated and will be removed in 2023 Jun.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
