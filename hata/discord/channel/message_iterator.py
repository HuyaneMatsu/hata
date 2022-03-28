__all__ = ('MessageIterator', )

from ..bases import maybe_snowflake
from ..core import CHANNELS
from ..exceptions import DiscordException, ERROR_CODES
from ..permission.permission import PERMISSION_MASK_READ_MESSAGE_HISTORY

from .channel import Channel


# sounds funny, but this is a class the chunk_size is 99, because it means 1 request for _load_messages_till

class MessageIterator:
    """
    An asynchronous message iterator over the given text channel.
    
    Attributes
    ----------
    _index : `int`
        The index of the message, what will be yielded.
    _can_read_history : `bool`
        Tells the message iterator, whether it's client can read the history if it's channel.
    channel : ``Channel``
        The channel, what's messages the message iterator will iterates over.
    chunk_size : `int`
        The amount of messages, what the message iterator will extend it's channel's message history, each time, the
        loaded messages are exhausted.
    client : ``Client``
        The client, who will do the api requests for requesting more messages.
    """
    __slots__ = ('_can_read_history', '_index', 'channel', 'chunk_size', 'client',)
    
    async def __new__(cls, client, channel, chunk_size=99):
        """
        Creates a message iterator.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will do the api requests for requesting more messages.
        channel : ``Channel``, `int`
            The channel, what's messages the message iterator will iterates over.
        chunk_size : `int`, Optional
            The amount of messages, what the message iterator will extend it's channel's message history, each time,
            the loaded messages are exhausted. Limited to `97` as a maximal value.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `chunk_size` was not given as `int`.
            - If `chunk_size` is out of range [1:].
        """
        if __debug__:
            if not isinstance(chunk_size, int):
                raise AssertionError(
                    f'`chunk_size` can be `int`, got {chunk_size.__class__.__name__}; {chunk_size!r}.'
                )
            
            if chunk_size < 1:
                raise AssertionError(
                    f'`chunk_size` is out from the expected [0:] range, got {chunk_size!r}.'
                )
        
        if chunk_size > 99:
            chunk_size = 99
        
        if isinstance(channel, Channel):
            pass
        else:
            channel_id = maybe_snowflake(channel)
            if channel_id is None:
                raise TypeError(
                    f'`channel` can be `{Channel.__name__}`, got '
                    f'{channel.__class__.__name__}; {channel!r}.'
                )
            
            channel = CHANNELS.get(channel_id, None)
            
            if channel is None:
                try:
                    messages = await client.message_get_chunk_from_zero(channel_id, 100)
                except BaseException as err:
                    if isinstance(err, DiscordException) and err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                    ):
                        pass
                    
                    else:
                        raise
                else:
                    if messages:
                        channel = messages[0].channel
                    else:
                        channel = None
        
        self = object.__new__(cls)
        self.client = client
        self.channel = channel
        self.chunk_size = chunk_size
        self._index = 0
        self._can_read_history = channel.cached_permissions_for(client) & PERMISSION_MASK_READ_MESSAGE_HISTORY
        return self
    
    def __aiter__(self):
        """Returns self and resets the `.index`."""
        self._index = 0
        return self
    
    async def __anext__(self):
        """
        Yields the next message of the iterator's channel.
        
        This method is a coroutine.
        """
        channel = self.channel
        if (channel is None):
            raise StopAsyncIteration
        
        index = self._index
        messages = channel.messages
        if (messages is not None) and (len(messages) > index):
            self._index = index + 1
            return channel.messages[index]
        
        if channel.message_history_reached_end or (not self._can_read_history):
            raise StopAsyncIteration
        
        try:
            await self.client._load_messages_till(channel, index + self.chunk_size)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                pass
            
            elif isinstance(err, DiscordException) and err.code in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # message's channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ERROR_CODES.cannot_message_user, # user has dm-s disallowed
            ):
                pass
            else:
                raise
        
        messages = channel.messages
        if (messages is not None) and (len(channel.messages) > index):
            self._index = index + 1
            return channel.messages[index]
        
        raise StopAsyncIteration
    
    
    def __repr__(self):
        """Returns the representation of the message iterator."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' of client ', self.client.full_name,
        ]
        
        channel = self.channel
        if (channel is not None):
            repr_parts.append(', at channel ')
            repr_parts.append(repr(channel.name))
            repr_parts.append(' (')
            repr_parts.append(repr(channel.id))
            repr_parts.append(')')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
