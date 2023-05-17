__all__ = ('ScheduledEventSubscribeEvent',)

from scarletio import copy_docs

from ...bases import EventBase
from ...core import GUILDS
from ...user import create_partial_user_from_id

from .fields import (
    parse_guild_id, parse_scheduled_event_id, parse_user_id, put_guild_id_into, put_scheduled_event_id_into,
    put_user_id_into, validate_guild_id, validate_scheduled_event_id, validate_user_id
)


class ScheduledEventSubscribeEvent(EventBase):
    """
    Represents a `GUILD_SCHEDULED_EVENT_USER_ADD` event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier where the event will be.
    scheduled_event_id : `int`
        The scheduled event's identifier.
    user_id : `int`
        The identifier of the user, who subscribed to the event.
    """
    __slots__ = ('guild_id', 'scheduled_event_id', 'user_id', )
    
    
    def __new__(cls, *, guild_id = ..., scheduled_event_id = ..., user_id = ...):
        """
        Creates a new scheduled event (un)subscribe event.
        
        Parameters
        ----------
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild or its identifier where the event will be.
        scheduled_event_id : `int`, ``ScheduledEvent``, Optional (Keyword only)
            The scheduled event or its identifier.
        user_id : `int` ``ClientUserBase``, Optional (Keyword only)
            The user or their their identifier who subscribed to the event.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # scheduled_event_id
        if scheduled_event_id is ...:
            scheduled_event_id = 0
        else:
            scheduled_event_id = validate_scheduled_event_id(scheduled_event_id)
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.scheduled_event_id = scheduled_event_id
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new scheduled event (un)subscribe event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Scheduled event subscribe event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.guild_id = parse_guild_id(data)
        self.scheduled_event_id = parse_scheduled_event_id(data)
        self.user_id = parse_user_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the scheduled event subscribe event.
        
        Parameters
        ----------
        defaults : `bool`
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_guild_id_into(self.guild_id, data, defaults)
        put_scheduled_event_id_into(self.scheduled_event_id, data, defaults)
        put_user_id_into(self.user_id, data, defaults)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' guild_id = ',
            repr(self.guild_id),
            ', scheduled_event_id = ',
            repr(self.scheduled_event_id),
            ', user_id = ',
            repr(self.user_id),
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
    

    def copy(self):
        """
        Copies the scheduled event (un)subscribe event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.guild_id = self.guild_id
        new.scheduled_event_id = self.scheduled_event_id
        new.user_id = self.user_id
        return new
    
    
    def copy_with(self, guild_id = ..., scheduled_event_id = ..., user_id = ...):
        """
        Copies the scheduled event (un)subscribe event with the given fields.
        
        Parameters
        ----------
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild or its identifier where the event will be.
        scheduled_event_id : `int`, ``ScheduledEvent``, Optional (Keyword only)
            The scheduled event or its identifier.
        user_id : `int` ``ClientUserBase``, Optional (Keyword only)
            The user or their their identifier who subscribed to the event.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # scheduled_event_id
        if scheduled_event_id is ...:
            scheduled_event_id = self.scheduled_event_id
        else:
            scheduled_event_id = validate_scheduled_event_id(scheduled_event_id)
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        new = object.__new__(type(self))
        new.guild_id = guild_id
        new.scheduled_event_id = scheduled_event_id
        new.user_id = user_id
        return new
    
    
    @property
    def guild(self):
        """
        Returns the scheduled event subscribe event's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def user(self):
        """
        Returns the user who subscribed to the event.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)
