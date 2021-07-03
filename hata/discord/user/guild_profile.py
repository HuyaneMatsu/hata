__all__ = ('GuildProfile', )

from datetime import datetime

from ...backend.export import include

from ..bases import IconSlot, Slotted

from ..utils import parse_time, DISCORD_EPOCH_START
from ..color import Color

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
    roles : `None` or `list` of ``Role``
        The user's roles at the guild.
        
        Feel free to use `.sort()` on it.
    avatar_hash : `int`
        The respective user's avatar hash at the guild in `uint128`.
    avatar_type : `bool`
        The respective user's avatar type at the guild.
    """
    __slots__ = ('boosts_since', 'joined_at', 'nick', 'pending', 'roles',)
    
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
            joined_at = parse_time(joined_at_data)
        
        self.joined_at = joined_at
        
        self._update_no_return(data)
    
    
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
                joined_at = parse_time(joined_at_data)
            
            self.joined_at = joined_at
    
    
    def _update_no_return(self, data):
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
            roles = []
            for role_id in role_ids:
                role_id = int(role_id)
                try:
                    role = create_partial_role_from_id(role_id)
                except KeyError:
                    continue
                
                roles.append(role)
            
            if (not roles):
                roles = None
        else:
            roles = None
        
        self.roles = roles
        
        boosts_since = data.get('premium_since', None)
        if (boosts_since is not None):
            boosts_since = parse_time(boosts_since)
        self.boosts_since = boosts_since
        
        self.pending = data.get('pending', None)
        
        self._set_avatar(data)
    
    
    def _update(self, data):
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
        | roles             | `None` or `list` of ``Role``  |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        nick = data.get('nick', None)
        if self.nick != nick:
            old_attributes['nick'] = self.nick
            self.nick = nick
        
        role_ids = data['roles']
        if role_ids:
            roles = []
            for role_id in role_ids:
                role_id = int(role_id)
                role = create_partial_role_from_id(role_id)
                roles.append(role)
            
            if (not roles):
                roles = None
        else:
            roles = None
        
        own_roles = self.roles
        if roles is None:
            if (own_roles is not None):
                old_attributes['roles'] = self.roles
                self.roles = None
        else:
            if own_roles is None:
                old_attributes['roles'] = None
                self.roles = roles
            else:
                own_roles.sort()
                roles.sort()
                
                if own_roles != roles:
                    old_attributes['roles'] = self.roles
                    self.roles = roles
        
        boosts_since = data.get('premium_since', None)
        if (boosts_since is not None):
            boosts_since = parse_time(boosts_since)
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
        roles = self.roles
        if roles is None:
            return default
        
        roles.sort()
        return roles[-1]
    
    
    @property
    def color(self):
        """
        Returns the color of the respective user at the respective guild.
        
        Returns
        -------
        color : ``Color``
        """
        roles = self.roles
        if (roles is not None):
            roles.sort()
            for role in reversed(roles):
                color = role.color
                if color:
                    return color
        
        return Color()
