__all__ = ('ScheduledEvent', )

from ...bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ...channel import ChannelType, create_partial_channel_from_id
from ...core import GUILDS, SCHEDULED_EVENTS
from ...http import urls as module_urls
from ...precreate_helpers import process_precreate_parameters
from ...user import ZEROUSER

from ..scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase

from .fields import (
    parse_channel_id, parse_creator, parse_description, parse_end, parse_entity_id, parse_entity_metadata,
    parse_entity_type, parse_guild_id, parse_id, parse_name, parse_privacy_level, parse_sku_ids, parse_start,
    parse_status, parse_user_count, put_channel_id_into, put_creator_into, put_description_into, put_end_into,
    put_entity_id_into, put_entity_metadata_into, put_entity_type_into, put_guild_id_into, put_id_into, put_name_into,
    put_privacy_level_into, put_sku_ids_into, put_start_into, put_status_into, put_user_count_into, validate_channel_id,
    validate_creator, validate_description, validate_end, validate_entity_id, validate_entity_type, validate_guild_id,
    validate_id, validate_name, validate_privacy_level, validate_sku_ids, validate_start, validate_status,
    validate_user_count
)
from .helpers import guess_scheduled_event_entity_type_from_keyword_parameters
from .preinstanced import PrivacyLevel, ScheduledEventEntityType, ScheduledEventStatus


SCHEDULED_EVENT_IMAGE = IconSlot(
    'image',
    'image',
    module_urls.scheduled_event_image_url,
    module_urls.scheduled_event_image_url_as,
)


PRECREATE_FIELDS = {
    'channel': ('channel_id', validate_channel_id),
    'channel_id': ('channel_id', validate_channel_id),
    'creator': ('creator', validate_creator),
    'description': ('description', validate_description),
    'end': ('end', validate_end),
    'entity_id': ('entity_id', validate_entity_id),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'image': ('image', SCHEDULED_EVENT_IMAGE.validate_icon),
    'name': ('name', validate_name),
    'privacy_level': ('privacy_level', validate_privacy_level),
    'start': ('start', validate_start),
    'sku_ids': ('sku_ids', validate_sku_ids),
    'status': ('status', validate_status),
    'user_count': ('user_count', validate_user_count),
}


