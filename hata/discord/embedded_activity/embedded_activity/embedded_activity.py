__all__ = ('EmbeddedActivity',)

from ...bases import DiscordEntity
from ...channel import ChannelType, create_partial_channel_from_id
from ...core import EMBEDDED_ACTIVITIES, GUILDS
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_application_id, parse_guild_id, parse_id, parse_launch_id, parse_location, parse_user_states,
    put_application_id, put_guild_id, put_id, put_launch_id, put_location,
    put_user_states, validate_application_id, validate_guild_id, validate_id, validate_launch_id,
    validate_location, validate_user_states
)
from .helpers import _add_embedded_activity_to_guild_cache, _remove_embedded_activity_from_guild_cache


PRECREATE_FIELDS = {
    'application_id': ('application_id', validate_application_id),
    'guild_id': ('guild_id', validate_guild_id),
    'launch_id': ('launch_id', validate_launch_id),
    'location': ('location', validate_location),
    'user_states': ('user_states', validate_user_states),
}


class EmbeddedActivity(DiscordEntity):
    """
    Represents an embedded activity's state.
    
    Attributes
    ----------
    application_id : `int`
        The owner application's identifier.
    
    guild_id : `int`
        The respective guild's identifier.
    
    id : `int`
        The embedded activity's identifier.
    
    launch_id : `int`
        Unique identifier for the activity launch.
    
    location : `None | EmbeddedActivityLocation`
        Where the activity is located.
    
    user_states : `dict<int, EmbeddedActivityUserState>`
        The users state in the activity.
    
    Notes
    -----
    Embedded activities are weakreferable.
    """
    __slots__ = ('__weakref__', 'application_id', 'guild_id', 'launch_id', 'location', 'user_states')
    
    def __new__(
        cls,
        *,
        application_id = ...,
        location = ...,
    ):
        """
        Creates a new partial embedded activities with the given fields.
        
        Parameters
        ----------
        application_id : `int | Application`, Optional (Keyword only)
            The owner application's identifier.
        
        location : `None | EmbeddedActivityLocation`, Optional (Keyword only)
            Where the activity is located.
        
        Raises
        ------
        TypeError
            - If a parameter's value is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # channel_id
        if application_id is ...:
            application_id = 0
        else:
            application_id = validate_application_id(application_id)
        
        # location
        if location is ...:
            location = None
        else:
            location = validate_location(location)
        
        # Construct
        self = object.__new__(cls)
        self.application_id = application_id
        self.guild_id = 0
        self.id = 0
        self.launch_id = 0
        self.location = location
        self.user_states = {}
        return self
    
    
    def __repr__(self):
        """Returns the embedded activity's representation."""
        repr_parts = ['<', type(self).__name__]
        
        embedded_activity_id = self.id
        if embedded_activity_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(embedded_activity_id))
            field_added = True
        
        else:
            repr_parts.append(' (partial)')
            field_added = False
        
        guild_id = self.guild_id
        if guild_id:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' guild_id = ')
            repr_parts.append(repr(guild_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activities are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id == other_id
        
        return self._is_equal_partial(other)
    
    
    def __ne__(self, other):
        """Returns whether the two embedded activities are not the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id != other_id
        
        return not self._is_equal_partial(other)
    
    
    def _is_equal_partial(self, other):
        """
        Returns whether the embedded activity is equal to the given one.
        This function is called when one or both the embedded activities are partial.
        
        Parameters
        ----------
        other : ``instance<type<self>>``
            The other embedded_activity to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        # application_id
        if self.application_id != other.application_id:
            return False
        
        # guild_id
        # Skip it, non partial field
        
        # id
        # Skip it, non partial field
        
        # launch_id
        # Skip it, non partial field
        
        # location
        if self.location != other.location:
            return False
        
        # user_states
        # Skip it, non partial field
        
        return True
    
    
    def __hash__(self):
        """Returns the embedded activity's hash value."""
        embedded_activity_id = self.id
        if embedded_activity_id:
            return embedded_activity_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns the embedded activity's hash value.
        This function is called when the embedded activity is partial.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # application_id
        hash_value ^= self.application_id
        
        # guild_id
        # Skip it, non partial field
        
        # id
        # Skip it, non partial field
        
        # launch_id
        # Skip it, non partial field
        
        # location
        location = self.location
        if (location is not None):
            hash_value ^= hash(location)
        
        # user_states
        # Skip it, non partial field.
        
        return hash_value
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates a new embedded activities from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Embedded activity data.
        
        guild_id : `int` = `0`, Optional
            The respective guild's identifier.
            
            If given the instance will not be strong cached.
        
        Returns
        -------
        self : `instance<cls>`
        """
        embedded_activity_id = parse_id(data)
        
        try:
            self = EMBEDDED_ACTIVITIES[embedded_activity_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = embedded_activity_id
            self._set_attributes(data, True, guild_id)
            EMBEDDED_ACTIVITIES[embedded_activity_id] = self
        
        else:
            if self.partial:
                self._set_attributes(data, False, guild_id)
        
        return self
    
    
    @classmethod
    def from_data_is_created(cls, data):
        """
        Creates a new embedded activities from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Embedded activity data.
        
        Returns
        -------
        self : `instance<cls>`
        created : `bool`
        """
        embedded_activity_id = parse_id(data)
        
        try:
            self = EMBEDDED_ACTIVITIES[embedded_activity_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = embedded_activity_id
            self._set_attributes(data, True, 0)
            EMBEDDED_ACTIVITIES[embedded_activity_id] = self
            created = True
        
        else:
            if self.partial:
                self._set_attributes(data, False, 0)
                created = True
            
            else:
                created = False
        
        return self, created
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the embedded activities into it's json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_application_id(self.application_id, data, defaults)
        put_location(self.location, data, defaults)
        
        if include_internals:
            put_guild_id(self.guild_id, data, defaults)
            put_id(self.id, data, defaults)
            put_launch_id(self.launch_id, data, defaults)
            put_user_states(self.user_states, data, defaults)
        
        return data
    
    
    def _set_attributes(self, data, creation, guild_id):
        """
        Sets the attributes of the embedded activity.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Embedded activity data.
        
        guild_id : `int` = `0`, Optional
            The respective guild's identifier.
        """
        if guild_id:
            strong_cache = False
        else:
            strong_cache = True
            guild_id = parse_guild_id(data)
        
        self.application_id = parse_application_id(data)
        self.guild_id = guild_id
        self.launch_id = parse_launch_id(data)
        self.location = parse_location(data)
        self.user_states = user_states = parse_user_states(data, ({} if creation else self.user_states), guild_id)
        
        if strong_cache and user_states:
            _add_embedded_activity_to_guild_cache(self)
    
    
    def _update_user_states(self, data):
        """
        Updates the user id-s of the embedded activities.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Embedded activity data.
        """
        user_states = parse_user_states(data, self.user_states, self.guild_id)
        if not user_states:
            _remove_embedded_activity_from_guild_cache(self)
    
    
    def _difference_update_user_states(self, data):
        """
        Difference updates the user id-s of the embedded activities.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Embedded activity data.
        
        Returns
        -------
        joined_users : `set<ClientUserBase>`
            The joined users.
        left_users : `set<ClientUserBase>`
            The left users.
        """
        user_states = self.user_states
        old_users = {user_state.user for user_state in self.user_states.values()}
        parse_user_states(data, self.user_states, self.guild_id)
        new_users = {user_state.user for user_state in self.user_states.values()}
        
        if not user_states:
            _remove_embedded_activity_from_guild_cache(self)
        
        return new_users - old_users, old_users - new_users
    
    
    @classmethod
    def precreate(cls, embedded_activity_id, **keyword_parameters):
        """
        Precreates an embedded activity by creating a partial one with the given parameters.
        
        Parameters
        ----------
        embedded_activity_id : `int | str`
            The embedded activity's identifier.
        
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the role.
        
        Other Parameters
        ----------------
        application_id : `int | str | Application`, Optional (Keyword only)
            The owner application's identifier.
        
        guild_id : `int | str | Guild`, Optional (Keyword only)
            The respective guild's identifier.
        
        launch_id : `int | str`, Optional (Keyword only)
            Unique identifier for the activity launch.
        
        location : `None | EmbeddedActivityLocation`, Optional (Keyword only)
            Where the activity is located.
        
        user_states : `None | iterable<EmbeddedActivityUserState> | dict<int, EmbeddedActivityUserState>` \
                Optional (Keyword only)
            The users state in the activity.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            - If a parameter's value is incorrect
        """
        embedded_activity_id = validate_id(embedded_activity_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = EMBEDDED_ACTIVITIES[embedded_activity_id]
        except KeyError:
            self = cls._create_empty(embedded_activity_id)
            EMBEDDED_ACTIVITIES[embedded_activity_id] = self
        else:
            if (not self.partial):
                return self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, embedded_activity_id):
        """
        Creates an empty embedded activity with the given identifier.
        
        Parameters
        ----------
        embedded_activity_id : `int | str`
            The embedded activity's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.application_id = 0
        self.guild_id = 0
        self.id = embedded_activity_id
        self.launch_id = 0
        self.location = None
        self.user_states = {}
        return self
    
    
    def copy(self):
        """
        Copies the embedded activities.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.application_id = self.application_id
        new.guild_id = 0
        new.id = 0
        new.launch_id = 0
        location = self.location
        if (location is not None):
            location = location.copy()
        new.location = location
        new.user_states = {}
        return new
    
    
    def copy_with(
        self,
        *, 
        application_id = ...,
        location = ...,
    ):
        """
        Copies the embedded activities with the given fields.
        
        
        Parameters
        ----------
        application_id : `int | Application`, Optional (Keyword only)
            The owner application's identifier.
        
        location : `None | EmbeddedActivityLocation`, Optional (Keyword only)
            Where the activity is located.
        
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
        # channel_id
        if application_id is ...:
            application_id = self.application_id
        else:
            application_id = validate_application_id(application_id)
        
        # location
        if location is ...:
            location = self.location
            if (location is not None):
                location = location.copy()
        else:
            location = validate_location(location)
        
        # Construct
        new = object.__new__(type(self))
        new.application_id = application_id
        new.guild_id = 0
        new.id = 0
        new.launch_id = 0
        new.location = location
        new.user_states = {}
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether the embedded activity state is partial.
        
        Returns
        -------
        partial : `bool`
        """
        guild_id = self.guild_id
        if not guild_id:
            return True
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            return True
        
        embedded_activities = guild.embedded_activities
        if embedded_activities is None:
            return True
        
        if self not in embedded_activities:
            return True
        
        return guild.partial
    
    
    @property
    def guild(self):
        """
        Returns the guild where the embedded activity is. The guild must be cached.
        
        Returns
        -------
        guild : ``None | Guild``
        """
        return GUILDS.get(self.guild_id, None)
    
    
    @property
    def channel_id(self):
        """
        Returns the channel's identifier where the embedded activity is.
        
        Returns
        -------
        channel_id : `int`
        """
        location = self.location
        if location is None:
            return 0
        
        return location.channel_id
    
    
    @property
    def channel(self):
        """
        Returns the channel where the embedded activity is.
        
        Returns
        -------
        channel : `None | Channel`
        """
        location = self.location
        if location is None:
            return None
        
        channel_id = location.channel_id
        if not channel_id:
            return None
        
        return create_partial_channel_from_id(channel_id, ChannelType.unknown, self.guild_id)
    
    
    def iter_user_states(self):
        """
        Iterates over the user states of the embedded activity.
        
        This function is an iterable generator.
        
        Yields
        ------
        user_state : ``EmbeddedActivityUserState``
        """
        yield from self.user_states.values()
    
    
    def iter_users(self):
        """
        Iterates over the users in the embedded activity.
        
        This function is an iterable generator.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        for user_state in self.user_states.values():
            yield user_state.user
