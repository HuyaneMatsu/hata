__all__ = ('EmbeddedActivityState',)


from scarletio import RichAttributeErrorBaseType

from ..activity import Activity
from ..channel import ChannelType, create_partial_channel_from_id
from ..core import EMBEDDED_ACTIVITY_STATES, GUILDS
from ..user import create_partial_user_from_id


EMBEDDED_ACTIVITY_UPDATE_NONE = 0
EMBEDDED_ACTIVITY_UPDATE_CREATE = 1
EMBEDDED_ACTIVITY_UPDATE_DELETE = 2
EMBEDDED_ACTIVITY_UPDATE_UPDATE = 3
EMBEDDED_ACTIVITY_UPDATE_USER_ADD = 4
EMBEDDED_ACTIVITY_UPDATE_USER_DELETE = 5


def _add_embedded_activity_state_to_guild_cache(embedded_activity_state):
    """
    Adds the embedded activity to it's guild.
    
    Parameters
    ----------
    embedded_activity_state : ``EmbeddedActivityState``
        The embedded activity to add to it's guild's cache.
    """
    try:
        guild = GUILDS[embedded_activity_state.guild_id]
    except KeyError:
        pass
    else:
        embedded_activity_states = guild._embedded_activity_states
        if (embedded_activity_states is None):
            embedded_activity_states = set()
            guild._embedded_activity_states = embedded_activity_states
        
        embedded_activity_states.add(embedded_activity_state)


def _remove_embedded_activity_state_from_guild_cache(embedded_activity_state):
    """
    Adds the embedded activity to it's guild.
    
    Parameters
    ----------
    embedded_activity_state : ``EmbeddedActivityState``
        The embedded activity to add to it's guild's cache.
    """
    try:
        guild = GUILDS[embedded_activity_state.guild_id]
    except KeyError:
        pass
    else:
        embedded_activity_states = guild._embedded_activity_states
        if (embedded_activity_states is not None):
            try:
                embedded_activity_states.remove(embedded_activity_state)
            except KeyError:
                pass
            else:
                if not embedded_activity_state:
                    guild._embedded_activity_states = None


def difference_handle_embedded_activity_update_event(data):
    """
    Handles embedded activity events returning the embedded activity state and the changes with it.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Embedded activity update event.
    
    Returns
    -------
    embedded_activity_state : ``EmbeddedActivityState``
        The updated embedded activity state.
    
    changes : `list` of `tuple` (`int`, `Any`)
        Change entries. Each tuple` has `2` elements:
        
        - The action identifier of the change:
        
            Can be one of the following:
            
            +---------------------------------------+-------+
            | Respective name                       | Value |
            +=======================================+=======+
            | EMBEDDED_ACTIVITY_UPDATE_NONE         | 0     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_CREATE       | 1     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_DELETE       | 2     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_UPDATE       | 3     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_USER_ADD     | 4     |
            +---------------------------------------+-------+
            | EMBEDDED_ACTIVITY_UPDATE_USER_DELETE  | 5     |
            +---------------------------------------+-------+
        
        - The value in the context of the action.
            
            If `action` is `EMBEDDED_ACTIVITY_UPDATE_UPDATE`, this value will contain the updated attributes of the
            activity.
            
            +-------------------+-----------------------------------+
            | Keys              | Values                            |
            +===================+===================================+
            | assets            | `None`, ``ActivityAssets``        |
            +-------------------+-----------------------------------+
            | created_at        | `datetime`                        |
            +-------------------+-----------------------------------+
            | details           | `None`, `str`                     |
            +-------------------+-----------------------------------+
            | flags             | ``ActivityFlag``                  |
            +-------------------+-----------------------------------+
            | name              | `str`                             |
            +-------------------+-----------------------------------+
            | metadata          | ``ActivityMetadataBase``          |
            +-------------------+-----------------------------------+
            | party             | `None`, ``ActivityParty``         |
            +-------------------+-----------------------------------+
            | secrets           | `None`, ``ActivitySecrets``       |
            +-------------------+-----------------------------------+
            | session_id        | `None`, `str`                     |
            +-------------------+-----------------------------------+
            | state             | `None`, `str`                     |
            +-------------------+-----------------------------------+
            | sync_id           | `None`, `str`                     |
            +-------------------+-----------------------------------+
            | timestamps        | `None`, `ActivityTimestamps``     |
            +-------------------+-----------------------------------+
            | url               | `None`, `str`                     |
            +-------------------+-----------------------------------+
            
            If `action` is `EMBEDDED_ACTIVITY_UPDATE_USER_ADD`, `EMBEDDED_ACTIVITY_UPDATE_USER_DELETE`, it will
            contain the joined or left user's identifier.
    """
    embedded_activity_state, is_created = EmbeddedActivityState(data, None)
    
    changes = []
    
    # If the object was just created, we have 2 cases:
    # Just came to cache as a deleted activity / it was created
    if is_created:
        if embedded_activity_state.users:
            _add_embedded_activity_state_to_guild_cache(embedded_activity_state)
            
            changes.append((EMBEDDED_ACTIVITY_UPDATE_CREATE, None))
        else:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_DELETE, None))
    
    else:
        joined_user_ids, left_user_ids = embedded_activity_state._difference_update_use_ids(data)
        for user_id in joined_user_ids:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_USER_ADD, user_id))
        
        for user_id in left_user_ids:
            changes.append((EMBEDDED_ACTIVITY_UPDATE_USER_DELETE, user_id))
        
        if embedded_activity_state.user_ids:
            activity_old_attributes = embedded_activity_state.activity._difference_update_attributes(
                data['embedded_activity'],
            )
            if activity_old_attributes:
                changes.append((EMBEDDED_ACTIVITY_UPDATE_UPDATE, activity_old_attributes))
        else:
            embedded_activity_state.activity._update_attributes(data['embedded_activity'])
            
            _remove_embedded_activity_state_from_guild_cache(embedded_activity_state)
            changes.append((EMBEDDED_ACTIVITY_UPDATE_DELETE, None))
    
    return embedded_activity_state, changes


