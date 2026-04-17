__all__ = ('ScheduledEventOccasionOverwriteUpdateEvent',)

from ..scheduled_event_occasion_overwrite_create_event import ScheduledEventOccasionOverwriteCreateEvent


class ScheduledEventOccasionOverwriteUpdateEvent(ScheduledEventOccasionOverwriteCreateEvent):
    """
    Represents a `GUILD_SCHEDULED_EVENT_EXCEPTION_CREATE` event where the occasion overwrite already exists.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier where the event is for.
    
    occasion_overwrite : ``ScheduledEventOccasionOverwrite``
        The affected occasion overwrite.
    
    scheduled_event_id : `int`
        The scheduled event's identifier.
    """
    __slots__ = ()
