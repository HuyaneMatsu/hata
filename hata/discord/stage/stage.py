__all__ = ('Stage',)

from scarletio import export

from ..bases import DiscordEntity
from ..channel import ChannelType, create_partial_channel_from_id
from ..core import GUILDS, STAGES
from ..precreate_helpers import process_precreate_parameters_and_raise_extra
from ..scheduled_event import PrivacyLevel

from .fields import (
    parse_channel_id, parse_discoverable, parse_guild_id, parse_id, parse_invite_code, parse_privacy_level,
    parse_scheduled_event_id, parse_topic, put_channel_id_into, put_discoverable_into, put_guild_id_into, put_id_into,
    put_invite_code_into, put_privacy_level_into, put_scheduled_event_id_into, put_topic_into, validate_channel_id,
    validate_discoverable, validate_guild_id, validate_id, validate_invite_code, validate_privacy_level,
    validate_scheduled_event_id, validate_topic
)


PRECREATE_FIELDS = {
    'channel': ('channel_id', validate_channel_id),
    'channel_id': ('channel_id', validate_channel_id),
    'discoverable': ('discoverable', validate_discoverable),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'invite_code': ('invite_code', validate_invite_code),
    'privacy_level': ('privacy_level', validate_privacy_level),
    'scheduled_event': ('scheduled_event_id', validate_scheduled_event_id),
    'scheduled_event_id': ('scheduled_event_id', validate_scheduled_event_id),
    'topic': ('topic', validate_topic),
}