def handle_embedded_update_event(data):
    """
    Handles an embedded activity event an iterates over the resulted events.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Embedded activity update event.
    """
    embedded_activity_state, is_created = EmbeddedActivityState(data, None)
    if is_created:
        _add_embedded_activity_state_to_guild_cache(embedded_activity_state)
    else:
        embedded_activity_state._update_user_ids(data)
        embedded_activity_state.activity._update_attributes(data['embedded_activity'])
        
        if not embedded_activity_state.user_ids:
            _remove_embedded_activity_state_from_guild_cache(embedded_activity_state)


class EmbeddedActivityState(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    activity : ``Activity``
        The embedded activity.
    channel_id : `int`
        The respective channel's identifier.
    guild_id : `int`
        The respective guild's identifier.
    user_ids : `set` of `int`
        The joined users' identifiers.
    
    Notes
    -----
    Embedded activity instances are weakreferable.
    """
    __slots__ = ('__weakref__', 'activity', 'channel_id', 'guild_id', 'user_ids')
    
    
    def __new__(cls, data, guild_id):
        """
        Creates a new embedded activity state instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received data.
        guild_id : `None`, `int`
            The guild's identifier where the activity is.
        
        Returns
        -------
        self : ``EmbeddedActivityState``
            The instance itself.
        is_created : `bool`
            Whether the instance was just created.
        """
        if guild_id is None:
            guild_id = data.get('guild_id', None)
            if guild_id is None:
                guild_id = 0
            else:
                guild_id = int(guild_id)
        
        channel_id = int(data['channel_id'])
        activity_data = data['embedded_activity']
        application_id = activity_data.get('application_id', None)
        if application_id is None:
            application_id = 0
        else:
            application_id = int(application_id)
        
        key = (guild_id, channel_id, application_id)
        
        try:
            self = EMBEDDED_ACTIVITY_STATES[key]
        except KeyError:
            self = object.__new__(cls)
            self.channel_id = channel_id
            self.guild_id = guild_id
            self.activity = Activity.from_data(activity_data)
            self.user_ids = set(int(user_id) for user_id in data['users'])
            
            EMBEDDED_ACTIVITY_STATES[key] = self
            is_created = True
        
        else:
            is_created = False
        
        return self, is_created
    
    
    def __repr__(self):
        """Returns the embedded activity's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' guild_id=', repr(self.guild_id),
            ', channel_id=', repr(self.channel_id),
            ', user_ids=', repr(self.user_ids),
            '>',
        ]
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activities are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.activity.application_id != other.activity.application_id:
            return False
        
        if self.channel_id != other.channel_id:
            return False
        
        if self.guild_id != other.guild_id:
            return False
        
        
    def __hash__(self):
        """Returns the hash value of the embedded activity state."""
        return self.guild_id ^ self.channel_id ^ self.activity.application_id
    
    
    @property
    def guild(self):
        """
        Returns the guild where the embedded activity is. The guild must be cached.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        return GUILDS.get(self.guild_id, None)
    
    
    @property
    def channel(self):
        """
        Returns the channel where the embedded activity is. The channel must be cached.
        
        Returns
        -------
        channel : ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.unknown, self.guild_id)
    
    
    @property
    def users(self):
        """
        Returns the users of the embedded activity.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return [create_partial_user_from_id(user_id) for user_id in self.user_ids]
    
    
    def _update_user_ids(self, data):
        """
        Updates the user id-s of the embedded activity state.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embedded activity state data.
        """
        self.user_ids = set(int(user_id) for user_id in data['users'])
    
    
    def _difference_update_use_ids(self, data):
        """
        Difference updates the user id-s of the embedded activity state.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embedded activity state data.
        
        Returns
        -------
        joined_user_ids : `set` of `int`
            The joined users' identifiers.
        left_user_ids : `set` of `int`
            The left users' identifiers.
        """
        new_user_ids = set(int(user_id) for user_id in data['users'])
        old_user_ids = self.user_ids
        self.user_ids = new_user_ids
        
        return new_user_ids - old_user_ids, old_user_ids - new_user_ids
