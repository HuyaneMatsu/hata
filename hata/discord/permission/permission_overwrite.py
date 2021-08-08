__all__ = ('PermissionOverwrite', )

from ...backend.export import include
from ..permission import Permission
from .utils import get_permission_overwrite_key_value, PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY
from .preinstanced import PermissionOverwriteTargetType

create_partial_role_from_id = include('create_partial_role_from_id')
create_partial_user_from_id = include('create_partial_user_from_id')
Role = include('Role')

PERMISSION_OVERWRITE_TYPE_ROLE = PermissionOverwriteTargetType.role
PERMISSION_OVERWRITE_TYPE_USER = PermissionOverwriteTargetType.user

class PermissionOverwrite:
    """
    Represents a permission overwrite of a guild channel.
    
    Attributes
    ----------
    allow : ``Permission``
        The allowed permissions by the overwrite.
    deny : ``Permission``
        The denied permission by the overwrite.
    target_id : `int`
        The permission overwrites target's identifier.
    target_type : ``PermissionOverwriteTargetType``
        The permission overwrite's target's type.

    target_role : `None`, ``Role`` or ``Unknown``
        The target role entity of the overwrite if applicable. Defaults to `None`.
    target_user_id : `int`
        The target user id of the overwrite if applicable. Defaults to `0`.
    """
    __slots__ = ('allow', 'deny', 'target_id', 'target_type')
    
    def __init__(self, data):
        """
        Creates a permission overwrite from the given data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        """
        self.target_id = int(data['id'])
        self.target_type = PermissionOverwriteTargetType.get(get_permission_overwrite_key_value(data))
        self.allow = Permission(data[PERMISSION_ALLOW_KEY])
        self.deny = Permission(data[PERMISSION_DENY_KEY])
    
    @property
    def target(self):
        """
        Returns the target entity of the overwrite.
        
        Returns
        -------
        target : ``ClientUserBase``, ``Role``, `None`
        """
        target_type = self.target_type
        target_id = self.target_id
        
        if target_type is PERMISSION_OVERWRITE_TYPE_ROLE:
            target = create_partial_role_from_id(target_id)
        
        elif target_type is PERMISSION_OVERWRITE_TYPE_USER:
            target = create_partial_user_from_id(target_id)
        
        else:
            target = None
        
        return target
    
    
    @classmethod
    def custom(cls, target, allow, deny):
        """
        Creates an overwrite object with the given parameters.
        
        Parameters
        ----------
        target : ``Role`` or ``UserBase`` instance
            The target entity of the overwrite.
        allow : `int`
            The allowed permissions by the overwrite.
        deny : `int`
            The denied permission by the overwrite.
        
        Returns
        -------
        self : ``PermissionOverwrite``
        """
        target_id = target.id
        if isinstance(target, Role):
            target_type = PERMISSION_OVERWRITE_TYPE_ROLE
        else:
            target_type = PERMISSION_OVERWRITE_TYPE_USER
        
        self = object.__new__(cls)
        self.target_id = target_id
        self.target_type = target_type
        self.allow = Permission(allow)
        self.deny = Permission(deny)
        return self
    
    def __hash__(self):
        """Returns the permission overwrite's hash."""
        return self.target_id^self.allow^self.deny^(self.target_type.value<<16)
    
    def __repr__(self):
        """Returns the permission overwrite's representation."""
        return f'<{self.__class__.__name__} target={self.target!r}>'
    
    def keys(self):
        """
        Yields the permissions' names.
        
        This method is a generator.
        
        Yields
        ------
        name : `str`
            Permissions' respective name.
        """
        yield from Permission.__keys__.keys()
    
    def values(self):
        """
        Yields position by position each permission's state. `+1` is yielded if the permission is enabled, `-1` if
        disabled and `0` if neither.
        
        This method is a generator.
        
        Yields
        ------
        state : `int`
            The permission's state.
            
            Can be one of the following:
            
            +-----------+-------+
            | Name      | Value |
            +===========+=======+
            | Enabled   | +1    |
            +-----------+-------+
            | None      | 0     |
            +-----------+-------+
            | Disabled  | -1    |
            +-----------+-------+
        """
        allow = self.allow
        deny = self.deny
        for index in Permission.__keys__.values():
            if (allow>>index)&1:
                state = +1
            elif (deny>>index)&1:
                state = -1
            else:
                state = 0
            
            yield state
    
    def items(self):
        """
        Yields the permission overwrite's items. What includes their name and their state. As state `+1` is yielded
        if the permission is enabled, `-1` if disabled and `0` if neither.
        
        This method is a generator.
        
        Yields
        -------
        name : `str`
            Permissions' respective name.
        state : `int`
            The permission's state.
            
            Can be one of the following:
            
            +-----------+-------+
            | Name      | Value |
            +===========+=======+
            | Enabled   | +1    |
            +-----------+-------+
            | None      | 0     |
            +-----------+-------+
            | Disabled  | -1    |
            +-----------+-------+
        """
        allow = self.allow
        deny = self.deny
        for key, index in Permission.__keys__.items():
            if (allow>>index)&1:
                state = +1
            elif (deny>>index)&1:
                state = -1
            else:
                state = 0
            
            yield key, state
    
    
    def __getitem__(self, key):
        """Returns the permission's state for the given permission name."""
        index = Permission.__keys__[key]
        if (self.allow>>index)&1:
            state = +1
        elif (self.deny>>index)&1:
            state = -1
        else:
            state = 0
        
        return state
    
    
    def __lt__(self, other):
        """Returns whether is this permission overwrite is at lower position in ordering than the order."""
        if type(self) is not type(other):
            return NotImplemented
        
        target_type = self.target_type
        if target_type is PERMISSION_OVERWRITE_TYPE_USER:
            self_target_type_sort_value = 0
        
        elif target_type is PERMISSION_OVERWRITE_TYPE_ROLE:
            self_target_type_sort_value = 1
        
        else:
            self_target_type_sort_value = 2
        

        target_type = other.target_type
        if target_type is PERMISSION_OVERWRITE_TYPE_USER:
            other_target_type_sort_value = 0
        
        elif target_type is PERMISSION_OVERWRITE_TYPE_ROLE:
            other_target_type_sort_value = 1
        
        else:
            other_target_type_sort_value = 2
        
        
        if self_target_type_sort_value < other_target_type_sort_value:
            return True
        
        if self_target_type_sort_value == other_target_type_sort_value:
            if self.target_id < other.target_id:
                return True
            
            return False
        
        return False
    
    
    def __eq__(self, other):
        """Returns whether is this permission overwrite is same as the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.allow != other.allow:
            return False
        
        if self.deny != other.deny:
            return False
        
        if self.target_id != other.target_id:
            return False
        
        return True
    
    
    def __gt__(self, other):
        """Returns whether is this permission overwrite is at greater position in ordering than the order."""
        if type(self) is not type(other):
            return NotImplemented
        
        target_type = self.target_type
        if target_type is PERMISSION_OVERWRITE_TYPE_USER:
            self_target_type_sort_value = 0
        
        elif target_type is PERMISSION_OVERWRITE_TYPE_ROLE:
            self_target_type_sort_value = 1
        
        else:
            self_target_type_sort_value = 2
        

        target_type = other.target_type
        if target_type is PERMISSION_OVERWRITE_TYPE_USER:
            other_target_type_sort_value = 0
        
        elif target_type is PERMISSION_OVERWRITE_TYPE_ROLE:
            other_target_type_sort_value = 1
        
        else:
            other_target_type_sort_value = 2
        
        
        if self_target_type_sort_value > other_target_type_sort_value:
            return True
        
        if self_target_type_sort_value == other_target_type_sort_value:
            if self.target_id > other.target_id:
                return True
            
            return False
        
        return False
