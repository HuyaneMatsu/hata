__all__ = ('PermissionOverwrite', )

from scarletio import RichAttributeErrorBaseType, include

from ..bases import maybe_snowflake
from ..permission import Permission
from ..preconverters import preconvert_preinstanced_type

from .preinstanced import PermissionOverwriteTargetType
from .utils import PERMISSION_ALLOW_KEY, PERMISSION_DENY_KEY, get_permission_overwrite_key_value


create_partial_role_from_id = include('create_partial_role_from_id')
create_partial_user_from_id = include('create_partial_user_from_id')

Role = include('Role')
ClientUserBase = include('ClientUserBase')

PERMISSION_OVERWRITE_TYPE_ROLE = PermissionOverwriteTargetType.role
PERMISSION_OVERWRITE_TYPE_USER = PermissionOverwriteTargetType.user


class PermissionOverwrite(RichAttributeErrorBaseType):
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
    """
    __slots__ = ('allow', 'deny', 'target_id', 'target_type')
    
    def __new__(cls, target_id, *, target_type=None, allow=None, deny=None):
        """
        Parameters
        ----------
        target_id : `int`, ``Role``, ``ClientUserBase``
            The permission overwrite's target.
        target_type : `None`, ``PermissionOverwriteTargetType`` = `None`, Optional (Keyword only)
            The permission overwrite's target's type. Required if `target_id` is given as a snowflake.
        allow : `None`, ``Permission``, `int` = `None`, Optional (Keyword only)
            The permission overwrite's allowed permission's value.
        deny : `None`, ``Permission``, `int` = `None`, Optional (Keyword only)
            The permission overwrite's denied permission's value.
        
        Raises
        ------
        TypeError
            - If `target_id` is not `int`, ``Role``, ``ClientUserBase``.
            - If `allow` is not `None`, `int`, ``Permission``.
            - If `deny` is not `None`, `int`, ``Permission``.
            - If `target_type` is not `None`, ``PermissionOverwriteTargetType``.
        ValueError
            - `target_type` not given and it cannot be detected from `target_id`.
            - `target_type` is different than the one defined by the `target_id` parameter.
        """
        # target_id
        if isinstance(target_id, Role):
            target_id_processed = target_id.id
            target_type_processed = PERMISSION_OVERWRITE_TYPE_ROLE
        
        elif isinstance(target_id, ClientUserBase):
            target_id_processed = target_id.id
            target_type_processed = PERMISSION_OVERWRITE_TYPE_USER
        
        else:
            target_id_processed = maybe_snowflake(target_id)
            if (target_id_processed is None):
                raise TypeError(
                    f'`target_id` can be `int`, `{Role.__name__}`, `{ClientUserBase.__name__}`, got '
                    f'{target_id.__class__.__name__}; {target_id!r}.'
                )
            
            target_type_processed = None
        
        # target_type
        if target_type is None:
            if target_type_processed is None:
                raise ValueError(
                    f'`target_type` cannot be `None` if `target_id` is given as a snowflake. '
                    f'Got target_id={target_id!r}.'
                )
        
        else:
            target_type_processed_from_target_type = preconvert_preinstanced_type(
                target_type, 'target_type', PermissionOverwriteTargetType
            )
            
            if target_type_processed is None:
                target_type_processed = target_type_processed_from_target_type
            
            else:
                if target_type_processed is not target_type_processed_from_target_type:
                    raise ValueError(
                        f'If `target_id` is given as an entity, then `target_type` should not be given, or should '
                        f'match the entity\'s type. Got target_id={target_id!r}; target_type={target_type!r}.'
                    )
        
        # allow
        if allow is None:
            allow = Permission()
        
        elif isinstance(allow, Permission):
            pass
        
        elif isinstance(allow, int):
            allow = Permission(allow)
        
        else:
            raise TypeError(
                f'`allow` can be `None`, `{Permission.__name__}`, `int`, got {allow.__class__.__name__}; {allow!r}.'
            )
        
        # deny
        if deny is None:
            deny = Permission()
        
        elif isinstance(deny, Permission):
            pass
        
        elif isinstance(deny, int):
            deny = Permission(deny)
        
        else:
            raise TypeError(
                f'`deny` can be `None`, `{Permission.__name__}`, `int`, got {deny.__class__.__name__}; {deny!r}.'
            )
        
        # Build
        self = object.__new__(cls)
        self.target_id = target_id_processed
        self.target_type = target_type_processed
        self.allow = allow
        self.deny = deny
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a permission overwrite from the given data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        
        Returns
        -------
        self : ``PermissionOverwrite``
        """
        self = object.__new__(cls)
        
        self.target_id = int(data['id'])
        self.target_type = PermissionOverwriteTargetType.get(get_permission_overwrite_key_value(data))
        self.allow = Permission(data[PERMISSION_ALLOW_KEY])
        self.deny = Permission(data[PERMISSION_DENY_KEY])
        
        return self
    
    
    def to_data(self, *, include_internals=False):
        """
        Converts the permission overwrite to a json serializable object.
        
        Parameters
        ----------
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields (like id-s) should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {
            'type': self.target_type.value,
            PERMISSION_ALLOW_KEY: format(self.allow, 'd'),
            PERMISSION_DENY_KEY: format(self.deny, 'd'),
        }
        
        if include_internals:
            data['id'] = str(self.target_id)
        
        return data
    
    
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
    
    
    def __hash__(self):
        """Returns the permission overwrite's hash."""
        return self.target_id ^ self.allow ^ self.deny ^ (self.target_type.value << 16)
    
    
    def __repr__(self):
        """Returns the permission overwrite's representation."""
        return f'<{self.__class__.__name__} target={self.target!r}>'
    
    
    def keys(self):
        """
        Yields the permissions' names.
        
        This method is an iterable generator.
        
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
            if (allow >> index) & 1:
                state = +1
            elif (deny >> index) & 1:
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
            if (allow >> index) & 1:
                state = +1
            elif (deny >> index) & 1:
                state = -1
            else:
                state = 0
            
            yield key, state
    
    
    def __getitem__(self, key):
        """Returns the permission's state for the given permission name."""
        index = Permission.__keys__[key]
        if (self.allow >> index) & 1:
            state = +1
        elif (self.deny >> index) & 1:
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
        
        # allow
        if self.allow != other.allow:
            return False
        
        # deny
        if self.deny != other.deny:
            return False
        
        # target_id
        if self.target_id != other.target_id:
            return False
        
        # target_type
        if self.target_type is not other.target_type:
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
