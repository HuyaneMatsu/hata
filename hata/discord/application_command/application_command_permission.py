__all__ = ('ApplicationCommandPermission',)

from scarletio import RichAttributeErrorBaseType

from ..bases import maybe_snowflake

from .application_command import ApplicationCommand
from .application_command_permission_overwrite import ApplicationCommandPermissionOverwrite
from .constants import APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX


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
    
    def __new__(cls, application_command, *, permission_overwrites=None):
        """
        Creates a new ``ApplicationCommandPermission`` from the given parameters.
        
        Parameters
        ----------
        application_command : ``ApplicationCommand``, `int`
            The application command's identifier.
        
        permission_overwrites : `None`, (`list`, `set`, `tuple`) of ``ApplicationCommandPermissionOverwrite` = `None`
                , Optional (Keyword only)
            Overwrites for the application command.
        
        Raises
        ------
        TypeError
            - If `application_command` was not given neither as ``ApplicationCommand`` nor as `int`.
        AssertionError
            - If `permission_overwrites` was not give neither as `None`, `list`, `set`, `tuple`.
            - If `permission_overwrites` contains a non ``ApplicationCommandPermissionOverwrite`` element.
            - If `permission_overwrites` length is over `10`.
        """
        # application_command
        if isinstance(application_command, ApplicationCommand):
            application_command_id = application_command.id
        else:
            application_command_id = maybe_snowflake(application_command)
            if application_command_id is None:
                raise TypeError(
                    f'`application_command` can be `{ApplicationCommand.__name__}`, `int` , got '
                    f'{application_command.__class__.__name__}; {application_command!r}.'
                )
        
        # application_id
        # Internal attribute
        
        # guild_id
        # Internal attribute
        
        # permission_overwrites
        if permission_overwrites is None:
            permission_overwrites_processed = None
        
        else:
            if __debug__:
                if not isinstance(permission_overwrites, (list, set, tuple)):
                    raise AssertionError(
                        f'`permission_overwrites` can be `None`, `list`, `set`, `tuple`, got '
                        f'{permission_overwrites.__class__.__name__}; {permission_overwrites!r}.'
                    )
            
            permission_overwrites_processed = []
            
            for permission_overwrite in permission_overwrites:
                if __debug__:
                    if not isinstance(permission_overwrite, ApplicationCommandPermissionOverwrite):
                        raise AssertionError(
                            f'`permission_overwrites` contains a non '
                            f'`{ApplicationCommandPermissionOverwrite.__name__}` element, got '
                            f'{permission_overwrite.__class__.__name__}; {permission_overwrite!r}; '
                            f'permission_overwrites={permission_overwrites!r}.'
                        )
                
                permission_overwrites_processed.append(permission_overwrite)
                
            
            if permission_overwrites_processed:
                if __debug__:
                    if len(permission_overwrites_processed) >= APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX:
                        raise AssertionError(
                            f'`permission_overwrites` can have up to '
                            f'`{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX}` elements, which is already reached, '
                            f'got {permission_overwrites_processed!r}.'
                        )
            else:
                permission_overwrites_processed = None
        
        self = object.__new__(cls)
        self.application_command_id = application_command_id
        self.application_id = 0
        self.guild_id = 0
        self.permission_overwrites = permission_overwrites_processed
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandPermission``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application command data.
        
        Returns
        -------
        self : ``ApplicationCommandPermission``
        """
        # application_command_id
        application_command_id = int(data['id'])
        
        # application_id
        application_id = int(data['application_id'])
        
        # guild_id
        guild_id = int(data['guild_id'])
        
        # permission_overwrites
        permission_overwrite_datas = data['permissions']
        if permission_overwrite_datas:
            permission_overwrites = [
                ApplicationCommandPermissionOverwrite.from_data(permission_overwrite_data) for
                permission_overwrite_data in permission_overwrite_datas
            ]
            
        else:
            permission_overwrites = None
        
        
        self = object.__new__(cls)
        
        self.application_command_id = application_command_id
        self.application_id = application_id
        self.guild_id = guild_id
        self.permission_overwrites = permission_overwrites
        
        return self
    
    
    def to_data(self):
        """
        Converts the application command permission to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # application_command_id
        data['id'] = self.application_command_id
        
        # application_id
        data['application_id'] = self.application_id
        
        # guild_id
        data['guild_id'] = self.guild_id
        
        # permission_overwrites
        permission_overwrites = self.permission_overwrites
        if permission_overwrites is None:
            permission_overwrite_datas = []
        else:
            permission_overwrite_datas = [
                permission_overwrite.to_data() for permission_overwrite in permission_overwrites
            ]
        
        data['permissions'] = permission_overwrite_datas
        
        return data
    
    
    def __repr__(self):
        """Returns the application command permission's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # application_command_id
        repr_parts.append(' application_command_id=')
        repr_parts.append(repr(self.application_command_id))
        
        # application_id
        # Unique by application_command_id
        
        # guild_id
        repr_parts.append(' guild_id=')
        repr_parts.append(repr(self.guild_id))
        
        # permission_overwrites
        permission_overwrites = self.permission_overwrites
        if permission_overwrites is None:
            permission_overwrite_count = '0'
        else:
            permission_overwrite_count = repr(len(permission_overwrites))
        repr_parts.append(', permission overwrite count=')
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
        if self.guild_id != other.guild_id:
            return False
        
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
        hash_value ^= self.guild_id
        
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
        new : ``ApplicationCommandPermission``
        """
        new = object.__new__(type(self))
        
        # application_command_id
        new.application_command_id = self.application_command_id
        
        # application_id
        new.application_id = self.application_id
        
        # guild_id
        new.guild_id = self.guild_id
        
        # permission_overwrites
        permission_overwrites = self.permission_overwrites
        if (permission_overwrites is not None):
            permission_overwrites = [permission_overwrite.copy() for permission_overwrite in permission_overwrites]
        new.permission_overwrites = permission_overwrites
        
        return new
    
    
    def add_permission_overwrite(self, permission_overwrite):
        """
        Adds an application command permission overwrite to the overwrites of the application command permission.
        
        Parameters
        ----------
        permission_overwrite : ``ApplicationCommandPermissionOverwrite``
            The overwrite to add.
        
        Raises
        ------
        AssertionError
            - If `overwrite` is not ``ApplicationCommandPermissionOverwrite``.
            - If the application command permission has `10` overwrites already.
        """
        if __debug__:
            if not isinstance(permission_overwrite, ApplicationCommandPermissionOverwrite):
                raise AssertionError(
                    f'`permission_overwrite` can be {ApplicationCommandPermissionOverwrite.__name__} , got '
                    f'{permission_overwrite.__class__.__name__}; {permission_overwrite!r}.'
                )
        
        permission_overwrites = self.permission_overwrites
        if permission_overwrites is None:
            self.permission_overwrites = permission_overwrites = []
        else:
            if __debug__:
                if len(permission_overwrites) >= APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX:
                    raise AssertionError(
                        f'`permission_overwrites` can have up to '
                        f'`{APPLICATION_COMMAND_PERMISSION_OVERWRITE_MAX}` elements, which is already reached, '
                        f'got {permission_overwrite!r}.'
                    )
        
        permission_overwrites.append(permission_overwrite)
