__all__ = ('TeamMember',)

from scarletio import RichAttributeErrorBaseType

from ...user import ZEROUSER

from .fields import (
    parse_role, parse_state, parse_user, put_role_into, put_state_into, put_user_into,
    validate_role, validate_state, validate_user
)
from .preinstanced import TeamMemberRole, TeamMembershipState


class TeamMember(RichAttributeErrorBaseType):
    """
    Represents a member of a ``Team``.
    
    Attributes
    ----------
    role : `None`, `tuple` of ``TeamMemberRole``
        The role of the team member.
    state : ``TeamMembershipState``
        The state of the team member. A member can be invited or can have the invite already accepted.
    user : ``ClientUserBase``
        The corresponding user account of the team member object.
    """
    __slots__ = ('role', 'state', 'user',)
    
    def __new__(cls, *, role = ..., state = ..., user = ...):
        """
        Creates a new team member from the given parameters.
        
        Parameters
        ----------
        role : `None`, `str`, ``TeamMemberRole``, Optional (Keyword only)
            The role of the team member.
        
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
        # role
        if role is ...:
            role = TeamMemberRole.none
        else:
            role = validate_role(role)
        
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
        self.role = role
        self.state = state
        self.user = user
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a `TeamMember` object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Team member data received from Discord.
        """
        self = object.__new__(cls)
        self.role = parse_role(data)
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
        put_role_into(self.role, data, defaults)
        put_state_into(self.state, data, defaults)
        
        if include_internals:
            put_user_into(self.user, data, defaults)
        
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
        
        # role
        repr_parts.append(', role = ')
        repr_parts.append(self.role.name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the team member's hash value, what is equal to it's user's id."""
        hash_value = 0
        
        # role
        hash_value ^= hash(self.role.value)
        
        # state
        hash_value ^= self.state.value
        
        # user
        hash_value ^= hash(self.user)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two team members are equal."""
        if type(self) is not type(other):
            return False
        
        # role
        if (self.role is not other.role):
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
        new.role = self.role
        new.state = self.state
        new.user = self.user
        return new
    
    
    def copy_with(self, *, role = ..., state = ..., user = ...):
        """
        Copies the team member with the the defined fields.
        
        Parameters
        ----------
        role : `None`, `str`, ``TeamMemberRole``, Optional (Keyword only)
            The role of the team member.
        
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
        # role
        if role is ...:
            role = self.role
        else:
            role = validate_role(role)
        
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
        new.role = role
        new.state = state
        new.user = user
        return new
