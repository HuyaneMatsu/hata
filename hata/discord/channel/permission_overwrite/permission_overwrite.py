__all__ = ('PermissionOverwrite', )

from scarletio import RichAttributeErrorBaseType, include

from ...permission import Permission

from .fields.allow import parse_allow, put_allow_into, validate_allow
from .fields.deny import parse_deny, put_deny_into, validate_deny
from .fields.target import validate_target
from .fields.target_id import parse_target_id, put_target_id_into, validate_target_id
from .fields.target_type import parse_target_type, put_target_type_into, validate_target_type
from .preinstanced import PermissionOverwriteTargetType


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
    
    def __new__(cls, target_id, *, target_type = None, allow = None, deny = None):
        """
        Creates a new permission overwrite from the given parameters.
        
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
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        target_id_processed, target_type_processed = validate_target(target_id)
        
        if (target_type is None):
            if target_type_processed is PermissionOverwriteTargetType.unknown:
                raise ValueError(
                    f'`target_type` cannot be `None` if `target_id` is given as a snowflake. '
                    f'Got target_id={target_id!r}.'
                )
        
        else:
            target_type_processed_from_target_type = validate_target_type(target_type)
            if target_type_processed is PermissionOverwriteTargetType.unknown:
                target_type_processed = target_type_processed_from_target_type
            else:
                if target_type_processed is not target_type_processed_from_target_type:
                    raise ValueError(
                        f'If `target_id` is given as an entity, then `target_type` should not be given, or should '
                        f'match the entity\'s type. Got target_id={target_id!r}; target_type={target_type!r}.'
                    )
                    
        
        allow = validate_allow(allow)
        deny = validate_deny(deny)
        
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
        
        self.target_id = parse_target_id(data)
        self.target_type = parse_target_type(data)
        self.allow = parse_allow(data)
        self.deny = parse_deny(data)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the permission overwrite to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default fields should be included as well.
            
            > This parameter has no effect on any fields.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields (like id-s) should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        put_allow_into(self.allow, data, defaults)
        put_deny_into(self.deny, data, defaults)
        put_target_id_into(self.target_id, data, defaults, include_internals = include_internals)
        put_target_type_into(self.target_type, data, defaults)
        
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
    
    
    def copy(self):
        """
        Copies the permission overwrite.
        
        Returns
        -------
        new : `instance<cls<self>>`
        """
        new = object.__new__(type(self))
        new.allow = self.allow
        new.deny = self.deny
        new.target_id = self.target_id
        new.target_type = self.target_type
        return new
    
    
    def copy_with(self, **keyword_parameters):
        """
        Copies the permission overwrite modifying the given values.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            The specified fields to change.
        """
        allow = self.allow
        deny = self.deny
        target_id = self.target_id
        target_type = self.target_type
        
        # allow
        try:
            allow = keyword_parameters.pop('allow')
        except KeyError:
            pass
        else:
            allow = validate_allow(allow)
        
        # deny
        try:
            deny = keyword_parameters.pop('deny')
        except KeyError:
            pass
        else:
            deny = validate_deny(deny)
        
        # [EXTRA] target 
        try:
            target = keyword_parameters.pop('target')
        except KeyError:
            pass
        else:
            target_id, potential_target_type = validate_target(target)
            if (potential_target_type is not PermissionOverwriteTargetType.unknown):
                target_type = potential_target_type
        
        # target_id
        try:
            target_id = keyword_parameters.pop('target_id')
        except KeyError:
            pass
        else:
            target_id = validate_target_id(target_id)
        
        # target_type
        try:
            target_type = keyword_parameters.pop('target_type')
        except KeyError:
            pass
        else:
            target_type = validate_target_type(target_type)
        
        
        new = object.__new__(type(self))
        new.allow = allow
        new.deny = deny
        new.target_id = target_id
        new.target_type = target_type
        return new
