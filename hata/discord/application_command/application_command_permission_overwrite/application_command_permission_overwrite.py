__all__ = ('ApplicationCommandPermissionOverwrite',)

from scarletio import RichAttributeErrorBaseType

from ...channel import ChannelType, create_partial_channel_from_id
from ...core import CHANNELS, ROLES
from ...role import create_partial_role_from_id
from ...user import create_partial_user_from_id

from .fields import (
    parse_allow, parse_target_id, parse_target_type, put_allow_into, put_target_id_into, put_target_type_into,
    validate_allow
)
from .helpers import validate_application_command_permission_overwrite_target
from .preinstanced import ApplicationCommandPermissionOverwriteTargetType


APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER = ApplicationCommandPermissionOverwriteTargetType.user
APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE = ApplicationCommandPermissionOverwriteTargetType.role
APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL = ApplicationCommandPermissionOverwriteTargetType.channel


class ApplicationCommandPermissionOverwrite(RichAttributeErrorBaseType):
    """
    Represents an application command's allow/disallow overwrite for the given entity.
    
    Attributes
    ----------
    allow : `bool`
        Whether the respective command is allowed for the represented entity.
    
    target_id : `int`
        The represented entity's identifier.
    
    target_type : ``ApplicationCommandPermissionOverwriteTargetType``
        The target entity's type.
    """
    __slots__ = ('allow', 'target_id', 'target_type')
    
    def __new__(cls, target, allow):
        """
        Creates a new application command permission overwrite with the given parameters.
        
        Parameters
        ----------
        target : ``ClientUserBase``, ``Role``, ``Channel``, `tuple` ((``ClientUserBase``, ``Role``, \
                ``Channel``, `str` (`'Role'`, `'role'`, `'User'`, `'user'`, `'Channel'`, `'channel'`, \
                ``ApplicationCommandPermissionOverwriteTargetType``, `int`)), `int`)
            The target entity of the application command permission overwrite.
            
            The expected type & value might be pretty confusing, but the target was it to allow relaxing creation.
            To avoid confusing, here is a list of the expected structures:
            
            - ``Role``
            - ``ClientUserBase``
            - ``Channel``
            - `tuple` (``Role``, `int`)
            - `tuple` (``ClientUserBase``, `int`)
            - `tuple` (``Channel``, `int`)
            - `tuple` (`'Role'`, `int`)
            - `tuple` (`'role'`, `int`)
            - `tuple` (`'User'`, `int`)
            - `tuple` (`'user'`, `int`)
            - `tuple` (`'Channel'`, `int`)
            - `tuple` (`'channel'`, `int`)
            - `tuple` (``ApplicationCommandPermissionOverwriteTargetType``, `int`)
            - `tuple` (`int`, `int`)
        
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        AssertionError
            - If a parameter's value is incorrect.
        """
        # allow
        allow = validate_allow(allow)
        
        # target_id & target_type
        target_type, target_id = validate_application_command_permission_overwrite_target(target)
        
        self = object.__new__(cls)
        self.allow = allow
        self.target_id = target_id
        self.target_type = target_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``ApplicationCommandPermissionOverwrite`` from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            The received application command permission overwrite data.
        
        Returns
        -------
        self : `instance<cls>`
            The created application command option.
        """
        self = object.__new__(cls)
        self.allow = parse_allow(data)
        self.target_id = parse_target_id(data)
        self.target_type = parse_target_type(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the application command permission overwrite to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_allow_into(self.allow, data, defaults)
        put_target_id_into(self.target_id, data, defaults)
        put_target_type_into(self.target_type, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the application command permission overwrite's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # Primary fields: `.target_type`, `.target_id`
        repr_parts.append(' target_type = ')
        repr_parts.append(self.target_type.name)
        
        repr_parts.append(', target_id = ')
        repr_parts.append(repr(self.target_id))
        
        # Secondary fields: `.allow`
        repr_parts.append(', allow = ')
        repr_parts.append(repr(self.allow))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two application command overwrites are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # allow
        if self.allow != other.allow:
            return False
        
        # target_id
        if self.target_id != other.target_id:
            return False
        
        # target_type
        if self.target_type is not other.target_type:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the application command permission overwrite's hash value."""
        hash_value = 0
        
        # allow
        hash_value ^= self.allow << 8
        
        # target_id
        hash_value ^= self.target_id
        
        # target_type
        hash_value ^= self.target_type.value
        
        return hash_value
    
    
    def __gt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_type_value = self.target_type.value
        other_type_value = other.target_type.value
        
        if self_type_value > other_type_value:
            return True
        
        if self_type_value < other_type_value:
            return False
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE.value:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_role = ROLES.get(self_target_id, None)
            other_role = ROLES.get(other_target_id, None)
            if self_role is None:
                if other_role is None:
                    return (self_target_id > other_target_id)
                else:
                    return False
            else:
                if other_role is None:
                    return True
                else:
                    return (self_role > other_role)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER.value:
            return (self.target_id > other.target_id)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL.value:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_channel = CHANNELS.get(self_target_id, None)
            other_channel = CHANNELS.get(other_target_id, None)
            if self_channel is None:
                if other_channel is None:
                    return (self_target_id > other_target_id)
                else:
                    return False
            else:
                if other_channel is None:
                    return True
                else:
                    return (self_channel.name > other_channel.name)
        
        # Should not happen
        return False
    
    
    def __lt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_type_value = self.target_type.value
        other_type_value = other.target_type.value
        
        if self_type_value > other_type_value:
            return False
        
        if self_type_value < other_type_value:
            return True
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE.value:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_role = ROLES.get(self_target_id, None)
            other_role = ROLES.get(other_target_id, None)
            if self_role is None:
                if other_role is None:
                    return (self_target_id < other_target_id)
                else:
                    return True
            else:
                if other_role is None:
                    return False
                else:
                    return (self_role < other_role)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER.value:
            return (self.target_id < other.target_id)
        
        if self_type_value == APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL.value:
            self_target_id = self.target_id
            other_target_id = other.target_id
            
            self_channel = CHANNELS.get(self_target_id, None)
            other_channel = CHANNELS.get(other_target_id, None)
            if self_channel is None:
                if other_channel is None:
                    return (self_target_id < other_target_id)
                else:
                    return True
            else:
                if other_channel is None:
                    return False
                else:
                    return (self_channel.name < other_channel.name)
        
        # Should not happen
        return True
    
    
    def copy(self):
        """
        Copies the application command permission overwrite.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # allow
        new.allow = self.allow
        
        # target_id
        new.target_id = self.target_id
        
        # target_type
        new.target_type = self.target_type
        
        return new
    
    
    
    def copy_with(self, *, allow = ..., target = ...,):
        """
        Copies the application command permission overwrite with modifying the given parameters inside of it.
        
        Parameters
        ----------
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        
        target : ``ClientUserBase``, ``Role``, ``Channel``, `tuple` ((``ClientUserBase``, ``Role``, \
                ``Channel``, `str` (`'Role'`, `'role'`, `'User'`, `'user'`, `'Channel'`, `'channel'`, \
                ``ApplicationCommandPermissionOverwriteTargetType``, `int`)), `int`)
            The target entity of the application command permission overwrite.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        AssertionError
            - If a parameter's value is incorrect.
        """
        # allow
        if allow is ...:
            allow = self.allow
        else:
            allow = validate_allow(allow)
        
        if target is ...:
            target_id = self.target_id
            target_type = self.target_type
        else:
            target_type, target_id = validate_application_command_permission_overwrite_target(target)
        
        new = object.__new__(type(self))
        new.allow = allow
        new.target_id = target_id
        new.target_type = target_type
        return new
    
    
    @property
    def target(self):
        """
        Returns the application command overwrite's target entity.
        
        Returns
        -------
        target : `None`, ``Role``, ``ClientUserBase``, ``Channel``
        """
        target_type = self.target_type
        target_id = self.target_id
        
        if target_type is APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_ROLE:
            target = create_partial_role_from_id(target_id)
        
        elif target_type is APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_USER:
            target = create_partial_user_from_id(target_id)
        
        elif target_type is APPLICATION_COMMAND_PERMISSION_OVERWRITE_TARGET_TYPE_CHANNEL:
            target = create_partial_channel_from_id(target_id, ChannelType.unknown, 0)
        
        else:
            target = None
        
        return target
