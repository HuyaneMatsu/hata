__all__ = ('message_relative_index',)

from collections import deque
from datetime import datetime
from time import time as current_time

from scarletio import LOOP_TIME, WeakReferer

from ..core import KOKORO
from ..utils import DATETIME_FORMAT_CODE



# searches the relative index of a message in a list
def message_relative_index(messages, message_id):
    """
    Searches the relative index of the given message's id in a channel's message history. The returned index is
    relative, because if the message with the given is not found, it should be at that specific index, if it would be
    inside of the respective channel's message history.
    
    Parameters
    ----------
    messages : `deque` of ``Message``
        The message history of a channel.
    message_id : `int`
        A messages' id to search.
    
    Returns
    -------
    index : `int`
    """
    bot = 0
    top = len(messages)
    while True:
        if bot < top:
            half = (bot + top) >> 1
            if messages[half].id > message_id:
                bot = half + 1
            else:
                top = half
            continue
        break
    
    return bot


class MessageHistoryCollector:
    """
    Attributes
    ----------
    channel_reference : ``WeakReferer`` to ``Channel``
        Reference to the parent channel.
    delay : `float`
        Additional message collection delay.
    handle : `None`, ``TimerHandle``
        Handle calling the history collector.
    """
    __slots__ = ('channel_reference', 'delay', 'handle', )
    
    def __new__(cls, channel, when):
        """
        Creates a new ``MessageHistoryCollector
        """
        self = object.__new__(cls)
        self.channel_reference = WeakReferer(channel)
        self.delay = 0.0
        self.handle = KOKORO.call_at(when, self)
        return self
    
    
    def __call__(self):
        """
        Calls the collector, removing the respective channel's extra messages.
        
        If there is extra delay, moves collection time.
        """
        channel = self.channel_reference()
        if (channel is None):
            self.handle = None
        else:
            delay = self.delay
            if delay:
                self.delay = 0.0
                self.handle = KOKORO.call_at(delay, self)
            else:
                self.handle = None
                channel._message_history_collector = None
                channel._switch_to_limited()
    
    
    def cancel(self):
        """Stops the handler of the collector."""
        handle = self.handle
        if (handle is not None):
            self.handle = None
            handle.cancel()
    
    __del__ = cancel
    
    def add_delay(self, delay):
        """
        Adds delay to the channel history collector.
        
        Parameters
        ----------
        delay : `bool`
            Delay to add.
        """
        self.delay += delay
    
    def __repr__(self):
        """Returns the message history collector's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        handle = self.handle
        if handle is None:
            repr_parts.append(' cancelled')
        else:
            repr_parts.append(' scheduled: ')
            timestamp = datetime.utcfromtimestamp(current_time() + handle.when + self.delay - LOOP_TIME())
            repr_parts.append(timestamp.__format__(DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


# Do not call any functions from this if you dunno anything about them!
# The message history is basically sorted by message_id, what can be translated to real time.
# The newer messages are at the start, meanwhile the older ones at the end.
# Do not try to delete not existing message's id, or it will cause de-sync.
# Use pypy?

class MessageHistory:
    """
    Contains message logic for message-able channels.
    
    Attributes
    ----------
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _message_history_collector :  `None`, ``MessageHistoryCollector``
        Collector for the channel's message history.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reach it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    """
    __slots__ = ('_message_keep_limit', '_message_history_collector', 'message_history_reached_end', 'messages',)
    
    def __init__(self, message_keep_limit):
        """
        Creates a nwe message history instance with it's default values.
        
        Parameters
        ----------
        message_keep_limit : `int`
            The amount of messages to keep.
        """
        self.message_history_reached_end = False
        self._message_history_collector = None
        self._message_keep_limit = message_keep_limit
        self.messages = None
    
    
    def _set_message_keep_limit(self, message_keep_limit):
        """
        Sets the amount of messages to keep by the channel.
        
        Parameters
        ----------
        message_keep_limit : `int`
            The amount of messages to keep.
        """
        if self._message_keep_limit != message_keep_limit:
            if message_keep_limit == 0:
                new_messages = None
            else:
                old_messages = self.messages
                if old_messages is None:
                    new_messages = None
                else:
                    new_messages = deque(
                        (old_messages[i] for i in range(min(message_keep_limit, len(old_messages)))),
                        maxlen = message_keep_limit,
                    )
            
            self.messages = new_messages
            self._message_keep_limit = message_keep_limit
