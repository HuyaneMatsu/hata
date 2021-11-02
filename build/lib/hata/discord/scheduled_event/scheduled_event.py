__all__ = ('ScheduledEvent', )

from ..bases import DiscordEntity, IconSlot
from ..core import SCHEDULED_EVENTS, CHANNELS, GUILDS
from ..channel import CHANNEL_TYPES, create_partial_channel_from_id
from ..utils import timestamp_to_datetime

from .preinstanced import ScheduledEventStatus, ScheduledEventEntityType, PrivacyLevel

class ScheduledEvent(DiscordEntity):
    """
    Attributes
    ----------
    id : `int`
        The scheduled event's identifier number.
    channel_id : `int`
        The stage channel id of the event.
        
        Defaults to `0` if not applicable.
    description : `None` or `str`
        Description of the event.
    entity_id : `int`
        The event's entity's type.
        
        Defaults to `0`.
    entity_type : ``ScheduledEventEntityType``
        To which type of entity the event is bound to.
    guild_id : `int`
        The respective event's identifier.
    entity_metadata : `None` or ``ScheduledEventMetadata`` instance
        Metadata about the target entity.
    image_type : ``IconType``
        The event's image's type.
    image_hash : `int`
        The event's image hash.
    name : `str`
        The event's name.
    privacy_level : ``PrivacyLevel``
        The privacy level of the event.
    end : `None` or `datetime`
        The scheduled end time of the event.
    start : `None` or `datetime`
        The scheduled start time of the event.
    send_start_notification : `bool`
        Whether start notification should be sent when the event is started.
    sku_ids : `tuple` of `int`
        Stock keeping unit identifiers used at the event.
    status : ``ScheduledEventStatus``
        The status of the event.
    user_count : `int`
        Users subscribed to the event.
    """
    __slots__ = ('channel_id', 'description', 'entity_id', 'entity_metadata', 'entity_type', 'guild_id', 'name',
        'privacy_level', 'end', 'start', 'send_start_notification', 'sku_ids', 'status', 'user_count' )
    
    image = IconSlot('image', 'image', None, None, add_updater=False)
    
    def __new__(cls, data):
        """
        Creates a new ``ScheduledEvent`` instance from the received data.
        
        Ift he instance already exists, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild event data.
        """
        event_id = int(data['id'])
        
        try:
            self = SCHEDULED_EVENTS[event_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = event_id
            SCHEDULED_EVENTS[event_id] = self
            
            self._set_attributes(data)
        else:
            self._update_counts_only(data)
        
        return self
    
    
    def _set_attributes(self, data):
        """
        Sets the event's attributes form the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Scheduled event data.
        """
        self.user_count = data.get('user_count', 0)
        
        entity_type = ScheduledEventEntityType.get(data['entity_type'])
        self.entity_type = entity_type
        self.privacy_level = PrivacyLevel.get(data['privacy_level'])
        
        channel_id = data.get('channel_id', None)
        if channel_id is None:
            channel_id = 0
        else:
            channel_id = int(channel_id)
        self.channel_id = channel_id
        
        self.guild_id = int(data['guild_id'])
        
        entity_metadata_data = data.get('entity_metadata', None)
        if entity_metadata_data is None:
            entity_metadata = None
        else:
            metadata_type = entity_type.metadata_type
            if (metadata_type is None):
                entity_metadata = None
            else:
                entity_metadata = metadata_type.from_data(entity_metadata_data)
        
        self.entity_metadata = entity_metadata
        
        entity_id = data.get('entity_id', None)
        if entity_id is None:
            entity_id = 0
        else:
            entity_id = int(entity_id)
        self.entity_id = entity_id
        
        self._update_attributes(data)
    
    def _update_attributes(self, data):
        """
        Updates the attributes of the scheduled event.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Scheduled event data.
        """
        description = data.get('description', None)
        if (description is not None) and (not description):
            description = None
        
        self.description = description
        
        self.status = ScheduledEventStatus.get(data['status'])
        
        self.name = data['name']
        
        self._set_image(data)
        
        end = data.get('scheduled_end_time', None)
        if (end is not None):
            end = timestamp_to_datetime(end)
        self.end = end
        
        start = data.get('scheduled_start_time', None)
        if (start is not None):
            start = timestamp_to_datetime(start)
        self.start = start
        
        sku_ids = data.get('sku_ids')
        if (sku_ids is None) or (not sku_ids):
            sku_ids = None
        else:
            sku_ids = tuple(sorted(int(sku_id) for sku_id in sku_ids))
        self.sku_ids = sku_ids
        
        self.send_start_notification = data.get('send_start_notification', False)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the attributes of the scheduled event and returns the changed ones within an `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Scheduled event data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            The updated attributes.
            
            The returned dictionary might contain the following items:
            
            +---------------------------+-------------------------------+
            | Key                       | Value                         |
            +===========================+===============================+
            | description               | `None` or `str`               |
            +---------------------------+-------------------------------+
            | image                     | ``Icon``                      |
            +---------------------------+-------------------------------+
            | name                      | `str`                         |
            +---------------------------+-------------------------------+
            | send_start_notification   | `bool`                        |
            +---------------------------+-------------------------------+
            | end                       | `None` or `datetime`          |
            +---------------------------+-------------------------------+
            | start                     | `None` or `datetime`          |
            +---------------------------+-------------------------------+
            | sku_ids                   | `None` or `tuple` of `int`    |
            +---------------------------+-------------------------------+
            | status                    | ``ScheduledEventStatus``      |
            +---------------------------+-------------------------------+
        """
        old_attributes = {}
        
        description = data.get('description', None)
        if (description is not None) and (not description):
            description = None
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        status = ScheduledEventStatus.get(data['status'])
        if self.status is not status:
            old_attributes['status'] = self.status
            self.status = status
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        self._update_image(data, old_attributes)
        
        end = data.get('scheduled_end_time', None)
        if (end is not None):
            end = timestamp_to_datetime(end)
        if self.end != end:
            old_attributes['end'] = self.end
            self.end = end
        
        start = data.get('scheduled_start_time', None)
        if (start is not None):
            start = timestamp_to_datetime(start)
        if self.start != start:
            old_attributes['start'] = self.start
            self.start = start
        
        sku_ids = data.get('sku_ids')
        if (sku_ids is None) or (not sku_ids):
            sku_ids = None
        else:
            sku_ids = tuple(sorted(int(sku_id) for sku_id in sku_ids))
        if self.sku_ids != sku_ids:
            old_attributes['sku_ids'] = self.sku_ids
            self.sku_ids = sku_ids
        
        send_start_notification = data.get('send_start_notification', False)
        if self.send_start_notification != send_start_notification:
            old_attributes['send_start_notification'] = self.send_start_notification
            self.send_start_notification = send_start_notification
        
        return old_attributes
    
    def update_counts_only(self, data):
        """
        Updates the scheduled event's count attributes only.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
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
            ' id=', repr(self.id),
            ', name=', repr(self.name),
            ', guild_id', repr(self.guild_id),
        ]
        
        entity_type = self.entity_type
        if entity_type is not ScheduledEventEntityType.none:
            repr_parts.append(', entity_type=')
            repr_parts.append(entity_type.name)
            repr_parts.append(' (')
            repr_parts.append(repr(entity_type.value))
            repr_parts.append(')')
        
        
        status = self.status
        if status is not ScheduledEventStatus.none:
            repr_parts.append(', status=')
            repr_parts.append(status.name)
            repr_parts.append(' (')
            repr_parts.append(repr(status.value))
            repr_parts.append(')')
        
        repr_parts.append('>')
        return ''.join(repr_parts)

    
    @property
    def entity(self):
        """
        Returns the stage channel's entity if applicable.
        
        Returns
        -------
        entity : `None` or ``ChannelStage``
        """
        entity_id = self.entity_id
        if entity_id:
            entity_type = self.entity_type
            if entity_type is ScheduledEventEntityType.none:
                entity = None
            elif entity_type is ScheduledEventEntityType.stage:
                entity = create_partial_channel_from_id(entity_id, CHANNEL_TYPES.guild_stage, self.guild_id)
            elif entity_type is ScheduledEventEntityType.voice:
                entity = create_partial_channel_from_id(entity_id, CHANNEL_TYPES.guild_voice, self.guild_id)
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
        channel : `None` or ``ChannelStage``
        """
        channel_id = self.channel_id
        if channel_id:
            return CHANNELS.get(channel_id, None)
    
    
    @property
    def guild(self):
        """
        Returns the event's guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        return GUILDS.get(self.guild_id, None)


