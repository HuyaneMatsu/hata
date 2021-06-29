__all__ = ('MessageReference',)

from ..core import GUILDS, MESSAGES, CHANNELS


class MessageReference:
    """
    A cross guild reference used as a ``Message``'s `.cross_reference` at crosspost messages.
    
    Attributes
    ----------
    _channel : `object`, `None` or ``ChannelBase``
        Internal slot used by the ``.channel`` property.
    _guild : `object`, `None` or ``Guild``
        Internal used by the ``.guild`` property.
    _message : `object`. `None`, ``Message``
        Internal slot used by the ``.message`` property.
    channel_id : `int`
        The referenced message's channel's id. Might be set as `0`.
    guild_id : `int`
        The referenced message's guild's id. Might be set as `None`.
    message_id : `int`
        The referenced message's id. Might be set as `0`.
    """
    __slots__ = ('_channel', '_message', '_guild', 'channel_id', 'guild_id', 'message_id',)
    def __new__(cls, data):
        """
        Creates a ``MessageReference`` from message reference data included inside of a ``Message``'s.
        
        If the message is loaded already, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message reference data.
        
        Returns
        -------
        self / message : ``MessageReference`` or ``Message``
        """
        message_id = data.get('message_id', None)
        if message_id is None:
            message_id = 0
        else:
            message_id = int(message_id)
            try:
                message = MESSAGES[message_id]
            except KeyError:
                pass
            else:
                return message
        
        channel_id = data.get('channel_id', None)
        if channel_id is None:
            channel_id = None
        else:
            channel_id = int(channel_id)
        
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        self = object.__new__(cls)
        
        self.message_id = message_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        self._message = ...
        self._channel = ...
        self._guild = ...
        
        return self
    
    @property
    def channel(self):
        """
        Returns referenced message's channel if found.
        
        Returns
        -------
        channel : `None` or ``ChannelBase`` instance
        """
        channel = self._channel
        if channel is ...:
            channel_id = self.channel_id
            if channel_id:
                channel = CHANNELS.get(channel_id, None)
            else:
                channel = None
            
            self._channel = channel
        
        return channel
    
    @property
    def guild(self):
        """
        Returns referenced message's guild if found.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        guild = self.guild
        if guild is ...:
            guild_id = self.guild_id
            if guild_id:
                guild = GUILDS.get(guild_id, None)
            else:
                guild = None
            
            self._guild = guild
        
        return guild
    
    @property
    def message(self):
        """
        Returns referenced message if found.
        
        Returns
        -------
        message : `None` or ``Message``
        """
        message = self.message
        if message is ...:
            message_id = self.message_id
            if message_id:
                message = GUILDS.get(message_id, None)
            else:
                message = None
            
            self._message = message
        
        return message
    
    def __repr__(self):
        """Returns the representation of the message reference."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        message_id = self.message_id
        if message_id:
            repr_parts.append(' message_id=')
            repr_parts.append(repr(message_id))
            field_added = True
        else:
            field_added = False
        
        channel_id = self.channel_id
        if channel_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' channel_id=')
            repr_parts.append(repr(channel_id))
        
        guild_id = self.guild_id
        if guild_id:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' guild_id=')
            repr_parts.append(repr(guild_id))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
