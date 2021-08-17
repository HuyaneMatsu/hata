__all__ = ('GuildProfile', )

from datetime import datetime

from ...backend.export import include

from ..bases import IconSlot, Slotted
from ..utils import timestamp_to_datetime, DISCORD_EPOCH_START
from ..color import Color
from ..core import ROLES

create_partial_role_from_id = include('create_partial_role_from_id')

class GuildProfile(metaclass=Slotted):
    """
    Represents a user's profile at a guild.
    
    Attributes
    ----------
    boosts_since : `None` or `datetime`
        Since when the user uses it's Nitro to boost the respective guild. If the user does not boost the guild, this
        attribute is set to `None`.
    joined_at : `None` or `datetime`
        The date, since the user is the member of the guild. If this field was not included with the initial data, then
        it is set to `None`.
    nick : `None` or `str`
        The user's nick at the guild if it has.
    pending : `bool`
        Whether the user has not yet passed the guild's membership screening requirements. Defaults to `False`.
    role_ids : `None` or `tuple` of ``Role``
        The user's roles at the guild.
    avatar_hash : `int`
        The respective user's avatar hash at the guild in `uint128`.
    avatar_type : `bool`
        The respective user's avatar type at the guild.
    """
    __slots__ = ('boosts_since', 'joined_at', 'nick', 'pending', 'role_ids',)
    
    avatar = IconSlot('avatar', 'avatar', None, None)
    
    @property
    def created_at(self):
        """
        Returns ``.joined_at`` if set, else the Discord epoch in datetime.
        
        Returns
        -------
        created_at : `datetime`
        """
        created_at = self.joined_at
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        
        return created_at
    
    
    def __init__(self, data):
        """
        Creates a ``GuildProfile`` instance from the received guild profile data and from it's respective guild.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        """
        try:
            joined_at_data = data['joined_at']
        except KeyError:
            joined_at = None
        else:
            joined_at = timestamp_to_datetime(joined_at_data)
        
        self.joined_at = joined_at
        
        self._update_attributes(data)
    
    
    def __repr__(self):
        """Returns the representation of the guild profile."""
        return f'<{self.__class__.__name__}>'
    
    
    def _set_joined(self, data):
        """
        Sets ``.joined_at`` of the guild profile if it is not set yet.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        """
        if self.joined_at is None:
            try:
                joined_at_data = data['joined_at']
            except KeyError:
                joined_at = None
            else:
                joined_at = timestamp_to_datetime(joined_at_data)
            
            self.joined_at = joined_at
    
    
    def _update_attributes(self, data):
        """
        Updates the guild profile with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        """
        self.nick = data.get('nick', None)
        
        role_ids = data['roles']
        if role_ids:
            role_ids = tuple(sorted(int(role_id) for role_id in role_ids))
        else:
            role_ids = None
        self.role_ids = role_ids
        
        boosts_since = data.get('premium_since', None)
        if (boosts_since is not None):
            boosts_since = timestamp_to_datetime(boosts_since)
        self.boosts_since = boosts_since
        
        self.pending = data.get('pending', None)
        
        self._set_avatar(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the guild profile and returns it's changed attributes in a `dict` within `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | avatar            | ``Icon``                      |
        +-------------------+-------------------------------+
        | boosts_since      | `None` or `datetime`          |
        +-------------------+-------------------------------+
        | nick              | `None` or `str`               |
        +-------------------+-------------------------------+
        | pending           | `bool`                        |
        +-------------------+-------------------------------+
        | role_ids          | `None` or `tuple` of `int`    |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        nick = data.get('nick', None)
        if self.nick != nick:
            old_attributes['nick'] = self.nick
            self.nick = nick
        
        role_ids = data['roles']
        if role_ids:
            role_ids = tuple(sorted(int(role_id) for role_id in role_ids))
        else:
            role_ids = None
        
        if role_ids != self.role_ids:
            old_attributes['role_ids'] = self.role_ids
            self.role_ids = role_ids
        
        boosts_since = data.get('premium_since', None)
        if (boosts_since is not None):
            boosts_since = timestamp_to_datetime(boosts_since)
        if self.boosts_since != boosts_since:
            old_attributes['boosts_since'] = self.boosts_since
            self.boosts_since = boosts_since
        
        pending = data.get('pending', False)
        if pending != self.pending:
            old_attributes['pending'] = self.pending
            self.pending = pending
        
        self._update_avatar(data, old_attributes)
        
        return old_attributes
    
    
    def get_top_role(self, default=None):
        """
        Returns the top role of the guild profile. If the profile has no roles, then returns the `default`'s value.
        
        Parameters
        ----------
        default : `Any`, Optional
            Default value to return if the respective user has no roles at the respective guild. Defaults to `None`.
        
        Returns
        -------
        top_role : ``Role`` or `default`
        """
        top_role = default
        
        role_ids = self.role_ids
        if (role_ids is not None):
            role_found = False
            
            for role_id in role_ids:
                try:
                    role = ROLES[role_id]
                except KeyError:
                    continue
                
                if role_found:
                    if role > top_role:
                        top_role = role
                else:
                    top_role = role
                    role_found = True
        
        return top_role
    
    
    @property
    def roles(self):
        """
        Returns the roles of the guild profile in sorted form.
        
        Returns
        -------
        roles : `None` or `list` of ``Role``
        """
        role_ids = self.role_ids
        if role_ids is None:
            roles = None
        else:
            roles = sorted(create_partial_role_from_id(role_id) for role_id in self.role_ids)
        
        return roles
    
    
    @property
    def color(self):
        """
        Returns the color of the respective user at the respective guild.
        
        Returns
        -------
        color : ``Color``
        """
        role_ids = self.role_ids
        if (role_ids is not None):
            for role in sorted((create_partial_role_from_id(role_id) for role_id in self.role_ids), reverse=True):
                color = role.color
                if color:
                    return color
        
        return Color()
