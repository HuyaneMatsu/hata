__all__ = ('GuildUserChunkEvent', 'VoiceServerUpdateEvent',)

from ...env import CACHE_PRESENCE

from ...backend.utils import set_docs

from ..bases import EventBase
from ..guild import Guild
from ..user import User
from ..core import GUILDS


class GuildUserChunkEvent(EventBase):
    """
    Represents a processed `GUILD_MEMBERS_CHUNK` dispatch event.
    
    Attributes
    ----------
    guild_id : `int`
        The guild's identifier, what received the user chunk.
    users : `list` of ``ClientUserBase``
        The received users.
    nonce : `None` or `str`
        A nonce to identify guild user chunk response.
    index : `int`
        The index of the received chunk response (0 <= index < count).
    count : `int`
        The total number of chunk responses what Discord sends for the respective gateway.
    """
    __slots__ = ('guild_id', 'users', 'nonce', 'index', 'count')
    
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
            self.guild = guild
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
    
    def __repr__(self):
        """Returns the representation of the guild user chunk event."""
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
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 5
    
    def __iter__(self):
        """
        Unpacks the guild user chunk event.
        
        This method is a generator.
        """
        yield self.guild_id
        yield self.users
        yield self.nonce
        yield self.index
        yield self.count


class VoiceServerUpdateEvent(EventBase):
    """
    Represents a `VOICE_SERVER_UPDATE` event.
    
    Attributes
    ----------
    endpoint : `None` or `str`
        The voice server's host.
    guild_id : `int`
        The respective guild's identifier.
    token : `str`
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
    
    def __repr__(self):
        """Returns the representation of the voice server update event."""
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
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """
        Unpacks the voice server update event.
        
        This method is a generator.
        """
        yield self.guild_id
        yield self.endpoint
        yield self.token