class ScheduledEvent(DiscordEntity):
    """
    Attributes
    ----------
    channel_id : `int`
        The event's stage's channel identifier.
    creator : ``ClientUserBase``
        The event's creator.
    description : `None`, `str`
        Description of the event.
    end : `None`, `datetime`
        The scheduled end time of the event.
    entity_id : `int`
        The event's entity's identifier.
    entity_metadata : ``ScheduledEventEntityMetadataBase``
        Metadata about the target entity.
    entity_type : ``ScheduledEventEntityType``
        To which type of entity the event is bound to.
    guild_id : `int`
        The respective event's identifier.
    id : `int`
        The scheduled event's identifier number.
    image_type : ``IconType``
        The event's image's type.
    image_hash : `int`
        The event's image hash.
    name : `str`
        The event's name.
    privacy_level : ``PrivacyLevel``
        The privacy level of the event.
    start : `None`, `datetime`
        The scheduled start time of the event.
    sku_ids : `None`, `tuple` of `int`
        Stock keeping unit identifiers used at the event.
    status : ``ScheduledEventStatus``
        The status of the event.
    user_count : `int`
        Users subscribed to the event.
    
    Notes
    -----
    Scheduled event instances support weakreferencing.
    """
    __slots__ = (
        '__weakref__', 'channel_id', 'creator', 'description', 'end', 'entity_id', 'entity_metadata', 'entity_type',
        'guild_id', 'name', 'privacy_level', 'sku_ids', 'start', 'status', 'user_count'
    )
    
    image = SCHEDULED_EVENT_IMAGE
    
    def __new__(
        cls,
        *,
        channel_id = ...,
        description = ...,
        end = ...,
        entity_type = ...,
        image = ...,
        name = ...,
        privacy_level = ...,
        start = ...,
        status = ...,
        **keyword_parameters,
    ):
        """
        Creates a new partial scheduled event with the given fields.
        
        Parameters
        ----------
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The event's stage's channel or its identifier.
        description : `None`, `str`, Optional (Keyword only)
            Description of the event.
        end : `None`, `datetime`, Optional (Keyword only)
            The scheduled end time of the event.
        entity_type : ``ScheduledEventEntityType``, `int`, Optional (Keyword only)
            To which type of entity the event is bound to.
        image : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The schedule event's image.
        name : `str`
            The event's name.
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the event.
        start : `None`, `datetime`, Optional (Keyword only)
            The scheduled start time of the event.
        status : ``ScheduledEventStatus``, Optional (Keyword only)
            The status of the event.
        **keyword_parameters : Keyword parameters
            Additional keyword parameters passed to the entity metadata.
        
        Other Parameters
        ----------------
        location : `None`, `str`, Optional (Keyword only)
            The place where the event will take place.
        speaker_ids : `None`, `iterable` of (`int`, `ClientUserBase`), Optional (Keyword only)
            The speakers' identifier of the stage channel.
        
        Raises
        ------
        TypeError
            - Extra or unused parameters.
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_channel_id(channel_id)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # end
        if end is ...:
            end = None
        else:
            end = validate_end(end)
        
        # entity_type
        if entity_type is ...:
            entity_type = guess_scheduled_event_entity_type_from_keyword_parameters(keyword_parameters)
        else:
            entity_type = validate_entity_type(entity_type)
        
        # image
        if image is ...:
            image = None
        else:
            image = cls.image.validate_icon(image, allow_data = True)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # privacy_level
        if privacy_level is ...:
            privacy_level = PrivacyLevel.guild_only
        else:
            privacy_level = validate_privacy_level(privacy_level)
        
        # start
        if start is ...:
            start = None
        else:
            start = validate_start(start)
        
        # status
        if status is ...:
            status = ScheduledEventStatus.none
        else:
            status = validate_status(status)
        
        # entity_metadata
        entity_metadata = entity_type.metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
        
        # Construct
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.creator = ZEROUSER
        self.description = description
        self.end = end
        self.entity_id = 0
        self.entity_metadata = entity_metadata
        self.entity_type = entity_type
        self.guild_id = 0
        self.id = 0
        self.image = image
        self.name = name
        self.privacy_level = privacy_level
        self.start = start
        self.sku_ids = None
        self.status = status
        self.user_count = 0
        return self
    
    
    @classmethod
    def from_data(cls, data, *, strong_cache = True):
        """
        Creates a new scheduled event instance from the received data.
        
        If the instance already exists, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Guild scheduled event data.
        strong_cache : `bool` = `True`, Optional (Keyword only)
            Whether the instance should be put into its strong cache.
        
        Returns
        -------
        self : `instance<cls>`
        """
        scheduled_event_id = parse_id(data)
        
        try:
            self = SCHEDULED_EVENTS[scheduled_event_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = scheduled_event_id
            self._set_attributes(data)
            SCHEDULED_EVENTS[scheduled_event_id] = self
        else:
            if strong_cache and (not self.partial):
                self._update_counts_only(data)
                return self
        
            self._set_attributes(data)
        
        if strong_cache:
            try:
                guild = GUILDS[self.guild_id]
            except KeyError:
                pass
            else:
                guild.scheduled_events[scheduled_event_id] = self
        
        return self
    
    
    @classmethod
    def from_data_is_created(cls, data):
        """
        Creates a new scheduled event instance from the received data. If already exists, picks it up.
        
        Also returns whether the instance was new (or partial) or already existed.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Guild scheduled event data.
        
        Returns
        -------
        self : `instance<cls>`
        is_created : `bool`
        """
        scheduled_event_id = parse_id(data)
        
        try:
            self = SCHEDULED_EVENTS[scheduled_event_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = scheduled_event_id
            SCHEDULED_EVENTS[scheduled_event_id] = self
        
        else:
            if not self.partial:
                self._update_counts_only(data)
                return self, False
        
        self._set_attributes(data)
        
        try:
            guild = GUILDS[self.guild_id]
        except KeyError:
            pass
        else:
            guild.scheduled_events[scheduled_event_id] = self
        
        return self, True
    
    
    @classmethod
    def _create_from_data_and_delete(cls, data):
        """
        Creates a new scheduled event instance from the received data.
        
        If the instance already exists, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Guild event data.
        
        Returns
        -------
        self : `instance<cls>`
            The created or found scheduled event instance.
        """
        scheduled_event_id = parse_id(data)
        
        try:
            self = SCHEDULED_EVENTS[scheduled_event_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = scheduled_event_id
            SCHEDULED_EVENTS[scheduled_event_id] = self
        else:
            if self._delete():
                self._update_counts_only(data)
                return self
        
        self._set_attributes(data)
        return self
    
    
    def _delete(self):
        """
        Tries to delete the scheduled event from its guild.
        
        Returns
        -------
        deleted : `bool`
        """
        try:
            guild = GUILDS[self.guild_id]
        except KeyError:
            return False
            
        try:
            del guild.scheduled_events[self.id]
        except KeyError:
            return False
        
        return True
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the scheduled event to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        put_channel_id_into(self.channel_id, data, defaults)
        put_description_into(self.description, data, defaults)
        put_end_into(self.end, data, defaults)
        put_entity_metadata_into(self.entity_metadata, data, defaults)
        put_entity_type_into(self.entity_type, data, defaults)
        type(self).image.put_into(self.image, data, defaults, as_data = not include_internals)
        put_name_into(self.name, data, defaults)
        put_privacy_level_into(self.privacy_level, data, defaults)
        put_start_into(self.start, data, defaults)
        put_status_into(self.status, data, defaults)
        
        if include_internals:
            put_creator_into(self.creator, data, defaults, include_internals = include_internals)
            put_entity_id_into(self.entity_id, data, defaults)
            put_guild_id_into(self.guild_id, data, defaults)
            put_id_into(self.id, data, defaults)
            put_sku_ids_into(self.sku_ids, data, defaults)
            put_user_count_into(self.user_count, data, defaults)
        
        return data
    
    
    def _set_attributes(self, data):
        """
        Sets the event's attributes form the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Scheduled event data.
        """
        self.creator = parse_creator(data)
        self.guild_id = parse_guild_id(data)
        self.user_count = parse_user_count(data)
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the attributes of the scheduled event.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Scheduled event data.
        """
        self._set_image(data)
        
        self.channel_id = parse_channel_id(data)
        self.description = parse_description(data)
        self.end = parse_end(data)
        self.entity_id = parse_entity_id(data)
        self.name = parse_name(data)
        self.privacy_level = parse_privacy_level(data)
        self.sku_ids = parse_sku_ids(data)
        self.start = parse_start(data)
        self.status = parse_status(data)
        
        self.entity_type = entity_type = parse_entity_type(data)
        self.entity_metadata = parse_entity_metadata(data, entity_type)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the attributes of the scheduled event and returns the changed ones within an `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Scheduled event data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            The updated attributes.
            
            The returned dictionary might contain the following items:
            
            +---------------------------+-----------------------------------------------+
            | Key                       | Value                                         |
            +===========================+===============================================+
            | channel_id                | `int`                                         |
            +---------------------------+-----------------------------------------------+
            | description               | `None`, `str`                                 |
            +---------------------------+-----------------------------------------------+
            | end                       | `None`, `datetime`                            |
            +---------------------------+-----------------------------------------------+
            | entity_id                 | `int`                                         |
            +---------------------------+-----------------------------------------------+
            | entity_metadata           | ``ScheduledEventEntityMetadataBase``          |
            +---------------------------+-----------------------------------------------+
            | entity_type               | ``ScheduledEventEntityType``                  |
            +---------------------------+-----------------------------------------------+
            | image                     | ``Icon``                                      |
            +---------------------------+-----------------------------------------------+
            | name                      | `str`                                         |
            +---------------------------+-----------------------------------------------+
            | privacy_level             | ``PrivacyLevel``                              |
            +---------------------------+-----------------------------------------------+
            | sku_ids                   | `None`, `tuple` of `int`                      |
            +---------------------------+-----------------------------------------------+
            | start                     | `None`, `datetime`                            |
            +---------------------------+-----------------------------------------------+
            | status                    | ``ScheduledEventStatus``                      |
            +---------------------------+-----------------------------------------------+
        """
        old_attributes = {}
        
        self._update_image(data, old_attributes)
        
        channel_id = parse_channel_id(data)
        if self.channel_id != channel_id:
            old_attributes['channel_id'] = self.channel_id
            self.channel_id = channel_id
        
        description = parse_description(data)
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        end = parse_end(data)
        if self.end != end:
            old_attributes['end'] = self.end
            self.end = end
        
        entity_id = parse_entity_id(data)
        if self.entity_id != entity_id:
            old_attributes['entity_id'] = self.entity_id
            self.entity_id = entity_id
        
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        privacy_level = parse_privacy_level(data)
        if self.privacy_level is not privacy_level:
            old_attributes['privacy_level'] = self.privacy_level
            self.privacy_level = privacy_level
        
        sku_ids = parse_sku_ids(data)
        if self.sku_ids != sku_ids:
            old_attributes['sku_ids'] = self.sku_ids
            self.sku_ids = sku_ids
        
        start = parse_start(data)
        if self.start != start:
            old_attributes['start'] = self.start
            self.start = start
        
        status =  parse_status(data)
        if self.status is not status:
            old_attributes['status'] = self.status
            self.status = status
        
        
        entity_type = parse_entity_type(data)
        if self.entity_type is not entity_type:
            old_attributes['entity_type'] = self.entity_type
            self.entity_type = entity_type
        
        entity_metadata = parse_entity_metadata(data, entity_type)
        if self.entity_metadata != entity_metadata:
            old_attributes['entity_metadata'] = self.entity_metadata
            self.entity_metadata = entity_metadata
        
        return old_attributes
    
    
    def _update_counts_only(self, data):
        """
        Updates the scheduled event's count attributes only.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Scheduled event data.
        """
        try:
            user_count = data['user_count']
        except KeyError:
            pass
        else:
            self.user_count = user_count
        
    
    def __repr__(self):
        """Returns the guild event's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id = ', repr(self.id),
            ', name = ', repr(self.name),
            ', guild_id = ', repr(self.guild_id),
        ]
        
        entity_type = self.entity_type
        if entity_type is not ScheduledEventEntityType.none:
            repr_parts.append(', entity_type = ')
            repr_parts.append(entity_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(entity_type.value))
        
        
        status = self.status
        if status is not ScheduledEventStatus.none:
            repr_parts.append(', status = ')
            repr_parts.append(status.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(status.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the scheduled event's hash value."""
        stage_id = self.id
        if stage_id:
            return stage_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns the scheduled event's hash value.
        This function is called when the scheduled event is partial.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # channel_id
        hash_value ^= self.channel_id
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(self.description)
        
        # end
        end = self.end
        if (end is not None):
            hash_value ^= hash(self.end)
        
        # entity_metadata
        hash_value ^= hash(self.entity_metadata)
        
        # entity_type
        hash_value ^= hash(self.entity_type)
        
        # image
        hash_value ^ hash(self.image)
        
        # name
        name = self.name
        if (name != description):
            hash_value ^= hash(name)
        
        hash_value ^= hash(self.privacy_level) << 4
        # scheduled_event_id | internal
        
        # start
        start = self.start
        if (start is not None):
            hash_value ^= hash(self.start)
        
        return hash_value
    

    def __eq__(self, other):
        """Returns whether the two scheduled events are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two scheduled events are not equal."""
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
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # end
        if self.end != other.end:
            return False
        
        # entity_type
        if self.entity_type != other.entity_type:
            return False
        
        # entity_metadata
        if self.entity_metadata != other.entity_metadata:
            return False
        
        # image
        if self.image != other.image:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # privacy_level
        if self.privacy_level is not other.privacy_level:
            return False
        
        # start
        if self.start != other.start:
            return False
        
        # status
        if self.status is not other.status:
            return False
        
        return True
        
        
    @classmethod
    def _create_empty(cls, scheduled_event_id):
        """
        Creates a scheduled event instance with its attributes set to their default values.
        
        Parameters
        ----------
        scheduled_event_id : `int`
            The stage's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.channel_id = 0
        self.creator = ZEROUSER
        self.description = None
        self.end = None
        self.entity_id = 0
        self.entity_metadata = ScheduledEventEntityMetadataBase._create_empty()
        self.entity_type = ScheduledEventEntityType.none
        self.guild_id = 0
        self.id = scheduled_event_id
        self.image_hash = 0
        self.image_type = ICON_TYPE_NONE
        self.name = ''
        self.privacy_level = PrivacyLevel.guild_only
        self.start = None
        self.sku_ids = None
        self.status = ScheduledEventStatus.none
        self.user_count = 0
        return self
    
    
    @classmethod
    def precreate(cls, scheduled_event_id, *, entity_type = ..., **keyword_parameters):
        """
        Precreates the scheduled event by creating a partial one with the given parameters.
        When the scheduled event is loaded the precreated one will be picked up. If an already existing scheduled event
        would be precreated, returns that instead and updates that only, if that is partial.
        
        Parameters
        ----------
        scheduled_event_id : `int`
            The scheduled event's identifier.
        entity_type : ``ScheduledEventEntityType``, `int`, Optional (Keyword only)
            To which type of entity the event is bound to.
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the scheduled event.
        
        Other Parameters
        ----------------
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `channel`.
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The event's stage's channel or its identifier.
        creator : ``ClientUserBase``, Optional (Keyword only)
            The event's creator.
        description : `None`, `str`, Optional (Keyword only)
            Description of the event.
        end : `None`, `datetime`, Optional (Keyword only)
            The scheduled end time of the event.
        entity_id : `int`, Optional (Keyword only)
            The event's entity's identifier.
        entity_type : ``ScheduledEventEntityType``, `int`, Optional (Keyword only)
            To which type of entity the event is bound to.
        guild : `int`, ``Guild``, Optional (Keyword only)
            Alternative for `guild_id`.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The scheduled event's guild or its identifier.
        image : `None`, ``Icon``, `str`, Optional (Keyword only)
            The schedule event's image.
        location : `None`, `str`, Optional (Keyword only)
            The place where the event will take place.
        name : `str`
            The event's name.
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the event.
        sku_ids : `None`, `iterable` of `int`, Optional (Keyword only)
            Stock keeping unit identifiers used at the event.
        speaker_ids : `None`, `iterable` of (`int`, `ClientUserBase`), Optional (Keyword only)
            The speakers' identifier of the stage channel.
        start : `None`, `datetime`, Optional (Keyword only)
            The scheduled start time of the event.
        status : ``ScheduledEventStatus``, Optional (Keyword only)
            The status of the event.
        user_count : `int`, Optional (Keyword only)
            Users subscribed to the event.
        
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
        scheduled_event_id = validate_id(scheduled_event_id)

        if (entity_type is not ...) or keyword_parameters:
            processed = []
                
            # entity_type
            if entity_type is ...:
                entity_type = guess_scheduled_event_entity_type_from_keyword_parameters(keyword_parameters)
            else:
                entity_type = validate_entity_type(entity_type)
            processed.append(('entity_type', entity_type))
            
            # keyword_parameters
            extra = process_precreate_parameters(keyword_parameters, PRECREATE_FIELDS, processed)
            
            # entity_metadata
            entity_metadata_type = entity_type.metadata_type
            if entity_metadata_type is not ScheduledEventEntityMetadataBase:
                if extra is None:
                    entity_metadata = entity_metadata_type._create_empty()
                else:
                    entity_metadata = entity_metadata_type.from_keyword_parameters(extra)
                processed.append(('entity_metadata', entity_metadata))
            
            # raise on extra
            if (extra is not None) and extra:
                raise TypeError(
                    f'Extra or unused keyword parameters: {keyword_parameters!r}.'
                )
        
        else:
            processed = None
        
        try:
            self = SCHEDULED_EVENTS[scheduled_event_id]
        except KeyError:
            self = cls._create_empty(scheduled_event_id)
            SCHEDULED_EVENTS[scheduled_event_id] = self
        else:
            if not self.partial:
                return self
        
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    def copy(self):
        """
        Copies the scheduled event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.channel_id = self.channel_id
        new.creator = ZEROUSER
        new.description = self.description
        new.end = self.end
        new.entity_id = 0
        new.entity_metadata = self.entity_metadata.copy()
        new.entity_type = self.entity_type
        new.guild_id = 0
        new.id = 0
        new.image = self.image
        new.name = self.name
        new.privacy_level = self.privacy_level
        new.start = self.start
        new.sku_ids = None
        new.status = self.status
        new.user_count = 0
        return new
    
    
    def copy_with(
        self,
        channel_id = ...,
        description = ...,
        end = ...,
        entity_type = ...,
        image = ...,
        name = ...,
        privacy_level = ...,
        start = ...,
        status = ...,
        **keyword_parameters,
    ):
        """
        Copies the scheduled event with the given fields.
        
        Parameters
        ----------
        channel_id : `int`, ``Channel``, Optional (Keyword only)
            The event's stage's channel or its identifier.
        description : `None`, `str`, Optional (Keyword only)
            Description of the event.
        end : `None`, `datetime`, Optional (Keyword only)
            The scheduled end time of the event.
        entity_type : ``ScheduledEventEntityType``, `int`, Optional (Keyword only)
            To which type of entity the event is bound to.
        image : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The schedule event's image.
        name : `str`
            The event's name.
        privacy_level : ``PrivacyLevel``, `int`, Optional (Keyword only)
            The privacy level of the event.
        start : `None`, `datetime`, Optional (Keyword only)
            The scheduled start time of the event.
        status : ``ScheduledEventStatus``, Optional (Keyword only)
            The status of the event.
        **keyword_parameters : Keyword parameters
            Additional keyword parameters passed to the entity metadata.
        
        Other Parameters
        ----------------
        location : `None`, `str`, Optional (Keyword only)
            The place where the event will take place.
        speaker_ids : `None`, `iterable` of (`int`, `ClientUserBase`), Optional (Keyword only)
            The speakers' identifier of the stage channel.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's value is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's type is incorrect.
        """
        # channel_id
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # end
        if end is ...:
            end = self.end
        else:
            end = validate_end(end)
        
        # entity_type
        if entity_type is ...:
            entity_type = guess_scheduled_event_entity_type_from_keyword_parameters(keyword_parameters)
            if (entity_type is ScheduledEventEntityType.none):
                entity_type = self.entity_type
        else:
            entity_type = validate_entity_type(entity_type)
        
        # image
        if image is ...:
            image = self.image
        else:
            image = type(self).image.validate_icon(image, allow_data = True)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # privacy_level
        if privacy_level is ...:
            privacy_level = self.privacy_level
        else:
            privacy_level = validate_privacy_level(privacy_level)
        
        # start
        if start is ...:
            start = self.start
        else:
            start = validate_start(start)
        
        # status
        if status is ...:
            status = self.status
        else:
            status = validate_status(status)
        
        # entity_metadata
        entity_metadata = self.entity_metadata
        if (entity_type.metadata_type is type(entity_metadata)):
            entity_metadata = entity_metadata.copy_with_keyword_parameters(keyword_parameters)
        else:
            entity_metadata = entity_type.metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
    
        # Construct
        new = object.__new__(type(self))
        new.channel_id = channel_id
        new.creator = ZEROUSER
        new.description = description
        new.end = end
        new.entity_id = 0
        new.entity_metadata = entity_metadata
        new.entity_type = entity_type
        new.guild_id = 0
        new.id = 0
        new.image = image
        new.name = name
        new.privacy_level = privacy_level
        new.start = start
        new.sku_ids = None
        new.status = status
        new.user_count = 0
        return new
    
    
    url = property(module_urls.scheduled_event_url)
    
    
    @property
    def partial(self):
        """
        Returns whether the scheduled event is partial.
        
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
                    if self.id in guild.scheduled_events.keys():
                        return False
        
        return True
    
    
    @property
    def entity(self):
        """
        Returns the stage channel's entity if applicable.
        
        Returns
        -------
        entity : `None`, ``Channel``
        """
        entity_id = self.entity_id
        if entity_id:
            entity_type = self.entity_type
            if entity_type is ScheduledEventEntityType.none:
                entity = None
            elif entity_type is ScheduledEventEntityType.stage:
                entity = create_partial_channel_from_id(entity_id, ChannelType.guild_stage, self.guild_id)
            elif entity_type is ScheduledEventEntityType.voice:
                entity = create_partial_channel_from_id(entity_id, ChannelType.guild_voice, self.guild_id)
            else:
                entity = None
        else:
            entity = None
        
        return entity
    
    
    @property
    def channel(self):
        """
        Returns the event's channel if has any.
        
        Returns
        -------
        channel : `None`, ``Channel``
        """
        channel_id = self.channel_id
        if channel_id:
            return create_partial_channel_from_id(channel_id, ChannelType.unknown, self.guild_id)
    
    
    @property
    def guild(self):
        """
        Returns the event's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        return GUILDS.get(self.guild_id, None)
    
    
    @property
    def creator_id(self):
        """
        The event's creator's identifier.
        
        Returns
        -------
        user_id : `int`
        """
        return self.creator.id
    
    
    def iter_sku_ids(self):
        """
        Iterates over the stock keeping unit identifiers used at the event.
        
        This method is an iterable generator.
        
        Yields
        ------
        sku_id : `int`
        """
        sku_ids = self.sku_ids
        if (sku_ids is not None):
            yield from sku_ids
