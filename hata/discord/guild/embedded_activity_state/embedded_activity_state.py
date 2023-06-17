__all__ = ('EmbeddedActivityState',)

from scarletio import RichAttributeErrorBaseType

from ...activity import Activity
from ...channel import ChannelType, create_partial_channel_from_id
from ...core import EMBEDDED_ACTIVITY_STATES, GUILDS
from ...user import create_partial_user_from_id

from .constants import ACTIVITY_KEY
from .fields import (
    parse_activity, parse_user_ids, put_activity_into, put_channel_id_into, put_guild_id_into, put_user_ids_into,
    validate_activity, validate_channel_id, validate_guild_id, validate_user_ids
)
from .helpers import _add_embedded_activity_state_to_guild_cache, _remove_embedded_activity_state_from_guild_cache
from .key import EmbeddedActivityStateKey


class EmbeddedActivityState(RichAttributeErrorBaseType):
    """
    Represents an embedded activity's state.
    
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
    Embedded activity state instances are weakreferable.
    """
    __slots__ = ('__weakref__', 'activity', 'channel_id', 'guild_id', 'user_ids')
    
    
    def __new__(cls, *, activity = ..., channel_id = ..., guild_id = ..., user_ids = ...):
        """
        Creates a new partial embedded activity state with the given fields.
        
        Parameters
        ----------
        activity : ``Activity``, Optional (Keyword only)
            The embedded activity.
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The respective channel or its identifier.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The respective guild or its identifier.
        user_ids : `None`, `iterable` of (`int`, ``ClientUserBase``), Optional (Keyword only)
            The joined users' identifiers.
        
        Raises
        ------
        TypeError
            - If a parameter's value is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # activity
        if activity is ...:
            activity = Activity()
        else:
            activity = validate_activity(activity)
        
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_channel_id(channel_id)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # user_ids
        if user_ids is ...:
            user_ids = set()
        else:
            user_ids = validate_user_ids(user_ids)
        
        self = object.__new__(cls)
        self.activity = activity
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.user_ids = user_ids
        return self
        
        
    @classmethod
    def from_data(cls, data, guild_id = 0, *, strong_cache = True):
        """
        Creates a new embedded activity state from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Embedded activity data.
        guild_id : `int` = `0`, Optional
            The guild's identifier where the activity is.
        
        Returns
        -------
        self : `instance<cls>`
        """
        key = EmbeddedActivityStateKey.from_data(data, guild_id)
        
        try:
            self = EMBEDDED_ACTIVITY_STATES[key]
        except KeyError:
            self = cls._from_data_construct(data, key, strong_cache)
        
        return self
    
    
    @classmethod
    def from_data_is_created(cls, data, guild_id = 0):
        """
        Creates a new embedded activity state from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Embedded activity data.
        guild_id : `int` = `0`, Optional
            The guild's identifier where the activity is.
        
        Returns
        -------
        self : `instance<cls>`
        is_created : `bool`
        """
        key = EmbeddedActivityStateKey.from_data(data, guild_id)
        
        try:
            self = EMBEDDED_ACTIVITY_STATES[key]
        except KeyError:
            self = cls._from_data_construct(data, key, True)
            is_created = True
        else:
            is_created = False
        
        return self, is_created
    
    
    @classmethod
    def _from_data_construct(cls, data, key, strong_cache):
        """
        Constructs the embedded activity state from the given fields.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Embedded activity data.
        key : ``EmbeddedActivityStateKey``
            Embedded activity key.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.activity = parse_activity(data)
        self.channel_id = key.channel_id
        self.guild_id = key.guild_id
        self.user_ids = user_ids = parse_user_ids(data)
        
        EMBEDDED_ACTIVITY_STATES[key] = self
        
        if strong_cache and user_ids:
            _add_embedded_activity_state_to_guild_cache(self)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the embedded activity state into it's json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_activity_into(self.activity, data, defaults)
        put_channel_id_into(self.channel_id, data, defaults)
        put_guild_id_into(self.guild_id, data, defaults)
        put_user_ids_into(self.user_ids, data, defaults)
        return data
    
    
    def _update_user_ids(self, data):
        """
        Updates the user id-s of the embedded activity state.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Embedded activity state data.
        """
        self.user_ids = user_ids = parse_user_ids(data)
        
        if not user_ids:
            _remove_embedded_activity_state_from_guild_cache(self)
    
    
    def _difference_update_user_ids(self, data):
        """
        Difference updates the user id-s of the embedded activity state.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Embedded activity state data.
        
        Returns
        -------
        joined_user_ids : `set` of `int`
            The joined users' identifiers.
        left_user_ids : `set` of `int`
            The left users' identifiers.
        """
        new_user_ids = parse_user_ids(data)
        old_user_ids = self.user_ids
        self.user_ids = new_user_ids
        
        if not new_user_ids:
            _remove_embedded_activity_state_from_guild_cache(self)
        
        return new_user_ids - old_user_ids, old_user_ids - new_user_ids
    
    
    def _update_activity(self, data):
        """
        Updates the activity of the embedded activity state.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Embedded activity state data.
        """
        self.activity._update_attributes(data[ACTIVITY_KEY])
    
    
    def _difference_update_activity(self, data):
        """
        Updates the activity of the embedded activity state and returns it's changed attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Embedded activity state data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            The old attributes of the activity, that were modified.
            Check ``Activity._difference_update_attributes`` for the exact fields.
        """
        return self.activity._difference_update_attributes(data[ACTIVITY_KEY])
    
    
    def __repr__(self):
        """Returns the embedded activity's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        repr_parts.append(', user_ids = ')
        repr_parts.append(repr(self.user_ids))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activities are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        # activity.application_id
        if self.activity.application_id != other.activity.application_id:
            return False
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the embedded activity state."""
        hash_value = 0
        
        # activity
        hash_value ^= self.activity.application_id
        
        # channel_id
        hash_value ^= self.channel_id
        
        # guild_id
        hash_value ^= self.guild_id
        
        return hash_value
    
    
    @property
    def application_id(self):
        """
        Returns the embedded activity's application's identifier.
        
        Returns
        -------
        application_id : `int`
        """
        return self.activity.application_id
    
    
    @property
    def key(self):
        """
        Returns the key used to store the embedded activity in cache.
        
        Returns
        -------
        key : ``EmbeddedActivityStateKey``
        """
        return EmbeddedActivityStateKey(self.guild_id, self.channel_id, self.application_id)
    
    
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
    
    
    def copy(self):
        """
        Copies the embedded activity state.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.activity = self.activity.copy()
        new.channel_id = self.channel_id
        new.guild_id = self.guild_id
        new.user_ids = self.user_ids.copy()
        return new
    
    
    def copy_with(self, *, activity = ..., channel_id = ..., guild_id = ..., user_ids = ...):
        """
        Copies the embedded activity state with the given fields.
        
        Parameters
        ----------
        activity : ``Activity``, Optional (Keyword only)
            The embedded activity.
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The respective channel or its identifier.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The respective guild or its identifier.
        user_ids : `None`, `iterable` of (`int`, ``ClientUserBase``), Optional (Keyword only)
            The joined users' identifiers.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's value is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # activity
        if activity is ...:
            activity = self.activity.copy()
        else:
            activity = validate_activity(activity)
        
        # channel_id
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # user_ids
        if user_ids is ...:
            user_ids = self.user_ids.copy()
        else:
            user_ids = validate_user_ids(user_ids)
        
        new = object.__new__(type(self))
        new.activity = activity
        new.channel_id = channel_id
        new.guild_id = guild_id
        new.user_ids = user_ids
        return new
