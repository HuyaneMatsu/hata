__all__ = ('Team', )

from ...bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ...core import TEAMS
from ...http import urls as module_urls
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import ClientUserBase, ZEROUSER, create_partial_user_from_id

from ..team_member import TeamMember, TeamMembershipState

from .fields import (
    parse_id, parse_members, parse_name, parse_owner_id, put_id_into, put_members_into, put_name_into,
    put_owner_id_into, validate_id, validate_members, validate_name, validate_owner_id
)


TEAM_ICON = IconSlot(
    'icon',
    'icon',
    module_urls.team_icon_url,
    module_urls.team_icon_url_as,
    add_updater = False,
)

PRECREATE_FIELDS = {
    'icon': ('icon', TEAM_ICON.validate_icon),
    'members': ('members', validate_members),
    'name': ('name', validate_name),
    'owner_id': ('owner_id', validate_owner_id),
}


class Team(DiscordEntity, immortal = True):
    """
    Represents a Team on the Discord developer portal.
    
    Attributes
    ----------
    icon_hash : `int`
        The team's icon's hash as `uint128`. Defaults to `0`.
    icon_type : `IconType`
        The team's icon's type.
    id : `int`
        The unique identifier number of the team.
    members : `tuple` of `TeamMember`
        The members of the team. Includes invited members as well.
    name : `str`
        The teams name.
    owner_id : `int`
        The team's owner's id.
    
    Notes
    -----
    Team objects support weakreferencing.
    """
    __slots__ = ('members', 'name', 'owner_id',)
    
    icon = TEAM_ICON
    
    def __new__(cls, *, icon = ..., members = ..., name = ..., owner_id = ...):
        """
        Creates a partial team instance.
        
        Parameters
        ----------
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The team's icon.
        
        members : `None`, `iterable` of ``TeamMember``, Optional (Keyword only)
            The members of the team.
        
        name : `str`, Optional (Keyword only)
            The team's name.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The team's owner's identifier.
        
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
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon, allow_data = True)
        
        # members
        if members is ...:
            members = None
        else:
            members = validate_members(members)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # owner_id
        if owner_id is ...:
            owner_id = 0
        else:
            owner_id = validate_owner_id(owner_id)
        
        self = object.__new__(cls)
        self.id = 0
        self.icon = icon
        self.members = members
        self.name = name
        self.owner_id = owner_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new team from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Team data.
        
        Returns
        -------
        team : ``Team``
        """
        team_id = parse_id(data)
        try:
            self = TEAMS[team_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = team_id
        
        self._set_attributes(data)
        return self
    
    
    @classmethod
    def _create_empty(cls, team_id):
        """
        Creates a new team instance with it's attribute set to their default values.
        
        Parameters
        ----------
        team_id : `int`
            The team's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = team_id
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        self.members = None
        self.name = ''
        self.owner_id = 0
        return self
    
    
    @classmethod
    def precreate(cls, team_id, **keyword_parameters):
        """
        Creates a cached team instance.
        
        Parameters
        ----------
        team_id : `int`
            The team's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The team's icon.
        
        members : `None`, `iterable` of ``TeamMember``, Optional (Keyword only)
            The members of the team.
        
        name : `str`, Optional (Keyword only)
            The team's name.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The team's owner's identifier.
        
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
        team_id = validate_id(team_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = TEAMS[team_id]
        except KeyError:
            self = cls._create_empty(team_id)
            TEAMS[team_id] = self
        else:
            if (not self.partial):
                return self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the team into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        put_name_into(self.name, data, defaults)
        put_members_into(self.members, data, defaults, include_internals = include_internals)
        put_owner_id_into(self.owner_id, data, defaults)
        
        return data
    
    
    def to_data_user(self):
        """
        Converts the team into a json serializable object as it would be a user.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        team_id = self.id
        
        # There are more fields, but who cares.
        return {
            'id': str(team_id),
            'username': f'team{team_id}',
            'avatar': None,
            'discriminator': '0000',
            'flags': 1024,
        }
    
    
    def _set_attributes(self, data):
        """
        Sets the team's attributes from the given data (except ``.id``).
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `object`) items
            Team dat.
        """
        self._set_icon(data)
        self.name = parse_name(data)
        self.members = parse_members(data)
        self.owner_id = parse_owner_id(data)
    
    
    def __repr__(self):
        """Returns the team's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the team's hash value."""
        team_id = self.id
        if team_id:
            return team_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Calculates the team's hash based on their fields.
        
        This method is called by ``.__hash__`` if the team has no ``.id`` set.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # icon
        hash_value ^= hash(self.icon)
        
        # members
        members = self.members
        if (members is not None):
            hash_value ^= len(members) << 8
            
            for member in members:
                hash_value ^= hash(member)
        
        # name
        hash_value ^= hash(self.name)
        
        # owner_id
        hash_value ^= hash(self.owner_id)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two teams are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two teams are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return (self_id == other_id)
        
        # icon
        if self.icon != other.icon:
            return False
        
        # members
        if self.members != other.members:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # owner_id
        if self.owner_id != other.owner_id:
            return False
        
        return True
    
    
    @property
    def owner(self):
        """
        Returns the team's owner.
        
        Returns
        -------
        owner : ``ClientUserBase``
        """
        owner_id = self.owner_id
        if owner_id:
            owner = create_partial_user_from_id(owner_id)
        else:
            owner = ZEROUSER
        
        return owner
    
    
    def iter_members(self):
        """
        Iterates over the team members of team.
        
        This method is an iterable generator.
        
        Yields
        ------
        team_member : ``TeamMember``
        """
        members = self.members
        if (members is not None):
            yield from members
    
    
    @property
    def invited(self):
        """
        A list of the invited users to the team.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        target_state = TeamMembershipState.invited
        return [team_member.user for team_member in self.iter_members() if team_member.state is target_state]
    
    
    @property
    def accepted(self):
        """
        A list of the users, who accepted their invite to the team.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        target_state = TeamMembershipState.accepted
        return [team_member.user for team_member in self.iter_members() if team_member.state is target_state]
    
    
    def copy(self):
        """
        Copies the team.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = 0
        new.icon_hash = self.icon_hash
        new.icon_type = self.icon_type
        members = self.members
        if (members is not None):
            members = (*members, )
        new.members = members
        new.name = self.name
        new.owner_id = self.owner_id
        return new
    
    
    def copy_with(self, *, icon = ..., members = ..., name = ..., owner_id = ...):
        """
        Copies the team with the defined fields.
        
        Parameters
        ----------
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The team's icon.
        
        members : `None`, `iterable` of ``TeamMember``, Optional (Keyword only)
            The members of the team.
        
        name : `str`, Optional (Keyword only)
            The team's name.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The team's owner's identifier.
        
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
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon, allow_data = True)
        
        # members
        if members is ...:
            members = self.members
            if (members is not None):
                members = (*members,)
        else:
            members = validate_members(members)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # owner_id
        if owner_id is ...:
            owner_id = self.owner_id
        else:
            owner_id = validate_owner_id(owner_id)
        
        new = object.__new__(type(self))
        new.id = 0
        new.icon = icon
        new.members = members
        new.name = name
        new.owner_id = owner_id
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether the team is partial.
        
        Returns
        -------
        partial : `bool
        """
        return (self.id == 0)
