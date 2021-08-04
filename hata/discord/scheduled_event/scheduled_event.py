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

