__all__ = ('ScheduledEventSubscribeEvent', 'ScheduledEventUnsubscribeEvent')

from ..bases import EventBase

class ScheduledEventSubscribeEvent(EventBase):
    """
    Represents a `GUILD_SCHEDULED_EVENT_USER_ADD` event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier, where the event will be.
    scheduled_event_id : `int`
        The scheduled event's identifier.
    user_id : `int`
        The identifier of the user, who subscribed to the event.
    """
    __slots__ = ('guild_id', 'scheduled_event_id', 'user_id', )
    
    def __new__(cls, data):
        """
        Creates a new scheduled event subscribe from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Scheduled event subscribe event data.
        """
        guild_id = int(data['guild_id'])
        scheduled_event_id = int(data['guild_scheduled_event_id'])
        user_id = int(data['user_id'])
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.scheduled_event_id = scheduled_event_id
        self.user_id = user_id
        return self
    
    
    def __repr__(self):
        """Returns the representation of the scheduled event subscribe event."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' guild_id=',
            repr(self.guild_id),
            ', scheduled_event_id=',
            repr(self.scheduled_event_id),
            ', user_id=',
            repr(self.scheduled_event_id),
            '>'
        ]
        
        return ''.join(repr_parts)
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    
    def __iter__(self):
        """
        Unpacks the scheduled event subscribe event.
        
        This method is a generator.
        """
        yield self.guild_id
        yield self.scheduled_event_id
        yield self.user_id


class ScheduledEventUnsubscribeEvent(EventBase):
    """
    Represents a `GUILD_SCHEDULED_EVENT_USER_REMOVE` event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier, where the event will be.
    scheduled_event_id : `int`
        The scheduled event's identifier.
    user_id : `int`
        The identifier of the user, who unsubscribed to the event.
    """
    __slots__ = ('guild_id', 'scheduled_event_id', 'user_id', )
    
    def __new__(cls, data):
        """
        Creates a new scheduled event unsubscribe from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Scheduled event unsubscribe event data.
        """
        guild_id = int(data['guild_id'])
        scheduled_event_id = int(data['guild_scheduled_event_id'])
        user_id = int(data['user_id'])
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.scheduled_event_id = scheduled_event_id
        self.user_id = user_id
        return self
    
    
    def __repr__(self):
        """Returns the representation of the scheduled event unsubscribe event."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' guild_id=',
            repr(self.guild_id),
            ', scheduled_event_id=',
            repr(self.scheduled_event_id),
            ', user_id=',
            repr(self.scheduled_event_id),
            '>'
        ]
        
        return ''.join(repr_parts)
    
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    
    def __iter__(self):
        """
        Unpacks the scheduled event unsubscribe event.
        
        This method is a generator.
        """
        yield self.guild_id
        yield self.scheduled_event_id
        yield self.user_id
