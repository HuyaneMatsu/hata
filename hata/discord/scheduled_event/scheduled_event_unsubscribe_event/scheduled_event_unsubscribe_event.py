__all__ = ('ScheduledEventUnsubscribeEvent',)

from ..scheduled_event_subscribe_event import ScheduledEventSubscribeEvent


class ScheduledEventUnsubscribeEvent(ScheduledEventSubscribeEvent):
    """
    Represents a `GUILD_SCHEDULED_EVENT_USER_REMOVE` event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier where the event will be.
    scheduled_event_id : `int`
        The scheduled event's identifier.
    user_id : `int`
        The identifier of the user, who unsubscribed to the event.
    """
    __slots__ = ()
