__all__ = ('ScheduledEventOccasionOverwriteCreateEvent',)

from scarletio import copy_docs

from ...core import GUILDS, SCHEDULED_EVENTS
from ...bases import EventBase

from ..scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from .fields import (
    parse_guild_id, parse_occasion_overwrite, parse_scheduled_event_id, put_guild_id, put_occasion_overwrite,
    put_scheduled_event_id, validate_guild_id, validate_occasion_overwrite, validate_scheduled_event_id
)


class ScheduledEventOccasionOverwriteCreateEvent(EventBase):
    """
    Represents a `GUILD_SCHEDULED_EVENT_EXCEPTION_CREATE` event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier where the event is for.
    
    occasion_overwrite : ``ScheduledEventOccasionOverwrite``
        The affected occasion overwrite.
    
    scheduled_event_id : `int`
        The scheduled event's identifier.
    """
    __slots__ = ('guild_id', 'occasion_overwrite', 'scheduled_event_id')
    
    
    def __new__(cls, *, guild_id = ..., occasion_overwrite = ..., scheduled_event_id = ...):
        """
        Creates a new scheduled event occasion overwrite (create / update / delete) event.
        
        Parameters
        ----------
        guild_id : ˙`None | int | Guild``, Optional (Keyword only)
            The guild or its identifier where the event will be.
        
        occasion_overwrite : ``ScheduledEventOccasionOverwrite``, Optional (Keyword only)
            The affected occasion overwrite.
        
        scheduled_event_id : ``None | int | ScheduledEvent``, Optional (Keyword only)
            The scheduled event or its identifier.
        
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
        
        # occasion_overwrite
        if occasion_overwrite is ...:
            occasion_overwrite = ScheduledEventOccasionOverwrite.create_empty()
        else:
            occasion_overwrite = validate_occasion_overwrite(occasion_overwrite)
        
        # scheduled_event_id
        if scheduled_event_id is ...:
            scheduled_event_id = 0
        else:
            scheduled_event_id = validate_scheduled_event_id(scheduled_event_id)
        
        # Construct
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.occasion_overwrite = occasion_overwrite
        self.scheduled_event_id = scheduled_event_id
        return self
    
    
    @classmethod
    def from_fields(cls, guild_id, scheduled_event_id, occasion_overwrite):
        """
        Creates a scheduled event occasion overwrite (create / update / delete) event from the given already parsed fields.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's identifier where the event is for.
        
        scheduled_event_id : `int`
            The scheduled event's identifier.
        
        occasion_overwrite : ``ScheduledEventOccasionOverwrite``
            The affected occasion overwrite.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.occasion_overwrite = occasion_overwrite
        self.scheduled_event_id = scheduled_event_id
        return self
        
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new scheduled event occasion overwrite (create / update / delete) event from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Scheduled event cancellation event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.guild_id = parse_guild_id(data)
        self.occasion_overwrite = parse_occasion_overwrite(data)
        self.scheduled_event_id = parse_scheduled_event_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the scheduled event occasion overwrite event.
        
        Parameters
        ----------
        defaults : `bool`
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_guild_id(self.guild_id, data, defaults)
        put_occasion_overwrite(self.occasion_overwrite, data, defaults)
        put_scheduled_event_id(self.scheduled_event_id, data, defaults)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # scheduled_event_id
        repr_parts.append(', scheduled_event_id = ')
        repr_parts.append(repr(self.scheduled_event_id))
        
        # occasion_overwrite
        repr_parts.append(', occasion_overwrite = ')
        repr_parts.append(repr(self.occasion_overwrite))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.scheduled_event_id
        yield self.occasion_overwrite
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # occasion_overwrite
        if self.occasion_overwrite != other.occasion_overwrite:
            return False
        
        # scheduled_event_id
        if self.scheduled_event_id != other.scheduled_event_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return self.guild_id ^ self.scheduled_event_id ^ hash(self.occasion_overwrite)
    

    def copy(self):
        """
        Copies the scheduled event occasion overwrite (create / update / delete) event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.guild_id = self.guild_id
        new.occasion_overwrite = self.occasion_overwrite.copy()
        new.scheduled_event_id = self.scheduled_event_id
        return new
    
    
    def copy_with(self, *, guild_id = ..., occasion_overwrite = ..., scheduled_event_id = ...):
        """
        Copies the scheduled event occasion overwrite (create / update / delete) event with the given fields.
        
        Parameters
        ----------
        guild_id : ˙`None | int | Guild``, Optional (Keyword only)
            The guild or its identifier where the event will be.
        
        occasion_overwrite : ``ScheduledEventOccasionOverwrite``, Optional (Keyword only)
            The affected occasion overwrite.
        
        scheduled_event_id : ``None | int | ScheduledEvent``, Optional (Keyword only)
            The scheduled event or its identifier.
        
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
        
        # occasion_overwrite
        if occasion_overwrite is ...:
            occasion_overwrite = self.occasion_overwrite
        else:
            occasion_overwrite = validate_occasion_overwrite(occasion_overwrite)
        
        # scheduled_event_id
        if scheduled_event_id is ...:
            scheduled_event_id = self.scheduled_event_id
        else:
            scheduled_event_id = validate_scheduled_event_id(scheduled_event_id)
        
        # Construct
        new = object.__new__(type(self))
        new.guild_id = guild_id
        new.occasion_overwrite = occasion_overwrite
        new.scheduled_event_id = scheduled_event_id
        return new
    
    
    @property
    def scheduled_event(self):
        """
        Returns the scheduled event.
        
        Returns
        -------
        scheduled_event : ``None | ScheduledEvent``
        """
        return SCHEDULED_EVENTS.get(self.scheduled_event_id, None)
    
    
    @property
    def guild(self):
        """
        Returns the scheduled event occasion overwrite event's guild.
        
        Returns
        -------
        guild : ``None | Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
