__all__ = ('ScheduledEventSubscribeEvent', 'ScheduledEventUnsubscribeEvent')

from scarletio import copy_docs

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
        Creates a new scheduled event (un)subscribe event from the given data.
        
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
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
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
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.scheduled_event_id
        yield self.user_id
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.scheduled_event_id != other.scheduled_event_id:
            return False
        
        if self.user_id != other.user_id:
            return False
        
        return True
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return self.guild_id ^ self.scheduled_event_id ^ self.user_id


class ScheduledEventUnsubscribeEvent(ScheduledEventSubscribeEvent):
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
    __slots__ = ()
