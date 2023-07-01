__all__ = ('ApplicationCommandCountUpdate',  'VoiceServerUpdateEvent', 'WebhookUpdateEvent',)

from scarletio import copy_docs

from ..application_command import ApplicationCommandTargetType
from ..bases import EventBase
from ..channel import ChannelType, create_partial_channel_from_id
from ..core import GUILDS


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
    
    Examples
    --------
    The event can be unpacked like:
    
    ```py
    guild_id, endpoint, token = event
    ```
    """
    __slots__ = ('endpoint', 'guild_id', 'token')
    
    def __new__(cls, data):
        """
        Creates a new voice server update event from the given voice server update data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
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
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        endpoint = self.endpoint
        if (endpoint is not None):
            repr_parts.append(', endpoint = ')
            repr_parts.append(repr(endpoint))
        
        token = self.token
        if (token is not None):
            repr_parts.append(', token = ')
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


class WebhookUpdateEvent(EventBase):
    """
    Represents a `WEBHOOKS_UPDATE` event.
    
    Attributes
    ----------
    channel_id : `int`
        The respective channel's identifier.
    guild_id : `int`
        The respective guild's identifier.
    
    Examples
    --------
    The event can be unpacked like:
    
    ```py
    guild_id, channel_id = event
    ```
    """
    __slots__ = ('channel_id', 'guild_id')
    
    def __new__(cls, data):
        """
        Creates a new webhook update event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Webhook update data.
        """
        channel_id = int(data['channel_id'])
        
        guild_id = data.get('guild_id', None)
        # non guild webhook check ??
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        self = object.__new__(cls)
        self.channel_id = channel_id
        self.guild_id = guild_id
        
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__,]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', channel_id = ')
        repr_parts.append(repr(self.channel_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.channel_id
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # channel_id
        hash_value ^= self.channel_id
        
        # guild_id
        hash_value ^= self.guild_id
        
        return hash_value
    
    
    @property
    def channel(self):
        """
        Returns the event's channel from cache.
        
        Returns
        -------
        channel : ``Channel``
        """
        return create_partial_channel_from_id(self.channel_id, ChannelType.unknown, self.guild_id)
    
    
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


class ApplicationCommandCountUpdate(EventBase):
    """
    Represents a `GUILD_APPLICATION_COMMAND_INDEX_UPDATE` event.
    
    Attributes
    ----------
    counts : `dict` of (``ApplicationCommandTargetType``, `int`) items
        The count of the application commands by target type.
    guild_id : `int`
        The respective guild's identifier.
    
    Examples
    --------
    The event can be unpacked like:
    
    ```py
    guild_id, channel_id = event
    ```
    """
    __slots__ = ('counts', 'guild_id')
    
    def __new__(cls, data):
        """
        Creates a new application command count update event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application command count update data.
        """
        raw_counts = data['application_command_counts']
        
        counts = {
            ApplicationCommandTargetType.get(int(application_command_target_type_string)): count
            for application_command_target_type_string, count in raw_counts.items()
        }
        
        guild_id = data.get('guild_id', None)
        # non guild check ??
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        self = object.__new__(cls)
        self.counts = counts
        self.guild_id = guild_id
        
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__,]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', counts = {')
        
        items = sorted(self.counts.items())
        item_count = len(items)
        if item_count:
            index = 0
            while True:
                application_command_target_type, count = items[index]
                repr_parts.append(application_command_target_type.name)
                repr_parts.append(': ')
                repr_parts.append(str(count))
                
                index += 1
                if index == item_count:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append('}')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.counts
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # counts
        if self.counts != other.counts:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # counts
        for application_command_target_type, count in self.counts.items():
            hash_value ^= application_command_target_type * count * count
        
        # guild_id
        hash_value ^= self.guild_id
        
        return hash_value
    
    
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
