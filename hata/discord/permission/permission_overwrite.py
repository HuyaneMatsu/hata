__all__ = ('PermissionOverwrite', )

from ...backend.export import include
from ..permission import Permission
from .utils import get_permission_overwrite_key_value, PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY
from .preinstanced import PermissionOverwriteTargetType

create_partial_role_from_id = include('create_partial_role_from_id')
create_partial_user_from_id = include('create_partial_user_from_id')
Role = include('Role')

PERMISSION_OVERWRITE_TYPE_ROLE_VALUE = PermissionOverwriteTargetType.role.value

class PermissionOverwrite:
    """
    Represents a permission overwrite of a guild channel.
    
    Attributes
    ----------
    allow : ``Permission``
        The allowed permissions by the overwrite.
    deny : ``Permission``
        The denied permission by the overwrite.
    target_role : `None`, ``Role`` or ``Unknown``
        The target role entity of the overwrite if applicable. Defaults to `None`.
    target_user_id : `int`
        The target user id of the overwrite if applicable. Defaults to `0`.
    """
    __slots__ = ('allow', 'deny', 'target_role', 'target_user_id')
    
    def __init__(self, data):
        """
        Creates a permission overwrite from the given data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        """
        id_ = int(data['id'])
        if get_permission_overwrite_key_value(data) == PERMISSION_OVERWRITE_TYPE_ROLE_VALUE:
            target_role = create_partial_role_from_id(id_)
            target_user_id = 0
        else:
            target_role = None
            target_user_id = id_
        
        self.target_role = target_role
        self.target_user_id = target_user_id
        self.allow = Permission(data[PERMISSION_ALLOW_KEY])
        self.deny = Permission(data[PERMISSION_DENY_KEY])
    
    @property
    def target(self):
        """
        Returns the target entity of the overwrite.
        
        Returns
        -------
        target : ``ClientUserBase`` or ``Role``
        """
        target = self.target_role
        if target is None:
            target = create_partial_user_from_id(self.target_user_id)
        
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
        if isinstance(target, Role):
            target_role = target
            target_user_id = 0
        else:
            target_role = None
            target_user_id = target.id
        
        self = object.__new__(cls)
        self.target_role = target_role
        self.target_user_id = target_user_id
        self.allow = Permission(allow)
        self.deny = Permission(deny)
        return self
    
    def __hash__(self):
        """Returns the permission overwrite's hash."""
        return self.target.id^self.allow^self.deny
    
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
    
    __iter__ = keys
    
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
        name : str`
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
    
    @property
    def type(self):
        """
        Returns the Discord side identifier value permission overwrite.
        
        Returns
        -------
        type_ : ``Per`
            Can be either `'role'` or `'member'`
        """
        if self.target_role is None:
            type_ = PermissionOverwriteTargetType.user
        else:
            type_ = PermissionOverwriteTargetType.role
        
        return type_
    
    @property
    def id(self):
        """
        Returns the permission overwrite's target's id.
        
        Returns
        -------
        id_ : `int`
        """
        target_role = self.target_role
        if target_role is None:
            id_ = self.target_user_id
        else:
            id_ = target_role.id
        
        return id_
    
    def __lt__(self, other):
        """Returns whether is this permission overwrite is at lower position in ordering than the order."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_target_role = self.target_role
        if self_target_role is None:
            self_target_type = 0
            self_target_id = self.target_user_id
        else:
            self_target_type = 1
            self_target_id = self_target_role.id
        
        other_target_role = other.target_role
        if other_target_role is None:
            other_target_type = 0
            other_target_id = other.target_user_id
        else:
            other_target_type = 1
            other_target_id = other_target_role.id
        
        if self_target_type < other_target_type:
            return True
        
        if self_target_type == other_target_type:
            if self_target_id < other_target_id:
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
        
        self_target_role = self.target_role
        if self_target_role is None:
            self_target_id = self.target_user_id
        else:
            self_target_id = self_target_role.id
        
        other_target_role = other.target_role
        if other_target_role is None:
            other_target_id = other.target_user_id
        else:
            other_target_id = other_target_role.id
        
        if self_target_id != other_target_id:
            return False
        
        return True
    
    def __gt__(self, other):
        """Returns whether is this permission overwrite is at greater position in ordering than the order."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_target_role = self.target_role
        if self_target_role is None:
            self_target_type = 0
            self_target_id = self.target_user_id
        else:
            self_target_type = 1
            self_target_id = self_target_role.id
            
        other_target_role = other.target_role
        if other_target_role is None:
            other_target_type = 0
            other_target_id = other.target_user_id
        else:
            other_target_type = 1
            other_target_id = other_target_role.id
        
        if self_target_type > other_target_type:
            return True
        
        if self_target_type == other_target_type:
            if self_target_id > other_target_id:
                return True
            
            return False
        
        return False
