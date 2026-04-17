__all__ = ('GuildEnhancementEntitlementsCreateEvent',)

from scarletio import copy_docs

from ...bases import EventBase
from ...core import GUILDS

from .fields import (
    parse_guild_id, parse_entitlements, put_guild_id, put_entitlements, validate_guild_id, validate_entitlements
)


class GuildEnhancementEntitlementsCreateEvent(EventBase):
    """
    Represents a `GUILD_POWERUP_ENTITLEMENTS_CREATE` event.
    
    Attributes
    ----------
    entitlements : ``None | tuple<Entitlement>``
        The affected entitlements.
    
    guild_id : `int`
        The guild's identifier where the event is for.
    """
    __slots__ = ('entitlements', 'guild_id')
    
    def __new__(cls, *, entitlements = ..., guild_id = ...):
        """
        Creates a new guild enhancement entitlements create / delete event.
        
        Parameters
        ----------
        entitlements : ``None | iterable<Entitlement>``, Optional (Keyword only)
            The affected entitlements.
        
        guild_id : ``None | int | Guild``, Optional (Keyword only)
            The guild or its identifier where the event will be.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # entitlements
        if entitlements is ...:
            entitlements = None
        else:
            entitlements = validate_entitlements(entitlements)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # Construct
        self = object.__new__(cls)
        self.entitlements = entitlements
        self.guild_id = guild_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild enhancement entitlements create / delete event from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild enhancement entitlements create / delete event.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.entitlements = parse_entitlements(data)
        self.guild_id = parse_guild_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the guild enhancement entitlements create / delete event.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_entitlements(self.entitlements, data, defaults)
        put_guild_id(self.guild_id, data, defaults)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # entitlements
        repr_parts.append(' entitlements = ')
        repr_parts.append(repr(self.entitlements))
        
        # guild_id
        repr_parts.append(', guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.entitlements
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # entitlements
        if self.entitlements != other.entitlements:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # entitlements
        entitlements = self.entitlements
        if (entitlements is not None):
            hash_value ^= len(entitlements)
            for entitlement in entitlements:
                hash_value ^= hash(entitlement)
        
        # guild_id
        hash_value ^= self.guild_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the guild enhancement entitlements create / delete event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        # entitlements
        entitlements = self.entitlements
        if (entitlements is not None):
            entitlements = (*(entitlement.copy() for entitlement in entitlements),)
        
        new.entitlements = entitlements
        
        new.guild_id = self.guild_id
        return new
    
    
    def copy_with(self, *, entitlements = ..., guild_id = ...):
        """
        Copies the guild enhancement entitlements create / delete event with the given fields.
        
        Parameters
        ----------
        entitlements : ``None | iterable<Entitlement>``, Optional (Keyword only)
            The affected entitlements.
        
        guild_id : ``None | int | Guild``, Optional (Keyword only)
            The guild or its identifier where the event will be.
        
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
        # entitlements
        if entitlements is ...:
            entitlements = self.entitlements
            if (entitlements is not None):
                entitlements = (*(entitlement.copy() for entitlement in entitlements),)
        else:
            entitlements = validate_entitlements(entitlements)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # Construct
        new = object.__new__(type(self))
        new.entitlements = entitlements
        new.guild_id = guild_id
        return new
    
    
    @property
    def guild(self):
        """
        Returns the guild enhancement entitlements create / delete event's guild.
        
        Returns
        -------
        guild : ``None | Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def entitlement(self):
        """
        Returns the first entitlement of the event.
        
        Returns
        -------
        entitlement : ``None | Entitlement``
        """
        entitlements = self.entitlements
        if (entitlements is not None):
            return entitlements[0]
    
    
    def iter_entitlements(self):
        """
        Iterates over the entitlements of the event.
        
        This method is an iterable generator.
        
        Yields
        ------
        entitlement : ``Entitlement``
        """
        entitlements = self.entitlements
        if (entitlements is not None):
            yield from entitlements