@export
class Stage(DiscordEntity, immortal = True):
    """
    Represents an active stage instance of a stage channel.
    
    Attributes
    ----------
    channel_id : `int`
        The stage channel's identifier where the stage is active.
    discoverable : `bool`
        Whether the stage is discoverable. Only applies for public stages.
    guild_id : `int`
        The stage guild's identifier.
    id : `int`
        The stage instance's identifier.
    invite_code : `None`, `str`
        Invite code to the stage's channel.
    privacy_level : ``PrivacyLevel``
        The privacy level of the stage.
    scheduled_event_id : `int`
        The scheduled event's identifier that started the stage.
    topic : `None`, `str`
        The topic of the stage. Can be empty string.
    """
    __slots__ = (
        'channel_id', 'discoverable', 'guild_id', 'invite_code', 'privacy_level', 'scheduled_event_id', 'topic'
    )
    
    
    def __new__(cls, *, privacy_level = ..., topic = ...):
        """
        Creates a partial stage with the given fields.
        
        Parameters
        ----------
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the stage.
        topic : `None`, `str`, Optional (Keyword only)
            The topic of the stage. Can be empty string.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # privacy_level
        if privacy_level is ...:
            privacy_level = PrivacyLevel.guild_only
        else:
            privacy_level = validate_privacy_level(privacy_level)
        
        # topic
        if topic is ...:
            topic = None
        else:
            topic = validate_topic(topic)
        
        # Construct
        self = object.__new__(cls)
        self.channel_id = 0
        self.discoverable = True
        self.guild_id = 0
        self.id = 0
        self.invite_code = None
        self.privacy_level = privacy_level
        self.scheduled_event_id = 0
        self.topic = topic
        return self
    
    
    @classmethod
    def from_data(cls, data, *, strong_cache = True):
        """
        Creates a new stage instance from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Stage data.
        strong_cache : `bool` = `True`, Optional (Keyword only)
            Whether the instance should be put into its strong cache.
        
        Returns
        -------
        self : `instance<cls>`
        """
        stage_id = parse_id(data)
        try:
            self = STAGES[stage_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = stage_id
            self._set_attributes(data)
            STAGES[stage_id] = self
        
        else:
            if strong_cache and (not self.partial):
                return self
            
            self._set_attributes(data)
        
        if strong_cache:
            try:
                guild = GUILDS[self.guild_id]
            except KeyError:
                pass
            else:
                stages = guild.stages
                if stages is None:
                    stages = guild.stages = {}
                
                stages[stage_id] = self
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Serialises the stage to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether we want to include identifiers as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) Items
        """
        data = {}
        put_privacy_level_into(self.privacy_level, data, defaults)
        put_topic_into(self.topic, data, defaults)
        
        if include_internals:
            put_channel_id_into(self.channel_id, data, defaults)
            put_discoverable_into(self.discoverable, data, defaults)
            put_guild_id_into(self.guild_id, data, defaults)
            put_id_into(self.id, data, defaults)
            put_invite_code_into(self.invite_code, data, defaults)
            put_scheduled_event_id_into(self.scheduled_event_id, data, defaults)
        
        return data
    
    
    def _set_attributes(self, data):
        """
        Sets the stage's attributes from the given data. Excludes `.id`.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Stage data.
        """
        self.channel_id = parse_channel_id(data)
        self.guild_id = parse_guild_id(data)
        self.scheduled_event_id = parse_scheduled_event_id(data)
    
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the stage from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Stage data.
        """
        self.discoverable = parse_discoverable(data)
        self.invite_code = parse_invite_code(data)
        self.privacy_level = parse_privacy_level(data)
        self.topic = parse_topic(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the stage from the given data and returns the changed attributes in `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Stage data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            The changed attributes of the stage.
            
            Each item in the returned dictionary is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | discoverable  | `bool`                |
        +---------------+-----------------------+
        | invite_code   | `None`, `str`         |
        +---------------+-----------------------+
        | privacy_level | ``PrivacyLevel``      |
        +---------------+-----------------------+
        | topic         | `None`, `str`         |
        +---------------+-----------------------+
        """
        old_attributes = {}
        
        
        discoverable = parse_discoverable(data)
        if discoverable != self.discoverable:
            old_attributes['discoverable'] = self.discoverable
            self.discoverable = discoverable
        
        invite_code = parse_invite_code(data)
        if invite_code != self.invite_code:
            old_attributes['invite_code'] = self.invite_code
            self.invite_code = invite_code
        
        privacy_level = parse_privacy_level(data)
        if privacy_level is not self.privacy_level:
            old_attributes['privacy_level'] = self.privacy_level
            self.privacy_level = privacy_level
        
        topic = parse_topic(data)
        if topic != self.topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        return old_attributes
    
    
    def __repr__(self):
        """Returns the stage's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Hashes the stage."""
        stage_id = self.id
        if stage_id:
            return stage_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns the stage's hash value.
        This function is called when the stage is partial.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        # channel_id | internal
        # discoverable | internal
        # guild_id | internal
        # id | internal
        # invite_code | internal
        hash_value ^= hash(self.privacy_level)
        # scheduled_event_id | internal
        
        topic = self.topic
        if (topic is not None):
            hash_value ^= hash(topic)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two stages are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two stages are not equal."""
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
            if self.id != other.id:
                return False
        
        # privacy_level
        if self.privacy_level is not other.privacy_level:
            return False
        
        # topic
        if self.topic != other.topic:
            return False
        
        return True
    
    
    @classmethod
    def _create_empty(cls, stage_id):
        """
        Creates a stage instance with its attributes set to their default values.
        
        Parameters
        ----------
        stage_id : `int`
            The stage's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.channel_id = 0
        self.discoverable = True
        self.guild_id = 0
        self.id = stage_id
        self.invite_code = None
        self.privacy_level = PrivacyLevel.guild_only
        self.scheduled_event_id = 0
        self.topic = None
        return self
    
    
    @classmethod
    def precreate(cls, stage_id, **keyword_parameters):
        """
        Precreates the stage by creating a partial one with the given parameters. When the stage is loaded
        the precreated one will be picked up. If an already existing stage would be precreated, returns that
        instead and updates that only, if that is partial.
        
        Parameters
        ----------
        stage_id : `int`
            The stage's identifier.
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the stage.
        
        Other Parameters
        ----------------
        channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `channel_id`.
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The stage channel or its identifier where the stage is active.
        discoverable : `bool`, Optional (Keyword only)
            Whether the stage is discoverable. Only applies for public stages.
        guild : `int`, ``Guild``, Optional (Keyword only)
            Alternative for `guild_id`.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The stage's guild or its identifier.
        invite_code : `None`, `str`, Optional (Keyword only)
            Invite code to the stage's channel.
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the stage.
        scheduled_event : `int`, ``ScheduledEvent``, Optional (Keyword only)
            Alternative for `scheduled_event_id`.
        scheduled_event_id : `int`, ``ScheduledEvent``, Optional (Keyword only)
            The scheduled event or its identifier that started the stage.
        topic : `None`, `str`, Optional (Keyword only)
            The topic of the stage. Can be empty string.
        
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
        stage_id = validate_id(stage_id)

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = STAGES[stage_id]
        except KeyError:
            self = cls._create_empty(stage_id)
            STAGES[stage_id] = self
        else:
            if not self.partial:
                return self
        
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    def copy(self):
        """
        Copies the stage state.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.channel_id = 0
        new.discoverable = True
        new.guild_id = 0
        new.id = 0
        new.invite_code = None
        new.privacy_level = self.privacy_level
        new.scheduled_event_id = 0
        new.topic = self.topic
        return new
    
    
    def copy_with(self, *, privacy_level = ..., topic = ...):
        """
        Copies the stage with the given fields.
        
        Parameters
        ----------
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the stage.
        topic : `None`, `str`, Optional (Keyword only)
            The topic of the stage. Can be empty string.
        
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
        # privacy_level
        if privacy_level is ...:
            privacy_level = self.privacy_level
        else:
            privacy_level = validate_privacy_level(privacy_level)
        
        # topic
        if topic is ...:
            topic = self.topic
        else:
            topic = validate_topic(topic)
        
        new = object.__new__(type(self))
        new.channel_id = 0
        new.discoverable = True
        new.guild_id = 0
        new.id = 0
        new.invite_code = None
        new.privacy_level = privacy_level
        new.scheduled_event_id = 0
        new.topic = topic
        return new
    
    
    def _delete(self):
        """
        Removes the stage's references.
        """
        try:
            guild = GUILDS[self.guild_id]
        except KeyError:
            pass
        else:
            stages = guild.stages
            if (stages is not None):
                try:
                    del stages[self.id]
                except KeyError:
                    pass
                else:
                    if not stages:
                        guild.stages = None
    
    
    @property
    def partial(self):
        """
        Returns whether the stage is partial.
        
        Returns
        -------
        partial : `bool`
        """
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                if not guild.partial:
                    stages = guild.stages
                    if (stages is not None) and (self.id in stages.keys()):
                        return False
        
        return True
    
    
    @property
    def channel(self):
        """
        Returns the stage's channel.
        
        Returns
        -------
        channel : `None`, ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.guild_stage, self.guild_id)
    
    
    @property
    def guild(self):
        """
        Returns the stage's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
