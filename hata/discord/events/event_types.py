__all__ = ('GuildUserChunkEvent', 'VoiceServerUpdateEvent',)

from scarletio import copy_docs, set_docs

from ...env import CACHE_PRESENCE

from ..bases import EventBase
from ..core import GUILDS
from ..user import User


class GuildUserChunkEvent(EventBase):
    """
    Represents a processed `GUILD_MEMBERS_CHUNK` dispatch event.
    
    Attributes
    ----------
    count : `int`
        The total number of chunk responses what Discord sends for the respective gateway.
    guild_id : `int`
        The guild's identifier, what received the user chunk.
    index : `int`
        The index of the received chunk response (0 <= index < count).
    nonce : `None`, `str`
        A nonce to identify guild user chunk response.
    users : `list` of ``ClientUserBase``
        The received users.
    """
    __slots__ = ('count', 'guild_id', 'index', 'nonce', 'users')
    
    if CACHE_PRESENCE:
        def __new__(cls, data):
            guild_id = int(data['guild_id'])
            guild = GUILDS.get(guild_id, None)
            
            users = []
            for user_data in data['members']:
                user = User(user_data, guild)
                users.append(user)
            
            try:
                presence_datas = data['presences']
            except KeyError:
                pass
            else:
                if (guild is not None):
                    guild._apply_presences(presence_datas)
            
            self = object.__new__(GuildUserChunkEvent)
            self.guild_id = guild_id
            self.users = users
            self.nonce = data.get('nonce', None)
            self.index = data.get('chunk_index', 0)
            self.count = data.get('chunk_count', 1)
            
            return self
    
    else:
        def __new__(cls, data):
            guild_id = int(data['guild_id'])
            guild = GUILDS.get(guild_id, None)
            
            users = []
            for user_data in data['members']:
                user = User(user_data, guild)
                users.append(user)
            
            self = object.__new__(GuildUserChunkEvent)
            self.guild_id = guild_id
            self.users = users
            self.nonce = data.get('nonce', None)
            self.index = data.get('chunk_index', 0)
            self.count = data.get('chunk_count', 1)
            
            return self
    
    set_docs(__new__,
        """
        Creates a new guild user chunk event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild user chunk event data.
        """
    )
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' guild_id=')
        repr_parts.append(repr(self.guild_id))
        
        count = self.count
        if count != 1:
            repr_parts.append(', index=')
            repr_parts.append(repr(self.index))
            repr_parts.append('/')
            repr_parts.append(repr(count))
        
        repr_parts.append(', user count=')
        repr_parts.append(repr(len(self.users)))
        
        nonce = self.nonce
        if (nonce is not None):
            repr_parts.append(' nonce=')
            repr_parts.append(repr(nonce))
        
        repr_parts.append('>')
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 5
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.users
        yield self.nonce
        yield self.index
        yield self.count
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.count != other.count:
            return False
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.index != other.index:
            return False
        
        if self.nonce != other.nonce:
            return False
        
        if self.users != other.users:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # count
        hash_value ^= self.count
        
        # guild_id
        hash_value ^= self.guild_id
        
        # index
        hash_value ^= (self.index << 12)
        
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


class VoiceServerUpdateEvent(EventBase):
    """
    Represents a `VOICE_SERVER_UPDATE` event.
    
    Attributes
    ----------
    endpoint : `None`, `str`
        The voice server's host.
    guild_id : `int`
        The respective guild's identifier.
    token : `None`, `str`
        Voice connection token.
    """
    __slots__ = ('endpoint', 'guild_id', 'token')
    
    def __new__(cls, data):
        """
        Creates a new voice server update event from the given voice server update data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice server update data.
        """
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.endpoint = data.get('endpoint', None)
        self.token = data.get('token', None)
        
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__,]
        
        repr_parts.append(' guild_id=')
        repr_parts.append(repr(self.guild_id))
        
        endpoint = self.endpoint
        if (endpoint is not None):
            repr_parts.append(', endpoint=')
            repr_parts.append(repr(endpoint))
        
        token = self.token
        if (token is not None):
            repr_parts.append(', token=')
            repr_parts.append(repr(self.token))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.endpoint
        yield self.token
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.endpoint != other.endpoint:
            return False
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.token != other.token:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # endpoint
        endpoint = self.endpoint
        if (endpoint is not None):
            hash_value ^= hash(endpoint)
        
        # guild_id
        hash_value ^= self.guild_id
        
        # token
        token = self.token
        if (token is not None):
            hash_value ^= hash(token)
        
        return hash_value
