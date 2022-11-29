__all__ = ('TeamMember',)

from scarletio import RichAttributeErrorBaseType

from ...user import ZEROUSER

from .fields import (
    parse_permissions, parse_state, parse_user, put_permissions_into, put_state_into, put_user_into,
    validate_permissions, validate_state, validate_user
)
from .preinstanced import TeamMembershipState


class TeamMember(RichAttributeErrorBaseType):
    """
    Represents a member of a ``Team``.
    
    Attributes
    ----------
    permissions : `None`, `tuple` of ``TeamMemberPermission``
        The permissions of the team member. Right now specific permissions are not supported, so the list has only
        one element : `'*'`, what represents all the permissions.
    state : ``TeamMembershipState``
        The state of the team member. A member can be invited or can have the invite already accepted.
    user : ``ClientUserBase``
        The corresponding user account of the team member object.
    """
    __slots__ = ('permissions', 'state', 'user',)
    
    def __new__(cls, *, permissions = ..., state = ..., user = ...):
        """
        Creates a new team member from the given parameters.
        
        Parameters
        ----------
        permissions : `None`, `iterable` of (`str`, ``TeamMemberPermission``), Optional (Keyword only)
            The permissions of the team member.
        
        state : `int`, ``TeamMembershipState``, Optional (Keyword only)
            The state of the team member.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            The corresponding user account of the team member.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # permissions
        if permissions is ...:
            permissions = None
        else:
            permissions = validate_permissions(permissions)
        
        # state
        if state is ...:
            state = TeamMembershipState.none
        else:
            state = validate_state(state)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        self = object.__new__(cls)
        self.permissions = permissions
        self.state = state
        self.user = user
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a `TeamMember` object from the data sent by Discord.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `Any`) items
            Team member data received from Discord.
        """
        self = object.__new__(cls)
        self.permissions = parse_permissions(data)
        self.state = parse_state(data)
        self.user = parse_user(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the team member to a json serializable object.
        
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
        put_permissions_into(self.permissions, data, defaults)
        put_state_into(self.state, data, defaults)
        put_user_into(self.user, data, defaults, include_internals = include_internals)
        return data
    
    
    def __repr__(self):
        """Returns the team member's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # user
        repr_parts.append(' user = ')
        repr_parts.append(repr(self.user))
        
        # state
        repr_parts.append(', state = ')
        repr_parts.append(self.state.name)
        
        # permissions
        repr_parts.append(', permissions = ')
        repr_parts.append(repr(self.permissions))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the team member's hash value, what is equal to it's user's id."""
        hash_value = 0
        
        # user
        hash_value ^= hash(self.user)
        
        # state
        hash_value ^= self.state.value
        
        # permissions
        permissions = self.permissions
        if (permissions is not None):
            hash_value ^= len(permissions) << 4
            
            for permission in permissions:
                hash_value ^= hash(permission)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two team members are equal."""
        if type(self) is not type(other):
            return False
        
        # permissions
        if (self.permissions != other.permissions):
            return False
        
        # state
        if (self.state is not other.state):
            return False
        
        # user
        if (self.user != other.user):
            return False
        
        return True
    
    
    def __gt__(self, other):
        """Returns whether self is less than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.user > other.user
    
    
    def __lt__(self, other):
        """Returns whether self is greater than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.user < other.user
    
    
    def copy(self):
        """
        Copies the team member.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        permissions = self.permissions
        if (permissions is not None):
            permissions = (*permissions, )
        new.permissions = permissions
        new.state = self.state
        new.user = self.user
        return new
    
    
    def copy_with(self, *, permissions = ..., state = ..., user = ...):
        """
        Copies the team member with the the defined fields.
        
        Parameters
        ----------
        permissions : `None`, `iterable` of (`str`, ``TeamMemberPermission``), Optional (Keyword only)
            The permissions of the team member.
        
        state : `int`, ``TeamMembershipState``, Optional (Keyword only)
            The state of the team member.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            The corresponding user account of the team member.
        
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
        # permissions
        if permissions is ...:
            permissions = self.permissions
            if (permissions is not None):
                permissions = (*permissions, )
        else:
            permissions = validate_permissions(permissions)
        
        # state
        if state is ...:
            state = self.state
        else:
            state = validate_state(state)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        new = object.__new__(type(self))
        new.permissions = permissions
        new.state = state
        new.user = user
        return new
    
    
    def iter_permissions(self):
        """
        Iterates over the permissions of the team member.
        
        This method is an iterable generator.
        
        Yields
        ------
        permission : ``TeamMemberPermission``
        """
        permissions = self.permissions
        if (permissions is not None):
            yield from permissions
