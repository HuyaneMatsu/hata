__all__ = ('ChannelTextBase', 'message_relative_index',)

from collections import deque
from time import time as current_time
from datetime import datetime
try:
    from _weakref import WeakSet
except ImportError:
    from weakref import WeakSet

from ...env import MESSAGE_CACHE_SIZE

from ...backend.utils import WeakReferer
from ...backend.event_loop import LOOP_TIME
from ...backend.export import export

from ..core import MESSAGES, KOKORO
from ..message import Message
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
        A messages's id to search.
    
    Returns
    -------
    index : `int`
    """
    bot = 0
    top = len(messages)
    while True:
        if bot < top:
            half = (bot+top)>>1
            if messages[half].id > message_id:
                bot = half+1
            else:
                top = half
            continue
        break
    
    return bot


class MessageHistoryCollector:
    """
    Attributes
    ----------
    channel_reference : ``WeakReferer`` to ``ChannelTextBase`` instance
        Reference to the parent channel.
    delay : `float`
        Additional message collection delay.
    handle : `None` or ``TimerHandle``
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
            timestamp = datetime.utcfromtimestamp(current_time()+handle.when+self.delay-LOOP_TIME())
            repr_parts.append(timestamp.__format__(DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


# Do not call any functions from this if you dunno anything about them!
# The message history is basically sorted by message_id, what can be translated to real time.
# The newer messages are at the start, meanwhile the older ones at the end.
# Do not try to delete not existing message's id, or it will cause de-sync.
# Use pypy?

@export
class ChannelTextBase:
    """
    Base class of the message-able channel types.
    
    Attributes
    ----------
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _message_history_collector :  `None` or ``MessageHistoryCollector``
        Collector for the channel's message history.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reach it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    """
    __slots__ = ()
    __slots = ('_message_keep_limit', '_message_history_collector', 'message_history_reached_end', 'messages', )
    
    def _messageable_init(self):
        """
        Sets the default values specific to text channels.
        """
        #discord side bug: we cant check last message
        self.message_history_reached_end = False
        self._message_history_collector = None
        self._message_keep_limit = MESSAGE_CACHE_SIZE
        self.messages = None
    
    @property
    def message_keep_limit(self):
        """
        A property for getting or setting how much message the channel can store before removing the last.
        
        Returns and accepts an `int`.
        """
        return self._message_keep_limit
    
    @message_keep_limit.setter
    def message_keep_limit(self, limit):
        if limit < 0:
            limit = 0
        
        if self._message_keep_limit == limit:
            return
        
        if limit == 0:
            new_messages = None
        else:
            old_messages = self.messages
            if old_messages is None:
                new_messages = None
            else:
                new_messages = deque((old_messages[i] for i in range(min(limit, len(old_messages)))), maxlen=limit)
                
        self.messages = new_messages
        self._message_keep_limit = limit
    
    
    def _create_new_message(self, message_data):
        """
        Creates a new message at the channel. If the message already exists inside of the channel's message history,
        returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        
        Returns
        -------
        message : ``Message``
        """
        from_cache, message = Message._create_message_is_in_cache(message_data)
        if from_cache:
            message._late_init(message_data)
            return message
        
        messages = self._maybe_create_queue()
        message_id = message.id
        
        if (messages is not None):
            if messages and (messages[0].id > message_id):
                index = message_relative_index(messages, message_id)
                max_length = messages.maxlen
                if max_length is None:
                    max_length_reached = False
                else:
                    if max_length == len(messages):
                        max_length_reached = True
                    else:
                        max_length_reached = False
                
                if index == len(messages):
                    if not max_length_reached:
                        messages.append(message)
                else:
                    if max_length_reached:
                        messages.pop()
                        self.message_history_reached_end = False
                    
                    messages.insert(index, message)
            
            else:
                messages_length = len(messages)
                messages.appendleft(message)
                if messages_length != len(messages):
                    self.message_history_reached_end = False
        
        return message
    
    
    def _create_old_message(self, message_data):
        """
        Creates an old message at the channel. If the message already exists inside of the channel's message history,
        returns that instead.
        
        Parameters
        ----------
        message_data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        
        Returns
        -------
        message : ``Message``
        
        Notes
        -----
        The created message cannot be added to the channel's message history, if it has no more spaces.
        """
        message = Message(message_data)
        message_id = message.id
        
        messages = self.messages
        if (messages is not None) and messages and (message_id > messages[-1].id):
            index = message_relative_index(messages, message_id)
            if index != len(messages):
                if messages[index].id != message_id:
                    self._maybe_increase_queue_size().insert(index, message)
        else:
            self._maybe_increase_queue_size().append(message)
        
        return message
    
    
    def _create_find_message(self, message_data, chained):
        """
        Tries to find whether the given message's data represents an existing message at the channel. If not, creates
        it. This method also returns whether the message existed at the channel's message history.
        
        Parameters
        ----------
        message_data : `dict` of (`str`, `Any`) items
            The message's data to find or create.
        chained : `bool`
            Whether the created message should be chained to the channel's message history's end, if not found.
        
        Returns
        -------
        message : ``Message``
        found : `bool`
        """
        message_id = int(message_data['id'])
        messages = self.messages
        if (messages is not None):
            index = message_relative_index(messages, message_id)
            if index != len(messages):
                message = messages[index]
                if message.id == message_id:
                    return message, True
        
        message = Message(message_data)
        
        if chained:
            self._maybe_increase_queue_size().append(message)
        
        return message, False
    
    
    def _add_message_collection_delay(self, delay):
        """
        Sets message collection timeout to the exact given time.
        
        Parameters
        ----------
        delay : `float`
            The time to delay the message collection with.
        """
        message_history_collector = self._message_history_collector
        if (message_history_collector is None):
            self._message_history_collector = MessageHistoryCollector(self, LOOP_TIME() + delay)
        else:
            message_history_collector.add_delay(delay)
    
    
    def _cancel_message_collection(self):
        """
        Cancels the message collector of the channel.
        """
        message_history_collector = self._message_history_collector
        if (message_history_collector is not None):
            self._message_history_collector = None
            message_history_collector.cancel()
    
    
    def _maybe_increase_queue_size(self):
        """
        Increases the queue size of the channel's message history if needed and returns it.
        
        Returns
        -------
        messages : `deque`
        """
        messages = self.messages
        if messages is None:
            # Create unlimited size.
            self.messages = messages = deque()
            self._add_message_collection_delay(110.0)
        else:
            max_length = messages.maxlen
            if (max_length is None):
                # The size is already unlimited
                self._add_message_collection_delay(10.0)
            else:
                # Switch to unlimited if we hit our current limit.
                if len(messages) == max_length:
                    self.messages = messages = deque(messages)
                    self._add_message_collection_delay(110.0)
        
        return messages
    
    
    def _maybe_create_queue(self):
        """
        Gets the channel's messages when creating a new message is created.
        
        Returns
        -------
        messages : `deque` or `None`
        """
        messages = self.messages
        if messages is None:
            message_keep_limit = self._message_keep_limit
            if message_keep_limit == 0:
                if self._message_history_collector is None:
                    messages = None
                else:
                    self.messages = messages = deque(maxlen=None)
            else:
                self.messages = messages = deque(maxlen=message_keep_limit)
        else:
            
            max_length = messages.maxlen
            if (max_length is not None) and (len(messages) == max_length):
                if self._message_history_collector is None:
                    self.message_history_reached_end = False
                else:
                    self.messages = messages = deque(messages, maxlen=None)
        
        return messages
    
    
    def _switch_to_limited(self):
        """
        Switches a channel's `.messages` to limited from unlimited.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance.
            The channel, what's `.messages` will be limited.
        """
        old_messages = self.messages
        if old_messages is None:
            new_messages = None
        else:
            limit = self._message_keep_limit
            if limit == 0:
                new_messages = None
            else:
                new_messages = deque(
                    (old_messages[index] for index in range(min(limit, len(old_messages)))),
                    maxlen=limit,
                )
        
        self.messages = new_messages
        self._cancel_message_collection()
        self.message_history_reached_end = False
    
    def _pop_message(self, delete_id):
        """
        Removes the specific message by it's id from the channel's message history and from `MESSAGES` as well.
        
        Parameters
        ----------
        delete_id : `int`
            The message's id to delete from the channel's message history.
        
        Returns
        -------
        message : `None` or ``Message``
        """
        messages = self.messages
        if (messages is not None):
            index = message_relative_index(messages, delete_id)
            if index != len(messages):
                message = messages[index]
                if message.id == delete_id:
                    del messages[index]
                    if (self._message_history_collector is not None):
                        if len(messages) < self._message_keep_limit:
                            self._switch_to_limited()
                    
                    try:
                        del MESSAGES[delete_id]
                    except KeyError:
                        pass
                    
                    message.deleted = True
                    return message
        
        try:
            message = MESSAGES.pop(delete_id)
        except KeyError:
            message = None
        else:
            message.deleted = True
        
        return message
    
    def _pop_multiple(self, delete_ids):
        """
        Removes the given messages from the channel and from `MESSAGES` as well. Returns the found messages.
        
        Parameters
        ----------
        delete_ids : `list` of `int`
            The messages' id to delete from the channel's message history.
        
        Returns
        -------
        found : `list` of ``Message``
            The found and removed messages.
        missed : `list` of `int`
            The identifier of the not found messages.
        """
        found = []
        missed = []
        delete_length = len(delete_ids)
        if not delete_length:
            return found, missed
        
        messages = self.messages
        delete_ids.sort(reverse=True)
        if messages is None:
            messages_length = 0
        else:
            messages_length = len(messages)
        
        if messages is None:
            messages_index = 0
        else:
            messages_index = message_relative_index(messages, delete_ids[0])
        delete_index = 0
        
        while True:
            if delete_index == delete_length:
                break
            
            if messages_index == messages_length:
                while True:
                    delete_id = delete_ids[delete_index]
                    try:
                        message = MESSAGES.pop(delete_id)
                    except KeyError:
                        missed.append(delete_id)
                    else:
                        message.deleted = True
                        found.append(message)
                        
                    delete_index += 1
                    if delete_index == delete_length:
                        break
                    
                    continue
                break
            
            message = messages[messages_index]
            delete_id = delete_ids[delete_index]
            message_id = message.id
            
            if message_id == delete_id:
                del messages[messages_index]
                try:
                    del MESSAGES[delete_id]
                except KeyError:
                    pass
                
                message.deleted = True
                found.append(message)
                
                messages_length -= 1
                delete_index += 1
                continue
            
            if message_id > delete_id:
                messages_index += 1
                continue
            
            delete_index += 1
            
            try:
                message = MESSAGES.pop(delete_id)
            except KeyError:
                missed.append(delete_id)
            else:
                message.deleted = True
                found.append(message)
            
            continue
        
        if (
            (messages is not None) and
            (self._message_history_collector is not None) and
            (len(messages) < self._message_keep_limit)
        ):
            self._switch_to_limited()
        
        return found, missed
