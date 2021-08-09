__all__ = ('ScheduledEvent', )

from ..bases import DiscordEntity
from ..core import SCHEDULED_EVENTS

from .preinstanced import ScheduledEventStatus, ScheduledEventEntityType, PrivacyLevel

class ScheduledEvent(DiscordEntity):
    """
    Attributes
    ----------
    id : `int`
        The scheduled event's identifier number.
    description : `None` or `str`
        Description of the event.
    entity_type : ``ScheduledEventEntityType``
        To which type of entity the event is bound to.
    privacy_level : ``PrivacyLevel``
        The privacy level of the event.
    send_start_notification : `bool`
        Whether start notification should be sent when the event is started.
    status : ``ScheduledEventStatus``
        The status of the event.
    """
    __slots__ = ('description', 'entity_type', 'privacy_level', 'send_start_notification', 'status')
    
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
        
        return self
    
    def _set_attributes(self, data):
        """
        Sets the event's attributes form the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild event data.
        """
        description = data.get('description', None)
        if (description is not None) and (not description):
            description = None
        
        self.description = description
        
        self.entity_type = ScheduledEventEntityType.get(data['entity_type'])
        self.privacy_level = PrivacyLevel.get(data['privacy_level'])
        self.send_start_notification = data.get('send_start_notification', False)
        self.status = ScheduledEventStatus.get(data['status'])
    
    def __repr__(self):
        """Returns the guild event's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id=', repr(self.id)
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
            repr_parts.append(', entity_type=')
            repr_parts.append(status.name)
            repr_parts.append(' (')
            repr_parts.append(repr(status.value))
            repr_parts.append(')')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
