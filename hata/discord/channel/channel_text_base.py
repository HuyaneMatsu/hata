__all__ = ('ChannelTextBase', 'message_relative_index',)

from collections import deque
try:
    from _weakref import WeakSet
except ImportError:
    from weakref import WeakSet

from ...backend.event_loop import LOOP_TIME
from ...backend.export import export

from ..core import MESSAGES
from ..message import Message
from ..core import GC_CYCLER

TURN_MESSAGE_LIMITING_ON = WeakSet()


def turn_message_limiting_on(cycler):
    """
    Goes through all the channels inside of `Q_on_GC` and switches their message history to limited if their
    time is over.
    
    Parameters
    ----------
    cycler : `Cycler`
        The cycler what calls this function every X seconds.
    """
    now = LOOP_TIME()
    collected = []
    for channel in TURN_MESSAGE_LIMITING_ON:
        if channel._turn_message_keep_limit_on_at<now:
            collected.append(channel)
    
    while collected:
        channel = collected.pop()
        TURN_MESSAGE_LIMITING_ON.remove(channel)
        channel._switch_to_limited()

GC_CYCLER.append(turn_message_limiting_on)

del turn_message_limiting_on, GC_CYCLER



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
    _turn_message_keep_limit_on_at : `float`
        The LOOP_TIME time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reach it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    
    Class Attributes
    ----------------
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    """
    MESSAGE_KEEP_LIMIT = 10
    __slots__ = ()
    __slots = ('_message_keep_limit', '_turn_message_keep_limit_on_at', 'message_history_reached_end', 'messages', )
    
    def _messageable_init(self):
        """
        Sets the default values specific to text channels.
        """
        #discord side bug: we cant check last message
        self.message_history_reached_end = False
        self._turn_message_keep_limit_on_at = 0.0
        limit = self.MESSAGE_KEEP_LIMIT
        self._message_keep_limit = limit
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
    
    def _create_new_message(self, data):
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
        message_id = int(data['id'])
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            pass
        else:
            message._late_init(data)
            return message
        
        messages = self._maybe_create_queue()
        
        message = object.__new__(Message)
        message.id = message_id
        message._finish_init(data, self)
        
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
    
    def _create_old_message(self, data):
        """
        Creates an old message at the channel. If the message already exists inside of the channel's message history,
        returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        
        Returns
        -------
        message : ``Message``
        
        Notes
        -----
        The created message cannot be added to the channel's message history, if it has no more spaces.
        """
        message_id = int(data['id'])
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            message = object.__new__(Message)
            message.id = message_id
            message._finish_init(data, self)
        else:
            message._late_init(data)
        
        messages = self.messages
        if (messages is not None) and messages and (message_id > messages[-1].id):
            index = message_relative_index(messages, message_id)
            if index != len(messages):
                if messages[index].id != message_id:
                    self._maybe_increase_queue_size().insert(index, message)
        else:
            self._maybe_increase_queue_size().append(message)
        
        return message
    
    def _create_find_message(self, data, chained):
        """
        Tries to find whether the given message's data represents an existing message at the channel. If not, creates
        it. This method also returns whether the message existed at the channel's message history.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The message's data to find or create.
        chained : `bool`
            Whether the created message should be chained to the channel's message history's end, if not found.
        
        Returns
        -------
        message : ``Message``
        found : `bool`
        """
        message_id = int(data['id'])
        messages = self.messages
        if (messages is not None):
            index = message_relative_index(messages, message_id)
            if index != len(messages):
                message = messages[index]
                if message.id == message_id:
                    return message, True
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            message = object.__new__(Message)
            message.id = message_id
            message._finish_init(data, self)
        else:
            message._late_init(data)
        
        if chained:
            self._maybe_increase_queue_size().append(message)
        
        return message, False
    
    def _create_unknown_message(self, data):
        """
        Creates a message at the channel, what should not be linked to it's history. If the message exists at
        `MESSAGES`, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            The message's data.
        
        Returns
        -------
        message : ``Message``
        """
        message_id = int(data['id'])
        try:
            message = MESSAGES[message_id]
        except KeyError:
            message = Message._create_unlinked(message_id, data, self)
        else:
            message._late_init(data)
        
        return message
    
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
            self._turn_message_keep_limit_on_at = LOOP_TIME() + 110.0
            TURN_MESSAGE_LIMITING_ON.add(self)
        else:
            max_length = messages.maxlen
            if (max_length is None):
                # The size is already unlimited
                self._turn_message_keep_limit_on_at += 10.0
            else:
                # Switch to unlimited if we hit our current limit.
                if len(messages) == max_length:
                    self.messages = messages = deque(messages)
                    self._turn_message_keep_limit_on_at = LOOP_TIME() + 110.0
                    TURN_MESSAGE_LIMITING_ON.add(self)
        
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
                if self._turn_message_keep_limit_on_at:
                    self.messages = messages = deque(maxlen=None)
                else:
                    messages =None
            else:
                self.messages = messages = deque(maxlen=message_keep_limit)
        else:
            
            max_length = messages.maxlen
            if (max_length is not None) and (len(messages) == max_length):
                if self._turn_message_keep_limit_on_at:
                    self.messages = messages = deque(messages, maxlen=None)
                else:
                    self.message_history_reached_end = False
        
        return messages
    
    def _switch_to_limited(channel):
        """
        Switches a channel's `.messages` to limited from unlimited.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance.
            The channel, what's `.messages` will be limited.
        """
        old_messages = channel.messages
        if old_messages is None:
            new_messages = None
        else:
            limit = channel._message_keep_limit
            if limit == 0:
                new_messages = None
            else:
                new_messages = deque((old_messages[i] for i in range(min(limit, len(old_messages)))), maxlen=limit)
        
        channel.messages = new_messages
        channel._turn_message_keep_limit_on_at = 0.0
        channel.message_history_reached_end = False
    
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
                    if self._turn_message_keep_limit_on_at:
                        if len(messages) < self._message_keep_limit:
                            TURN_MESSAGE_LIMITING_ON.discard(self)
                            self._turn_message_keep_limit_on_at = 0.0
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
        
        if (messages is not None) and self._turn_message_keep_limit_on_at:
            if len(messages) < self._message_keep_limit:
                TURN_MESSAGE_LIMITING_ON.discard(self)
                self._turn_message_keep_limit_on_at = 0.0
                self._switch_to_limited()
        
        return found, missed
    
    def _process_message_chunk(self, data):
        """
        Called with the response data after requesting older messages of a channel. It checks whether we can chain
        the messages to the channel's history. If we can it chains them and removes the length limitation too if
        needed.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items) elements
            A list of message's data received from Discord.
        
        Returns
        -------
        received : `list` of ``Message`` objects
        """
        received = []
        index = 0
        limit = len(data)
        
        if index == limit:
            return received
        
        message_data = data[index]
        index += 1
        message, exists = self._create_find_message(message_data, False)
        received.append(message)
        
        if exists:
            while True:
                if index == limit:
                    break
                
                message_data = data[index]
                index += 1
                message, exists = self._create_find_message(message_data, True)
                received.append(message)
                
                if exists:
                    continue
                
                while True:
                    if index == limit:
                        break
                    
                    message_data = data[index]
                    index += 1
                    message = self._create_old_message(message_data)
                    received.append(message)
                    continue
                
                break
        else:
            while True:
                if index == limit:
                    break
                
                message_data = data[index]
                index += 1
                message = self._create_unknown_message(message_data)
                received.append(message)
                continue
        
        return received
