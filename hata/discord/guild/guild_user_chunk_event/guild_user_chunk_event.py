__all__ = ('GuildUserChunkEvent',)

import warnings

from scarletio import copy_docs

from ...bases import EventBase
from ...core import GUILDS

from .fields import (
    parse_chunk_count, parse_chunk_index, parse_guild_id, parse_nonce, parse_users, put_chunk_count_into,
    put_chunk_index_into, put_guild_id_into, put_nonce_into, put_users_into, validate_chunk_count, validate_chunk_index,
    validate_guild_id, validate_nonce, validate_users
)


class GuildUserChunkEvent(EventBase):
    """
    Represents a processed `GUILD_MEMBERS_CHUNK` dispatch event.
    
    Attributes
    ----------
    chunk_count : `int`
        The total number of chunk responses what Discord sends for the respective gateway.
    chunk_index : `int`
        The chunk_index of the received chunk response (0 <= chunk_index < chunk_count).
    guild_id : `int`
        The guild's identifier, what received the user chunk.
    nonce : `None`, `str`
        A nonce to identify guild user chunk response.
    users : `list` of ``ClientUserBase``
        The received users.
    
    Examples
    --------
    The event can be unpacked like:
    
    ```py
    guild_id, users, nonce, chunk_index, chunk_count = event
    ```
    """
    __slots__ = ('chunk_count', 'chunk_index', 'guild_id', 'nonce', 'users')
    
    def __new__(cls, *, chunk_count = ..., chunk_index = ..., guild_id = ..., nonce = ..., users = ...):
        """
        Creates a new guild chunk event from the given parameters.
        
        Parameters
        ----------
        chunk_count : `int`, Optional (Keyword only)
            The total number of chunk responses what Discord sends for the respective gateway.
        chunk_index : `int`, Optional (Keyword only)
            The chunk_index of the received chunk response (0 <= chunk_index < chunk_count).
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild's identifier, what received the user chunk.
        nonce : `None`, `str`, Optional (Keyword only)
            A nonce to identify guild user chunk response.
        users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The received users.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # chunk_count
        if chunk_count is ...:
            chunk_count = 0
        else:
            chunk_count = validate_chunk_count(chunk_count)
        
        # chunk_index
        if chunk_index is ...:
            chunk_index = 0
        else:
            chunk_index = validate_chunk_index(chunk_index)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # nonce
        if nonce is ...:
            nonce = None
        else:
            nonce = validate_nonce(nonce)
        
        # users
        if users is ...:
            users = []
        else:
            users = validate_users(users)
        
        self = object.__new__(cls)
        self.chunk_count = chunk_count
        self.chunk_index = chunk_index
        self.guild_id = guild_id
        self.nonce = nonce
        self.users = users
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild user chunk event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Guild user chunk event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(GuildUserChunkEvent)
        self.chunk_index = parse_chunk_index(data)
        self.chunk_count = parse_chunk_count(data)
        self.guild_id = guild_id = parse_guild_id(data)
        self.nonce = parse_nonce(data)
        self.users = parse_users(data, guild_id)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the guild user chunk event into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_chunk_count_into(self.chunk_count, data, defaults)
        put_chunk_index_into(self.chunk_index, data, defaults)
        put_guild_id_into(self.guild_id, data, defaults)
        put_nonce_into(self.nonce, data, defaults)
        put_users_into(self.users, data, defaults, guild_id = self.guild_id)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        chunk_count = self.chunk_count
        if chunk_count != 1:
            repr_parts.append(', chunk_index = ')
            repr_parts.append(repr(self.chunk_index))
            repr_parts.append('/')
            repr_parts.append(repr(chunk_count))
        
        nonce = self.nonce
        if (nonce is not None):
            repr_parts.append(' nonce = ')
            repr_parts.append(repr(nonce))
        
        repr_parts.append(', user_count: ')
        repr_parts.append(repr(len(self.users)))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 5
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.users
        yield self.nonce
        yield self.chunk_index
        yield self.chunk_count
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.chunk_count != other.chunk_count:
            return False
        
        if self.chunk_index != other.chunk_index:
            return False
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.nonce != other.nonce:
            return False
        
        if self.users != other.users:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # chunk_count
        hash_value ^= self.chunk_count
        
        # chunk_index
        hash_value ^= (self.chunk_index << 12)
        
        # guild_id
        hash_value ^= self.guild_id
        
        # nonce
        nonce = self.nonce
        if (nonce is not None):
            hash_value ^= hash(nonce)
        
        # users
        users = self.users
        if users:
            hash_value ^= (len(users) << 24)
            
            for user in users:
                hash_value ^= user.id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the guild user chunk event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.chunk_count = self.chunk_count
        new.chunk_index = self.chunk_index
        new.guild_id = self.guild_id
        new.nonce = self.nonce
        new.users = [*self.users]
        return new
    
    
    def copy_with(self, *, chunk_count = ..., chunk_index = ..., guild_id = ..., nonce = ..., users = ...):
        """
        Copies the guild chunk event with the given fields.
        
        Parameters
        ----------
        chunk_count : `int`, Optional (Keyword only)
            The total number of chunk responses what Discord sends for the respective gateway.
        chunk_index : `int`, Optional (Keyword only)
            The chunk_index of the received chunk response (0 <= chunk_index < chunk_count).
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild's identifier, what received the user chunk.
        nonce : `None`, `str`, Optional (Keyword only)
            A nonce to identify guild user chunk response.
        users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The received users.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # chunk_count
        if chunk_count is ...:
            chunk_count = self.chunk_count
        else:
            chunk_count = validate_chunk_count(chunk_count)
        
        # chunk_index
        if chunk_index is ...:
            chunk_index = self.chunk_index
        else:
            chunk_index = validate_chunk_index(chunk_index)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # nonce
        if nonce is ...:
            nonce = self.nonce
        else:
            nonce = validate_nonce(nonce)
        
        # users
        if users is ...:
            users = [*self.users]
        else:
            users = validate_users(users)
        
        new = object.__new__(type(self))
        new.chunk_count = chunk_count
        new.chunk_index = chunk_index
        new.guild_id = guild_id
        new.nonce = nonce
        new.users = users
        return new
    
    
    @property
    def guild(self):
        """
        Returns the event's guild from cache.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def iter_users(self):
        """
        Iterates over the received users.
        
        This method is a generator.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        yield from self.users
    
    
    @property
    def index(self):
        warnings.warn(
            (
                f'`{self.__name__}.index` is deprecated and will be removed in 2023 December.'
                f'Please use `.chunk_index` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.chunk_index
    
    
    @property
    def count(self):
        warnings.warn(
            (
                f'`{self.__name__}.count` is deprecated and will be removed in 2023 December.'
                f'Please use `.chunk_count` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.chunk_count
