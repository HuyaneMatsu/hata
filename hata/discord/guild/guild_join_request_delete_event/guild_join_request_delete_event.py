__all__ = ('GuildJoinRequestDeleteEvent',)

from scarletio import copy_docs

from ...bases import EventBase
from ...core import GUILDS
from ...user import create_partial_user_from_id

from .fields import (
    parse_guild_id, parse_user_id, put_guild_id_into, put_user_id_into, validate_guild_id, validate_user_id
)


class GuildJoinRequestDeleteEvent(EventBase):
    """
    Represents a `GUILD_JOIN_REQUEST_DELETE` event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier where the event will be.
    user_id : `int`
        The user's identifier whos join request was deleted.
    """
    __slots__ = ('guild_id', 'user_id', )
    
    def __new__(cls, *, guild_id = ..., user_id = ...):
        """
        Creates a new guild join request delete event.
        
        Parameters
        ----------
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild or its identifier where the event will be.
        user_id : `int` ``ClientUserBase``, Optional (Keyword only)
            The user or their their identifier whos join request was deleted.
        
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
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild join request delete event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Guild join request delete event.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.guild_id = parse_guild_id(data)
        self.user_id = parse_user_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the guild join request delete event.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_guild_id_into(self.guild_id, data, defaults)
        put_user_id_into(self.user_id, data, defaults)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.user_id
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # guild_id
        hash_value ^= self.guild_id
        
        # user_id
        hash_value ^= self.user_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the guild join request delete event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.guild_id = self.guild_id
        new.user_id = self.user_id
        return new
    
    
    def copy_with(self, guild_id = ..., user_id = ...):
        """
        Copies the guild join request delete event with the given fields.
        
        Parameters
        ----------
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild or its identifier where the event will be.
        user_id : `int` ``ClientUserBase``, Optional (Keyword only)
            The user or their their identifier whos join request was deleted.
        
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
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        new = object.__new__(type(self))
        new.guild_id = guild_id
        new.user_id = user_id
        return new
    
    
    @property
    def guild(self):
        """
        Returns the guild join request delete event's guild.
        
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
        Returns the user whos join request was deleted.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)
