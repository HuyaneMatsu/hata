﻿# -*- coding: utf-8 -*-
__all__ = ('ChannelBase', 'ChannelCategory', 'ChannelGroup', 'ChannelGuildBase', 'ChannelPrivate', 'ChannelStore',
    'ChannelText', 'ChannelTextBase', 'ChannelVoice', 'MessageIterator', 'cr_pg_channel_object')

import re
from collections import deque
from time import monotonic
from weakref import WeakSet

from ..backend.dereaddons_local import autoposlist

from .bases import DiscordEntity, IconSlot, ICON_TYPE_NONE
from .client_core import CHANNELS
from .permission import Permission
from .http import URLS
from .message import Message, MESSAGES
from .user import User, ZEROUSER
from .role import PermOW
from .client_core import GC_cycler
from .webhook import Webhook, WebhookRepr
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_int, preconvert_bool

from . import webhook, message, ratelimit, http

Client = NotImplemented

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
    now = monotonic()
    collected = []
    for channel in TURN_MESSAGE_LIMITING_ON:
        if channel._turn_message_keep_limit_on_at<now:
            collected.append(channel)
    
    while collected:
        channel = collected.pop()
        TURN_MESSAGE_LIMITING_ON.remove(channel)
        channel._switch_to_limited()

GC_cycler.append(turn_message_limiting_on)

del turn_message_limiting_on, GC_cycler

def PartialChannel(data, partial_guild=None):
    """
    Creates a partial channel from partial channel data.
    
    Parameters
    ----------
    data : `None` or `dict` of (`str`, `Any`) items
        Partial channel data received from Discord.
    partial_guild : `None` or ``Guild``, Optional
        A partial guild for the created channel.
    
    Returns
    -------
    channel : `None` or ``ChannelBase`` instance
        The created partial channel, or `None`, if no data was received.
    """
    if (data is None) or (not data):
        return None
    channel_id=int(data['id'])
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass
    
    try:
        cls=CHANNEL_TYPES[data['type']]
    except IndexError:
        return None
    
    channel=cls._from_partial_data(data,channel_id,partial_guild)
    CHANNELS[channel_id]=channel
    
    return channel

class ChannelBase(DiscordEntity, immortal=True):
    """
    Base class for Discord channels.
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the channel.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(0,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    
    Notes
    -----
    Channels support weakreferencing.
    """
    INTERCHANGE = (0,)
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a channel from the channel data received from Discord. If the channel already exists and if it is
        partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data reeceive from Discord.
        client : ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : ``Guild``, Optional
            The guild of the channel, if it has.
        
        Returns
        -------
        channel : ``ChannelGuildBase`` instance
        """
        channel_id=int(data['id'])
        try:
            channel = CHANNELS[channel_id]
            update = (not channel.clients)
        except KeyError:
            channel=object.__new__(cls)
            channel.id=channel_id
            CHANNELS[channel_id]=channel
            update=True
        
        if update:
            # make sure about this
            if issubclass(cls, ChannelGuildBase):
                secondary_argument = guild
            else:
                secondary_argument = client
            
            assert (secondary_argument is not None), \
                f'Secondary argument cannot be `None` when calling `channel._finish_init`.'
            
            channel._finish_init(data, secondary_argument)
        
        if cls is ChannelPrivate:
            if channel.users[0] is client:
                user=channel.users[1]
            else:
                user=channel.users[0]
            
            client.private_channels[user.id]=channel
        
        elif cls is ChannelGroup:
            client.group_channels[channel_id]=channel
        
        return channel

    def __repr__(self):
        """Returns the reprsentation of the channel."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.__str__()!r}>'
    
    def __str__(self):
        """Returns the channel's name."""
        return ''
    
    def __format__(self, code):
        """
        Formats the channel in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        channel : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        >>> from hata import ChannelText, now_as_id
        >>> channel = ChannelText.precreate(now_as_id(), name='GENERAL')
        >>> channel
        <ChannelText id=710506058560307200, name='GENERAL'>
        >>> # no code stands for str(channel).
        >>> f'{channel}'
        'GENERAL'
        >>> # 'd' stands for display name.
        >>> f'{channel:d}'
        'general'
        >>> # 'm' stands for mention.
        >>> f'{channel:m}'
        '<#710506058560307200>'
        >>> # 'c' stands for created at.
        >>> f'{channel:c}'
        '2020.05.14-14:57:24'
        """
        if not code:
            return self.__str__()
        if code=='m':
            return f'<#{self.id}>'
        if code=='d':
            return self.display_name
        if code=='c':
            return self.created_at.__format__('%Y.%m.%d-%H:%M:%S')
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    @property
    def display_name(self):
        """
        The channel's display name.
        
        Returns
        -------
        display_name : `str`
        """
        return ''
    
    @property
    def mention(self):
        """
        The channel's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'<#{self.id}>'
    
    @property
    def partial(self):
        """
        Whether this channel is partial.
        
        A channel is partial if non of the running clients can see it.
        
        Returns
        -------
        is_partial : `bool`
        """
        return (not self.clients)
    
    def get_user(self, name, default=None):
        """
        Tries to find the a user with the given name at the channel. Returns the first matched one.
        
        The search order is the following:
        - `full_name`
        - `name`
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``User``, ``Client`` or `None`
        """
        if len(name)>37:
            return default
        users=self.users
        
        if len(name)>6 and name[-5]=='#':
            try:
                discriminator=int(name[-4:])
            except ValueError:
                pass
            else:
                name=name[:-5]
                for user in users:
                    if user.discriminator==discriminator and user.name==name:
                        return user
        
        if len(name)>32:
            return default
        
        for user in users:
            if user.name==name:
                return user
        
        return default
    
    def get_user_like(self, name, default=None):
        """
        Searches a user, who's name starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``User``, ``Client`` or `default`
        """
        if not 1<len(name)<33:
            return default
        pattern=re.compile(re.escape(name),re.I)
        for user in self.users:
            if pattern.match(user.name) is None:
                continue
            return user
        return default
    
    def get_users_like(self, name):
        """
        Searches the users, who's name starts with the given string.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        result=[]
        if not 1<len(name)<33:
            return result
        pattern=re.compile(re.escape(name),re.I)
        for user in self.users:
            if pattern.match(user.name) is None:
                continue
            result.append(user)
        return result
    
    @property
    def users(self):
        """
        The users who are can see this channel.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``) objects
        """
        return []
    
    @property
    def clients(self):
        """
        The clients, who can access this channel.
        
        Returns
        -------
        clients : `list` of ``Client`` objects
        """
        result=[]
        for user in self.users:
            if type(user) is User:
                continue
            result.append(user)
        return result
    
    #for sorting channels
    def __gt__(self,other):
        """Returns whether this channel's id is greater than the other's."""
        if isinstance(other,ChannelBase):
            return self.id>other.id
        return NotImplemented
    
    def __ge__(self,other):
        """Returns whether this channel's id is greater or equal than the other's."""
        if isinstance(other,ChannelBase):
            return self.id>=other.id
        return NotImplemented
    
    def __eq__(self,other):
        """Returns whether this channel's id is equal to the other's."""
        if isinstance(other,ChannelBase):
            return self.id==other.id
        return NotImplemented
    
    def __ne__(self,other):
        """Returns whether this channel's id is not equal to the other's."""
        if isinstance(other,ChannelBase):
            return self.id!=other.id
        return NotImplemented
    
    def __le__(self,other):
        """Returns whether this channel's id is less or equal than the other's."""
        if isinstance(other,ChannelBase):
            return self.id<=other.id
        return NotImplemented
    
    def __lt__(self,other):
        """Returns whether this channel's id is less than the other's."""
        if isinstance(other,ChannelBase):
            return self.id<other.id
        return NotImplemented

#sounds funny, but this is a class
#the chunksize is 97, because it means 1 request for _load_messages_till
class MessageIterator(object):
    """
    An asynchronous message iterator over the given text channel.
    
    Attributes
    ----------
    _index : `int`
        The index of the message, what will be yielded.
    _can_read_history : `bool`
        Tells the message iterator, whether it's client can not read the history if it's channel.
    channel : ``ChannelTextBase`` instance
        The channel, what's messages the message iterator will iterates over.
    chunksize : `int`
        The amount of messages, what the message iterator will extend it's channel's message history, each time, the
        loaded messages are exhausted.
    client : ``Client``
        The client, who will do the api requests for requesting more messages.
    """
    __slots__ = ('_can_read_history', '_index', 'channel', 'chunksize', 'client',)
    def __init__(self, client, channel, chunksize=99):
        """
        Creates a message iterator.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will do the api requests for requesting more messages.
        channel : ``ChannelTextBase`` instance
            The channel, what's messages the message iterator will iterates over.
        chunksize : `int`, Optional
            The amount of messages, what the message iterator will extend it's channel's message history, each time, the
            loaded messages are exhausted. Limited to `97` as a maximal value.
        """
        if chunksize>99:
            chunksize=99
        
        self.client     = client
        self.channel    = channel
        self.chunksize  = chunksize
        self._index     = 0
        self._can_read_history = not channel.cached_permissions_for(client).can_read_message_history
    
    def __aiter__(self):
        """Returns self and resets the `.index`."""
        self._index = 0
        return self
    
    async def __anext__(self):
        """Yields the next message of the iterator's channel."""
        channel=self.channel
        index=self._index
        if len(channel.messages)>index:
            self._index=index+1
            return channel.messages[index]
        
        if channel.message_history_reached_end or self._can_read_history:
            raise StopAsyncIteration
        
        try:
            await self.client._load_messages_till(channel, index+self.chunksize)
        except IndexError:
            pass
        
        if len(channel.messages)>index:
            self._index=index+1
            return channel.messages[index]
        
        raise StopAsyncIteration
    
    def __repr__(self):
        """Returns the representation of the message iterator."""
        return f'<{self.__class__.__name__} of client {self.client.full_name}, at channel {self.channel.name!r} ({self.channel.id})>'

#searches the relative index of a message in a list
def message_relativeindex(messages, message_id):
    """
    Searches the relative index of the given message's id in a channel's message history. The returned index is
    relative, because if the message with the given is not found, it should be at that specific index, if it would be
    inside of the respeive channel's message history.
    
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
    bot=0
    top=len(messages)
    while True:
        if bot<top:
            half=(bot+top)>>1
            if messages[half].id>message_id:
                bot=half+1
            else:
                top=half
            continue
        break
    return bot

# Do not call any functions from this if you dunno anything about them!
# The message history is basically sorted by message_id, what can be translated to real time.
# The newer messages are at the start, meanwhile the olders at the end.
# Do not try to delete not existing message's id, or it will cause desync.
# Use pypy?
class ChannelTextBase:
    """
    Baseclass of the messageable channel types.
    
    Atrributes
    ----------
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The monotonic time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's messag history reache it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    
    Class attributes
    ----------------
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    """
    MESSAGE_KEEP_LIMIT = 10
    __slots__ = ()
    __slots = ('_message_keep_limit', '_turn_message_keep_limit_on_at', 'message_history_reached_end', 'messages', )
    
    def _messageable_init(channel):
        """
        Sets the default values specific to text channels.
        """
        #discord side bug: we cant check last message
        channel.message_history_reached_end=False
        channel._turn_message_keep_limit_on_at=0
        limit=channel.MESSAGE_KEEP_LIMIT
        channel._message_keep_limit=limit
        channel.messages=deque(maxlen=limit)
    
    def _get_message_keep_limit(channel):
        return channel._message_keep_limit
    
    def _set_message_keep_limit(channel, limit):
        if channel._message_keep_limit==limit:
            return
        if limit<=0:
            channel._message_keep_limit=0
            channel.messages=deque(maxlen=0)
            return
        
        old_messages=channel.messages
        if len(old_messages)>limit:
            channel.messages=deque((old_messages[i] for i in range(limit)),maxlen=limit)
        channel._message_keep_limit=limit
    
    message_keep_limit=property(_get_message_keep_limit,_set_message_keep_limit)
    del _get_message_keep_limit, _set_message_keep_limit
    # If opt level is under2, set docstring
    if (_messageable_init.__doc__ is not None):
        message_keep_limit.__doc__ = (
        """
        A property for getting or setting how much message the channel can store before removing the last.
        
        Returns and accepts an `int`.
        """)
    
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
        
        messages = self.messages
        if messages:
            message = messages[0]
            last_message_id = message.id
            if last_message_id < message_id:
                pass
            elif last_message_id == message_id:
                return message
            else:
                return self._create_asynced_message(data, message_id, False)
        
        message = object.__new__(Message)
        message.id = message_id
        message._finish_init(data, self)
        
        if (self.messages.maxlen is not None) and len(messages)==self._message_keep_limit:
            self.message_history_reached_end = False
        
        messages.appendleft(message)
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
        
        messages = self.messages
        if messages:
            if message_id > messages[-1].id:
                return self._create_asynced_message(data, message_id, True)
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            message = object.__new__(Message)
            message.id = message_id
            message._finish_init(data, self)
        
        self._increased_queue_size().append(message)
        return message
    
    def _create_asynced_message(self, data, message_id, increase_queue_size):
        """
        This method gets called if ``._create_new_message`` sees that the message is older than it's first one,
        or if ``._create_old_message`` sees that the message is newer than it's last. As the method's name says,
        it tries to find the message by it's  `id` and insert to the right place if not exists. If it exists
        returns the found one.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message data received from Discord.
        message_id : `int`
            The id of the message.
        increase_queue_size : `bool`
            Whether the message's queue size should be increased if older messages are loaded.
        
        Returns
        -------
        message : ``Message``
        """
        messages = self.messages
        index = message_relativeindex(messages, message_id)
        if index != len(messages):
            actual = messages[index]
            if actual.id==message_id:
                return actual
        
        if increase_queue_size:
            messages = self._increased_queue_size()
        else:
            if (messages.maxlen is not None) and (messages.maxlen == len(messages)):
                messages.pop()
        
        message = object.__new__(Message)
        message.id = message_id
        message._finish_init(data, self)
        
        messages.insert(index, message)
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
        
        if self._message_keep_limit!=0:
            messages = self.messages
            index = message_relativeindex(messages, message_id)
            if index!=len(messages):
                message = messages[index]
                if message.id==message_id:
                    return message, True
        
        try:
            message = MESSAGES[message_id]
        except KeyError:
            message = object.__new__(Message)
            message.id=message_id
            message._finish_init(data, self)
        
        if chained:
            self._increased_queue_size().append(message)
        
        return message, False
    
    def _create_unknown_message(self, data):
        """
        Creates a message at the channel, what should not be linked to it's history. If the mesage exists at
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
            message = object.__new__(Message)
            message.id = message_id
            message._finish_init(data, self)
        
        return message
    
    def _increased_queue_size(self):
        """
        Increases the queue size of the channel's message history if needed and returns it.
        
        Returns
        -------
        messages : `deque`
        """
        messages = self.messages
        if (messages.maxlen is None):
            self._turn_message_keep_limit_on_at += 10.0
        else:
            if len(messages) == self._message_keep_limit:
                self.messages = messages = deque(messages)
                self._turn_message_keep_limit_on_at = monotonic() + 110.0
        
        return messages
    
    def _switch_to_limited(channel):
        """
        Switches a channel's `.messages` to limited from unlimited.
        
        Parameters
        ----------
        channel : ``ChannelTextBase`` instance.
            The channel, what's `.messages` will be limited.
        """
        old_messages=channel.messages
        limit=channel._message_keep_limit
        if len(old_messages)>limit:
            messages=deque((old_messages[i] for i in range(limit)),maxlen=limit)
        else:
            messages=deque(old_messages,maxlen=limit)
        
        channel.messages = messages
        channel._turn_message_keep_limit_on_at=0.
        channel.message_history_reached_end=False
    
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
        if self._message_keep_limit:
            messages = self.messages
            index = message_relativeindex(messages, delete_id)
            if index != len(messages):
                message = messages[index]
                if message.id == delete_id:
                    del messages[index]
                    if self._turn_message_keep_limit_on_at:
                        if len(messages) < self._message_keep_limit:
                            try:
                                TURN_MESSAGE_LIMITING_ON.remove(self)
                            except KeyError:
                                pass
                            self._turn_message_keep_limit_on_at=0.
                            self._switch_to_limited()
                    
                    try:
                        del MESSAGES[delete_id]
                    except KeyError:
                        pass
                    
                    return message
        
        return MESSAGES.pop(delete_id, None)
    
    def _pop_multiple(self, delete_ids):
        """
        Removes the given messages from the channel and from `MESSAGES` as well. Returns the found messages.
        
        Parameters
        ----------
        delete_ids : `list` of `int`
            The messages' id to delete from the channel's message history.
        
        Returns
        -------
        messages : `list` of ``Message``
        """
        found = []
        delete_ln = len(delete_ids)
        if not delete_ln:
            return found
        
        messages = self.messages
        delete_ids.sort(reverse=True)
        messages_ln = len(messages)
        
        messages_index = message_relativeindex(messages, delete_ids[0])
        delete_index = 0
        
        while True:
            if delete_index == delete_ln:
                break
            
            if messages_index == messages_ln:
                while True:
                    delete_id = delete_ids[delete_index]
                    try:
                        message = MESSAGES.pop(delete_id)
                    except KeyError:
                        pass
                    else:
                        found.append(message)
                        
                    delete_index +=1
                    if delete_index == delete_ln:
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
                found.append(message)
                
                messages_ln -= 1
                delete_index += 1
                continue
            
            if message_id>delete_id:
                messages_index += 1
                continue
            
            delete_index += 1
            
            try:
                message = MESSAGES.pop(delete_id)
            except KeyError:
                pass
            else:
                found.append(message)
            
            continue
        
        if self._turn_message_keep_limit_on_at:
            if len(messages) < self._message_keep_limit:
                try:
                    TURN_MESSAGE_LIMITING_ON.remove(self)
                except KeyError:
                    pass
                self._turn_message_keep_limit_on_at=0.0
                self._switch_to_limited()
        
        return found
    
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
        index +=1
        message, exists = self._create_find_message(message_data, False)
        received.append(message)
        
        if exists:
            while True:
                if index==limit:
                    break
                
                message_data = data[index]
                index +=1
                message, exists = self._create_find_message(message_data, True)
                received.append(message)
                
                if exists:
                    continue
                
                while True:
                    if index == limit:
                        break
                    
                    message_data = data[index]
                    index +=1
                    message = self._create_old_message(message_data)
                    received.append(message)
                    continue
                
                break
        else:
            while True:
                if index==limit:
                    break
                
                message_data = data[index]
                index +=1
                message = self._create_unknown_message(message_data)
                received.append(message)
                continue
        
        return received

class ChannelGuildBase(ChannelBase):
    """
    Base class for guild channels.
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the channel.
    _cache_perm : `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermOW`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(0,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : ˛int` = `0`
        An order group what defined which guild channel type comes after the other one.
    """
    __slots__ = ('_cache_perm', 'category', 'guild', 'name', 'overwrites', 'position', )
    
    ORDER_GROUP = 0
    
    def __gt__(self, other):
        """
        Whether this channel has higher (visible) position than an other one in a guild.
        If the other channel is not guild channel, then just compares their id.
        """
        if isinstance(other, ChannelGuildBase):
            if self.ORDER_GROUP > other.ORDER_GROUP:
                return True
            
            if self.ORDER_GROUP == other.ORDER_GROUP:
                if self.position > other.position:
                    return True
                
                if self.position == other.position:
                    if self.id > other.id:
                        return True
            
            return False
        
        if isinstance(other, ChannelBase):
            return self.id > other.id
        
        return NotImplemented
    
    def __ge__(self, other):
        """
        Whether this channel is same as the other one, or has higher (visible) position than an other one in a guild.
        If the other channel is not guild channel, then just compares their id.
        """
        if isinstance(other, ChannelGuildBase):
            if self.ORDER_GROUP > other.ORDER_GROUP:
                return True
            
            if self.ORDER_GROUP == other.ORDER_GROUP:
                if self.position > other.position:
                    return True
                
                if self.position == other.position:
                    if self.id >= other.id:
                        return True
            
            return False
        
        if isinstance(other, ChannelBase):
            return self.id > other.id
        
        return NotImplemented
    
    def __le__(self, other):
        """
        Whether this channel is same as the other one, or has lower (visible) position than an other one in a guild.
        If the other channel is not guild channel, then just compares their id.
        """
        if isinstance(other, ChannelGuildBase):
            if self.ORDER_GROUP < other.ORDER_GROUP:
                return True
            
            if self.ORDER_GROUP == other.ORDER_GROUP:
                if self.position < other.position:
                    return True
                
                if self.position == other.position:
                    if self.id <= other.id:
                        return True
            
            return False
        
        if isinstance(other, ChannelBase):
            return self.id < other.id
        
        return NotImplemented
    
    def __lt__(self, other):
        """
        Whether this channel has lower (visible) position than an other one in a guild.
        If the other channel is not guild channel, then just compares their id.
        """
        if isinstance(other, ChannelGuildBase):
            if self.ORDER_GROUP < other.ORDER_GROUP:
                return True
            
            if self.ORDER_GROUP == other.ORDER_GROUP:
                if self.position < other.position:
                    return True
                
                if self.position == other.position:
                    if self.id < other.id:
                        return True
            
            return False
        
        if isinstance(other, ChannelBase):
            return self.id < other.id
        
        return NotImplemented

    def _init_catpos(self, data, guild):
        """
        Inicializes the `.category` and the `.position` of the channel. If a channel is under the ``Guild.md``,
        and not in a category (category channels are all like these), then their `.category` is the ``Guild`` itself.
        This method is used when we inicialize a guild channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        guild : ``Guild``
            The guild of the channel.
        """
        self.guild = guild
        guild.all_channel[self.id] = self
        
        self.position = data.get('position',0)
        
        category_id = data.get('parent_id')
        if category_id is None:
            category = guild
        else:
            category = guild.all_channel[int(category_id)]
        
        self.category = category
        category.channels.append(self)
    
    def _set_catpos(self, data):
        """
        Similar to the ``._init_catpos`` method, but this method applies the changes too, so moves the channel
        between categories and moves the channel inside of the catgeory too, to keep the order.
        
        Called from `._update_no_return` when updating a guild channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord
        """
        guild = self.guild
        if guild is None:
            return
        
        new_category_id = data.get('parent_id',None)
        if new_category_id is None:
            new_category = guild
        else:
            new_category = guild.all_channel[int(new_category_id)]
        
        position=data.get('position',0)
        
        category = self.category
        if category is new_category:
            if self.position != position:
                self.position = position
                category.channels.sort()
        else:
            category.channels.remove(self)
            
            self.position = position
            self.category = new_category
            new_category.channels.append(self)
    
    def _update_catpos(self, data, old_attributes):
        """
        Acts same as ``._set_catpos``, but it sets the modified attrbiutes' previous value to `old_attributes`.
        
        Called from `._update` when updating a guild channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord
        old_attributes : `dict` of (`str`, `Any`) items
            `attribute-name` - `old-value` relations containing the changes of caused by the update.
        """
        guild = self.guild
        if guild is None:
            return
        
        new_category_id = data.get('parent_id',None)
        if new_category_id is None:
            new_category = guild
        else:
            new_category = guild.all_channel[int(new_category_id)]
        
        position=data.get('position',0)
        
        category = self.category
        if category is new_category:
            if self.position != position:
                old_attributes['position'] = self.position
                self.position = position
                category.channels.sort()
        else:
            old_attributes['category'] = category
            old_attributes['position'] = self.position
            
            category.channels.remove(self)
            
            self.position = position
            self.category = category
            new_category.channels.append(self)
    
    def _permissions_for(self, user):
        """
        Base permission calculator method. Subclasses call this first, then apply their channel type related changes.
        
        Parameters
        ----------
        user : ``UserBase`` instance
            The user, who's permissions will be returned.
        
        Returns
        -------
        permission : ``Permission``
        """
        guild = self.guild
        if guild is None:
            return Permission.permission_none
        
        default_role=guild.roles[0]
        base=default_role.permissions
        
        try:
            roles = user.guild_profiles[guild].roles
        except KeyError:
            if type(user) in (Webhook, WebhookRepr) and user.channel is self:
                
                overwrites = self.overwrites
                if overwrites:
                    overwrite = overwrites[0]
                    
                    if overwrite.target is default_role:
                        base=(base&~overwrite.deny)|overwrite.allow
                
                return Permission(base)
            
            return Permission.permission_none
        
        else:
            roles.sort()
            for role in roles:
                base|=role.permissions
        
        if Permission.can_administrator(base):
            return Permission.permission_all
        
        overwrites = self.overwrites
        if overwrites:
            overwrite = overwrites[0]
            
            if overwrite.target is default_role:
                base=(base&~overwrite.deny)|overwrite.allow
            
            for overwrite in overwrites:
                if overwrite.target in roles or overwrite.target is user:
                    base=(base&~overwrite.deny)|overwrite.allow
        
        return Permission(base)
    
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        
        See Also
        --------
        .cached_permissions_for : Cached permission calculator.
        """
        if user==self.guild.owner:
            return Permission.permission_all
        
        result=self._permissions_for(user)
        if not result.can_view_channel:
            return Permission.permission_none
        
        return result
    
    def cached_permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel. If the user's permissions are not cached, calculates
        and stores them first.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Mainly designed for getting clients' permissions.
        """
        try:
            return self._cache_perm[user.id]
        except KeyError:
            permissions=self.permissions_for(user)
            self._cache_perm[user.id]=permissions
            return permissions
    
    def _parse_overwrites(self, data):
        """
        Parses the permission overwrites from the given data and returns them.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items) elements
            A list of permission overwrites' data.
        
        Returns
        -------
        overwrites : `list` of ``PermOW``
        """
        overwrites=[]
        try:
            overwrites_data=data['permission_overwrites']
        except KeyError:
            return overwrites
        if not overwrites_data:
            return overwrites
        
        default_role=self.guild.default_role
        
        for overwrite_data in overwrites_data:
            overwrite=PermOW(overwrite_data)
            if overwrite.target is default_role:
                overwrites.insert(0,overwrite)
            else:
                overwrites.append(overwrite)
        
        return overwrites
    
    def __str__(self):
        """Returns the channel's name."""
        return self.name
    
    @property
    def users(self):
        """
        Returns the users, who can see this channel.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        guild = self.guild
        if guild is None:
            return []
        return [user for user in guild.users.values() if self.permissions_for(user).can_view_channel]
    
    @property
    def clients(self):
        """
        The clients, who can access this channel.
        
        Returns
        -------
        clients : `list` of ``Client`` objects
        """
        guild=self.guild
        if guild is None:
            return []
        return guild.clients
    
    def get_user(self, name, default=None):
        """
        Tries to find the a user with the given name at the channel. Users, who cannot see the channel are ignored.
        Returns the first matched one.
        
        The search order is the following:
        - `full_name`
        - `name`
        - `nick`
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``User``, ``Client`` or `default`
        """
        if self.guild is None:
            return default
        
        if len(name)>37:
            return default
        
        users = self.users
        
        if len(name)>6 and name[-5]=='#':
            try:
                discriminator=int(name[-4:])
            except ValueError:
                pass
            else:
                name=name[:-5]
                for user in users:
                    if user.discriminator==discriminator and user.name==name:
                        return user
        
        if len(name)>32:
            return default

        for user in users:
            if user.name==name:
                return user
        
        guild = self.guild
        for user in users:
            nick = user.guild_profiles[guild]
            if nick is None:
                continue
            
            if nick==name:
                return user
        
        return default

    def get_user_like(self, name ,default=None):
        """
        Searches a user, who's name starts with the given string and returns the first find. Users, who cannot see the
        channel are ignored.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``User``, ``Client`` or `default`
        """
        guild=self.guild
        if guild is None:
            return default
        
        if not 1<len(name)<33:
            return default
        
        pattern=re.compile(re.escape(name),re.I)
        
        for user in guild.users.values():
            if not self.permissions_for(user).can_view_channel:
                continue
            if pattern.match(user.name) is not None:
                return user
            nick=user.guild_profiles[guild].nick
            if nick is None:
                continue
            if pattern.match(nick) is None:
                continue
            return user
        
        return default
    
    def get_users_like(self, name):
        """
        Searches the users, who's name start with the given string. Users, who cannot see the channel are ignored.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        result = []
        guild=self.guild
        if guild is None:
            return result
        
        if not 1<len(name)<33:
            return result
        
        pattern=re.compile(re.escape(name),re.I)
        
        for user in guild.users.values():
            if not self.permissions_for(user).can_view_channel:
                continue
            if pattern.match(user.name) is not None:
                result.append(user)
                continue
            nick=user.guild_profiles[guild].nick
            if nick is None:
                continue
            if pattern.match(nick) is None:
                continue
            result.append(user)

        return result

class ChannelText(ChannelGuildBase, ChannelTextBase):
    """
    Represents a ``Guild`` text channel or an announcements channel. So the type of the channel is interchangeable
    between them. The channel's Discord side channel type is 0 (text) or 5 (announcements).
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the channel.
    _cache_perm : `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermOW`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The monotonic time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's messag history reache it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user acounts with
        `manage_messages` or `manage_channel` permissions are unaffected
    topic : `str`
        The channel's topic.
    type : `int`
        The channel's Disord side type. Can be any of `.INTERCHANGE`.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(0, 5,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    """
    __slots__ = ('nsfw', 'slowmode', 'topic', 'type',) #guild text channel related
    
    ORDER_GROUP = 0
    INTERCHANGE = (0, 5,)

    def _finish_init(self, data, guild):
        """
        Finishes the channel's initialization with setting it's channel type specific attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data recevied from Discord.
        guild : ``Guild``
            The channel's guild.
        """
        self._cache_perm={}
        self.name=data['name']
        self.type=data['type']
        
        self._init_catpos(data, guild)
        self.overwrites=self._parse_overwrites(data)
        
        self._messageable_init()
        
        self.topic=data.get('topic','')
        self.nsfw=data.get('nsfw',False)
        self.slowmode=int(data.get('rate_limit_per_user',0))

    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelText`` from partial data. Called by ``PartialChannel`` when a new partial channel is needed
        to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : ``Guild`` or `None`
            The channel's guild if applicable.
        
        Returns
        -------
        channel : ``ChannelText``
        """
        self=object.__new__(cls)
        self._messageable_init()
        
        self._cache_perm= {}
        self.category   = None
        self.guild      = partial_guild
        self.id         = channel_id
        self.name       = data.get('name','')
        self.nsfw       = False
        self.overwrites = []
        self.position   = 0
        self.slowmode   = 0
        self.topic      = ''
        self.type       = int(data['type'])
        
        return self
    
    @property
    def display_name(self):
        """
        A text channel's display name is it's name with lovercase characters.
        
        Returns
        -------
        display_name : `str`
        """
        return self.name.lower()
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        self._cache_perm.clear()
        self._set_catpos(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name=data['name']
        self.type=data['type']
        self.topic=data.get('topic','')
        self.nsfw=data.get('nsfw',False)
        self.slowmode=int(data.get('rate_limit_per_user',0))
    
    def _update(self, data):
        """
        Updates the channel and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------------------+
        | Keys          | Values                            |
        +===============+===================================+
        | category      | ``ChannelCategory`` or ``Guild``  |
        +---------------+-----------------------------------+
        | name          | `str`                             |
        +---------------+-----------------------------------+
        | nsfw          | `bool`                            |
        +---------------+-----------------------------------+
        | overwrites    | `list` of ``PermOW``              |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        | slowmode      | `int`                             |
        +---------------+-----------------------------------+
        | topic         | `str`                             |
        +---------------+-----------------------------------+
        | type          | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm.clear()
        old_attributes = {}
        
        type_=data['type']
        if self.type!=type_:
            old_attributes['type']=self.type
            self.type=type_
        
        name=data['name']
        if self.name!=name:
            old_attributes['name']=self.name
            self.name=name
        
        topic=data.get('topic','')
        if self.topic!=topic:
            old_attributes['topic']=self.topic
            self.topic=topic
        
        nsfw=data.get('nsfw',False)
        if self.nsfw!=nsfw:
            old_attributes['nsfw']=self.nsfw
            self.nsfw=nsfw
        
        slowmode=int(data.get('rate_limit_per_user',0))
        if self.slowmode!=slowmode:
            old_attributes['slowmode']=self.slowmode
            self.slowmode=slowmode
        
        overwrites=self._parse_overwrites(data)
        if self.overwrites!=overwrites:
            old_attributes['overwrites']=self.overwrites
            self.overwrites=overwrites
        
        self._update_catpos(data, old_attributes)
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild=self.guild
        if guild is None:
            return
        
        self.guild=None
        del guild.all_channel[self.id]

        if self is guild.system_channel:
            guild.system_channel=None
        if self is guild.widget_channel:
            guild.widget_channel=None    
        if self is guild.embed_channel:
            guild.embed_channel=None
        if self is guild.rules_channel:
            guild.rules_channel=None
        if self is guild.public_updates_channel:
            guild.public_updates_channel=None
        
        self.category.channels.remove(self)
        self.category=None
        
        self.overwrites.clear()
        self._cache_perm.clear()
        
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        
        See Also
        --------
        .cached_permissions_for : Cached permission calculator.
        """
        if user==self.guild.owner:
            return Permission.permission_deny_voice
        
        result=self._permissions_for(user)
        if not result.can_view_channel:
            return Permission.permission_none
        
        #text channels dont have voice permissions
        result&=Permission.permission_deny_voice
        
        if self.type and (not Permission.can_manage_messages(result)):
            result=result&Permission.permission_deny_text
            return Permission(result)
        
        if not Permission.can_send_messages(result):
            result=result&Permission.permission_deny_text
        
        return Permission(result)

    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        name : `str`, Optional
            The channel's ``.name``.
        topic : `str`, Optional
            The channel's ``.topic``.
        slowmode : `int`, Optional
            The channel's ``.slowmode``.
        type : `int`, Optional
            The channel's ``.type``.
        nsfw : `int`, Optional
            Whether the channel is marked as nsfw.
        
        Returns
        -------
        channel : ``ChannelText``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            processable = []
            
            for key, details in (
                    ('name' , (2, 100)),
                    ('topic', (0,1024)),
                        ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_str(value, key, *details)
                    processable.append((key,value))
            
            try:
                slowmode = kwargs.pop('slowmode')
            except KeyError:
                pass
            else:
                slowmode = preconvert_int(slowmode, 'slowmode', 0, 21600)
                processable.append(('slowmode', slowmode))
            
            try:
                type_ = kwargs.pop('type')
            except KeyError:
                pass
            else:
                type_ = preconvert_int(type_, 'type', 0, 256)
                if (type_ not in cls.INTERCHANGE):
                    raise ValueError(f'`type` should be one of: {cls.INTERCHANGE!r}')
                
                processable.append(('type', type_))
            
            try:
                nsfw = kwargs.pop('nsfw')
            except KeyError:
                pass
            else:
                nsfw = preconvert_bool(nsfw, 'nsfw')
                processable.append(('nsfw', nsfw))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel._cache_perm = {}
            channel.category    = None
            channel.guild       = None
            channel.overwrites  = []
            channel.position    = 0
            channel.name        = ''

            channel.nsfw        = False
            channel.slowmode    = 0
            channel.topic       = ''

            channel._messageable_init()
            
            CHANNELS[channel_id]=channel
            
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel


class ChannelPrivate(ChannelBase, ChannelTextBase):
    """
    Represents a private (/ direct message) channel.
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the channel.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The monotonic time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's messag history reache it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    users : `list` of (``User`` or ``Client``) objects
        The channel's recipient.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(1,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    type : `int` = `1`
        The channel's Discord side type.
    """
    __slots__ = ('users',) #private related
    
    INTERCHANGE=(1,)
    type=1
    
    def _finish_init(self, data, client):
        """
        Finishes the channel's initialization with setting it's channel type specific attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data recevied from Discord.
        client : ``Client``
            The client, who received the channel data.
        """
        self.users=[User(data['recipients'][0]),client]
        self.users.sort()
        
        self._messageable_init()

    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelPrivate`` from partial data. Called by ``PartialChannel`` when a new partial channel is
        needed to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : `None`
            Compabtility parameter with the other channel types.
        
        Returns
        -------
        channel : ``ChannelPrivate``
        """
        self=object.__new__(cls)
        self._messageable_init()
        self.id         = channel_id
        # exactly what partial private channel data contains?
        self.users      = []
        
        return self
    
    def __str__(self):
        """Returns the channel's name."""
        return f'Direct Message {self.users[0]:f} with {self.users[1]:f}'

    def _delete(self, client):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        
        Parameters
        ----------
        client : ``Client``
            The client, who's private channel was deleted.
        """
        users=self.users
        if client is users[0]:
            user=users[1]
        else:
            user=users[0]
        
        del client.private_channels[user.id]
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        This method is just for compability with the other channel types.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        return
    
    def _update(self, data):
        """
        Updates the channel and returns it's overwritten old attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        This method is just for compability with the other channel types, what means it always returns an empty
        `dict`.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            Always empty.
        """
        return {}

    name = property(__str__)
    # Add docstring for name, if opt level is under 2
    if (name.__doc__ is not None):
        name.__doc__ = (
        """
        Returns the channel's name.
        
        Returns
        -------
        name : `str`
        """)
    
    display_name = property(__str__)
    if (display_name.__doc__ is not None):
        display_name.__doc__ = (
        """
        Returns the channel's display name.
        
        Returns
        -------
        display_name : `str`
        """)
    
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        """
        if user in self.users:
            if user.is_bot:
                return Permission.permission_private_bot
            else:
                return Permission.permission_private
            
        return Permission.permission_none
    
    cached_permissions_for = permissions_for
    
    @property
    def guild(self):
        """
        Returns the private channel's guild what is `None` every time.
        
        This property is just for compability with the other channel types.
        
        Returns
        -------
        guild : `None`
        """
        return None
    
    @classmethod
    def _dispatch(cls, data, client):
        """
        Discord sends a channel create event with each direct or group channel``Message``. This method decides
        whenever it is really a new channel (returns the channel), or it is just an another message (returns `None`).
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        client : ``Client``
            The client, who recived a message at the channel.
        
        Returns
        -------
        channel : `ChannelPrivate`` or `None`
        """
        channel_id=int(data['id'])
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)
            channel.id=channel_id
            CHANNELS[channel_id]=channel
            channel._finish_init(data,client)
            result=channel
        else:
            result=None #returning None is intended.
        
        if channel.users[0] is client:
            user=channel.users[1]
        else:
            user=channel.users[0]
        client.private_channels[user.id]=channel
        
        return result
    
    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the channel.
        
        Returns
        -------
        channel : ``ChannelPrivate``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            raise ValueError(f'Unused or unsettable attributes: {kwargs}')
        
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)
            
            channel.id = channel_id
            
            channel.users = []
            
            channel._messageable_init()
            
            CHANNELS[channel_id]=channel
        
        return channel


class ChannelVoice(ChannelGuildBase):
    """
    Represents a ``Guild`` voice channel.
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the channel.
    _cache_perm : `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermOW`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(2,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `2`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `2`
        The channel's Discord side type.
    """
    __slots__ = ('bitrate',  'user_limit') #Voice channel related
    
    ORDER_GROUP = 2
    INTERCHANGE = (2,)
    type = 2

    def _finish_init(self, data, guild):
        """
        Finishes the channel's initialization with setting it's channel type specific attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data recevied from Discord.
        guild : ``Guild``
            The channel's guild.
        """
        self._cache_perm={}
        self.name=data['name']
        
        self._init_catpos(data, guild)
        self.overwrites=self._parse_overwrites(data)
        
        self.bitrate=data['bitrate']
        self.user_limit=data['user_limit']
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelVoice`` from partial data. Called by ``PartialChannel`` when a new partial channel is needed
        to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : ``Guild`` or `None`
            The channel's guild if applicable.
        
        Returns
        -------
        channel : ``ChannelVoice``
        """
        self=object.__new__(cls)
        
        self._cache_perm= {}
        self.bitrate    = 0
        self.category   = None
        self.guild      = partial_guild
        self.id         = channel_id
        self.name       = data.get('name','')
        self.overwrites = []
        self.position   = 0
        self.user_limit = 0
        
        return self
    
    @property
    def display_name(self):
        """
        A voice channel's display name is it's capitalized name.
        
        Returns
        -------
        display_name : `str`
        """
        return self.name.capitalize()
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        self.guild=None
        del guild.all_channel[self.id]
        
        self.category.channels.remove(self)
        self.category=None
        #safe delete
        
        if self is guild.afk_channel:
            guild.afk_channel=None
        
        self.overwrites.clear()
        self._cache_perm.clear()
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        self._cache_perm.clear()
        self._set_catpos(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name=data['name']
        self.bitrate=data['bitrate']
        self.user_limit=data['user_limit']
    
    def _update(self,data):
        """
        Updates the channel and returns it's overwritten old attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------------------+
        | Keys          | Values                            |
        +===============+===================================+
        | bitrate       | `int`                             |
        +---------------+-----------------------------------+
        | category      | ``ChannelCategory`` or ``Guild``  |
        +---------------+-----------------------------------+
        | name          | `str`                             |
        +---------------+-----------------------------------+
        | overwrites    | `list` of ``PermOW``              |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        | user_limit    | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm.clear()
        old_attributes = {}
        
        name=data['name']
        if self.name!=name:
            old_attributes['name']=self.name
            self.name=name
        
        bitrate=data['bitrate']
        if self.bitrate!=bitrate:
            old_attributes['bitarate']=self.bitrate
            self.bitrate=bitrate
        
        user_limit=data['user_limit']
        if self.user_limit!=user_limit:
            old_attributes['user_limit']=self.user_limit
            self.user_limit=user_limit
        
        overwrites=self._parse_overwrites(data)
        if self.overwrites!=overwrites:
            old_attributes['overwrites']=self.overwrites
            self.overwrites=overwrites
        
        self._update_catpos(data, old_attributes)
        
        return old_attributes
    
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        
        See Also
        --------
        .cached_permissions_for : Cached permission calculator.
        """
        if user==self.guild.owner:
            return Permission.permission_deny_text
        
        result=self._permissions_for(user)
        if not result.can_view_channel:
            return Permission.permission_none
        
        #voice channels dont have text permissions
        result&=Permission.permission_deny_text
        
        if not Permission.can_connect(result):
            result&=Permission.permission_deny_voice_con
        
        return Permission(result)
    
    @property
    def voice_users(self):
        """
        Returns a list of the users, who are in the voice channel.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        result=[]
        guild = self.guild
        if guild is None:
            return result
        
        for state in guild.voice_states.values():
            if state.channel is self:
                result.append(state.user)
        return result

    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        name : `str`, Optional
            The channel's ``.name``.
        bitrate : `int`, Optional
            The channel's ``.bitrate``.
        user_limit : `int`, Optional
            The channel's ``.user_limit``.
        
        Returns
        -------
        channel : ``ChannelVoice``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 100)
                processable.append(('name',name))
            
            for key, details in (
                    ('bitrate'   , (8000, 384000)),
                    ('user_limit', (    0,    99)),
                        ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_int(value, key, *details)
                    processable.append((key,value))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel._cache_perm = {}
            channel.category    = None
            channel.guild       = None
            channel.overwrites  = []
            channel.position    = 0
            channel.name        = ''

            channel.bitrate     = 64000
            channel.user_limit  = 0
            
            CHANNELS[channel_id]=channel
        
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel


class ChannelGroup(ChannelBase, ChannelTextBase):
    """
    Represents a group channel.
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the channel.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The monotonic time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's messag history reache it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    users : `list` of (``User`` or ``Client``) objects
        The channel's recipient.
    icon_hash : `int`
        The channel's icon's hash in `uint128`.
    icon_type : ``iconType``
        The channel's icon's type.
    name : `str`
        The channel's display name. Can be empty string if the channel has no name.
    owner : ``User`` or ``Client``
        The group channel's owner.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(3,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    type : `int` = `3`
        The channel's Discord side type.
    """
    __slots__ = ('users', # private channel related
        'name', 'owner',) #group channel related
    
    icon = IconSlot('icon', 'icon', URLS.channel_group_icon_url, URLS.channel_group_icon_url_as)
    
    INTERCHANGE = (3,)
    type = 3

    def _finish_init(self, data, client):
        """
        Finishes the channel's initialization with setting it's channel type specific attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data recevied from Discord.
        client : ``Client``
            The client, who received the channel data.
        """
        self._messageable_init()
        
        name=data.get('name',None)
        self.name = '' if name is None else name
        
        self._set_icon(data)
        
        users = [User(user_data) for user_data in data['recipients']]
        users.sort()
        self.users = users
        
        owner_id=int(data['owner_id'])
        for user in users:
            if user.id==owner_id:
                owner=user
                break
        else:
            owner=ZEROUSER
        
        self.owner = owner
        
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelGroup`` from partial data. Called by ``PartialChannel`` when a new partial channel is needed
        to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : `None`
            Compabtility parameter with the other channel types.
        
        Returns
        -------
        channel : ``ChannelGroup``
        """
        self=object.__new__(cls)
        self._messageable_init()
        self.id         = channel_id
        # even if we get recipients, we will ignore them
        self.users      = []
        
        self._set_icon(data)
        
        name=data.get('name',None)
        #should we transfer the recipients to name?
        self.name='' if name is None else name
        
        self.owner=ZEROUSER
        
        return self
        
    def _delete(self, client):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        
        Parameters
        ----------
        client : ``Client``
            The client, who's private channel was deleted.
        """
        del client.group_channels[self.id]

    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        name=data.get('name',None)
        self.name = '' if name is None else name
        
        self._set_icon(data)
        
        users = [User(user) for user in data['recipients']]
        users.sort()
        self.users = users
        
        owner_id=int(data['owner_id'])
        for user in users:
            if user.id==owner_id:
                self.owner=user
                break
    
    def _update(self, data):
        """
        Updates the channel and returns it's overwritten old attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+---------------------------------------+
        | Keys          | Values                                |
        +===============+=======================================+
        | icon          | ``Icon``                              |
        +---------------+---------------------------------------+
        | name          | `str`                                 |
        +---------------+---------------------------------------+
        | owner         | ``User`` or ``Client``                |
        +---------------+---------------------------------------+
        | users         | `list` of (``User`` or ``Client``)    |
        +---------------+---------------------------------------+
        """
        old_attributes = {}
        
        name=data.get('name',None)
        if name is None:
            name=''
        if self.name!=name:
            old_attributes['name']=self.name
            self.name=name
        
        self._update_icon(data, old_attributes)
        
        users = [User(user) for user in data['recipeents']]
        users.sort()
        
        if self.users!=users:
            old_attributes['users']=self.users
            self.users=users
        
        owner_id=int(data['owner_id'])
        if self.owner.id!=owner_id:
            for user in users:
                if user.id==owner_id:
                    owner=user
                    break
            else:
                owner=ZEROUSER
            old_attributes['owner']=self.owner
            self.owner=owner
        
        return old_attributes

    def __str__(self):
        """Returns the channel's name."""
        name = self.name
        if name:
            return name
        
        users=self.users
        if users:
            return ', '.join([user.name for user in users])
        
        return 'Unnamed'
    
    display_name = property(__str__)
    if (display_name.__doc__ is not None):
        display_name.__doc__ = (
        """
        Returns the channel's display name.
        
        Returns
        -------
        display_name : `str`
        """)
    
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        """
        if self.owner==user:
            return Permission.permission_group_owner
        elif user in self.users:
            return Permission.permission_group
        else:
            return Permission.permission_none
    
    cached_permissions_for = permissions_for
    
    @property
    def guild(self):
        """
        Returns the group channel's guild what is `None` every time.
        
        This property is just for compability with the other channel types.
        
        Returns
        -------
        guild : `None`
        """
        return None
    
    @classmethod
    def _dispatch(cls, data, client):
        """
        Discord sends a channel create event with each direct or group channel``Message``. This method decides
        whenever it is really a new channel (returns the channel), or it is just an another message (returns `None`).
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        client : ``Client``
            The client, who recived a message at the channel.
        
        Returns
        -------
        channel : `ChannelGroup`` or `None`
        """
        channel_id=int(data['id'])
        if channel_id in CHANNELS:
            return
        
        channel=object.__new__(cls)
        channel.id=channel_id
        CHANNELS[channel_id]=channel
        client.group_channels[channel_id]=channel
        channel._finish_init(data, client)
        return channel
    
    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        name : `str`, Optional
            The channel's ``.name``.
        icon : `int`, Optional
            The channel's ``.icon``.
        owner : ``User`` or ``Client, Optional
            The channel's ``.owner``.
        
        Returns
        -------
        channel : ``ChannelGroup``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 100)
                processable.append(('name', name))
            
            cls.icon.preconvert(kwargs, processable)
            
            try:
                owner = kwargs.pop('owner')
            except KeyError:
                pass
            else:
                if not isinstance(owner,(User,Client)):
                    raise TypeError(f'`owner` can be {User.__name__} or {Client.__name__} instance, got {owner.__class__.__name__}.')
                processable.append(('owner', owner))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)
            
            channel.id = channel_id
            
            channel.users = []
            
            channel.name = ''
            channel.icon_hash = 0
            channel.icon_type = ICON_TYPE_NONE
            channel.owner = ZEROUSER
            
            channel._messageable_init()
            
            CHANNELS[channel_id]=channel
            
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel

class ChannelCategory(ChannelGuildBase):
    """
    Represents a ``Guild`` channel category.
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the channel.
    _cache_perm : `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions.
    category : `None` or ``Guild``
        The channel's category. Category channels can not be in an other category, so it is always set to their
        `.guild`. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermOW`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    channels : `autoposlist`
        A list like datatype to store the category's channels in order.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(4,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `4`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `4`
        The channel's Discord side type.
    """
    __slots__=('channels',) #channel category related
    
    ORDER_GROUP = 4
    INTERCHANGE = (4,)
    type = 4

    def _finish_init(self, data, guild):
        """
        Finishes the channel's initialization with setting it's channel type specific attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data recevied from Discord.
        guild : ``Guild``
            The channel's guild.
        """
        self._cache_perm={}
        self.name=data['name']
        
        self._init_catpos(data, guild)
        self.overwrites=self._parse_overwrites(data)
        
        self.channels=autoposlist()
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelCategory`` from partial data. Called by ``PartialChannel`` when a new partial channel is
        needed to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : ``Guild`` or `None`
            The channel's guild if applicable.
        
        Returns
        -------
        channel : ``ChannelCategory``
        """
        self=object.__new__(cls)
        
        self._cache_perm= {}
        self.category   = None
        self.channels   = autoposlist()
        self.guild      = partial_guild
        self.id         = channel_id
        self.name       = data.get('name','')
        self.overwrites = []
        self.position   = 0
        
        return self
    
    @property
    def display_name(self):
        """
        A catgory channel's display name is it's name with uppercase characters.
        
        Returns
        -------
        display_name : `str`
        """
        return self.name.upper()
        
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        self._cache_perm.clear()
        self._set_catpos(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name=data['name']
        
    def _update(self, data):
        """
        Updates the channel and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------------------+
        | Keys          | Values                            |
        +===============+===================================+
        | name          | `str`                             |
        +---------------+-----------------------------------+
        | overwrites    | `list` of ``PermOW``              |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm.clear()
        old_attributes = {}

        name=data['name']
        if self.name!=name:
            old_attributes['name']=self.name
            self.name=name

        overwrites=self._parse_overwrites(data)
        if self.overwrites!=overwrites:
            old_attributes['overwrites']=self.overwrites
            self.overwrites=overwrites

        self._update_catpos(data, old_attributes)
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild=self.guild
        if guild is None:
            return
        
        self.guild=None
        del guild.all_channel[self.id]
        
        self.category.channels.remove(self)
        self.category=None
        
        #self.channels.clear() #if this really happens we will know it
        self.overwrites.clear()
        self._cache_perm.clear()
    
    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        name : `str`, Optional
            The channel's ``.name``.
        
        Returns
        -------
        channel : ``ChannelText``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 100)
                processable.append(('name', name))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)

            channel.id          = channel_id

            channel._cache_perm = {}
            channel.category    = None
            channel.guild       = None
            channel.overwrites  = []
            channel.position    = 0
            channel.name        = ''
            
            CHANNELS[channel_id]=channel
            
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel


class ChannelStore(ChannelGuildBase):
    """
    Represents a ``Guild`` store channel.
    
    Attributes
    ----------
    id : `int`
        Unique identificator of the channel.
    _cache_perm : `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermOW`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(6,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `6`
        The channel's Discord side type.
    """
    __slots__ = ('nsfw',) #guild channel store related
    
    ORDER_GROUP = 0
    INTERCHANGE = (6,)
    type = 6
    
    def _finish_init(self, data, guild):
        """
        Finishes the channel's initialization with setting it's channel type specific attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data recevied from Discord.
        guild : ``Guild``
            The channel's guild.
        """
        self._cache_perm={}
        self.name=data['name']
        self.nsfw=data.get('nsfw',False)
        
        self._init_catpos(data, guild)
        self.overwrites=self._parse_overwrites(data)
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelStore`` from partial data. Called by ``PartialChannel`` when a new partial channel is needed
        to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : ``Guild`` or `None`
            The channel's guild if applicable.
        
        Returns
        -------
        channel : ``ChannelStore``
        """
        self=object.__new__(cls)
        
        self._cache_perm= {}
        self.category   = None
        self.guild      = partial_guild
        self.id         = channel_id
        self.name       = data.get('name','')
        self.nsfw       = False
        self.overwrites = []
        self.position   = 0
        
        return self
        
    @property
    def display_name(self):
        """
        A store channel's display name is it's name with lovercase characters.
        
        Returns
        -------
        display_name : `str`
        """
        return self.name.lower()
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        self._cache_perm.clear()
        self._set_catpos(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name=data['name']
        self.nsfw=data.get('nsfw',False)
        
    def _update(self,data):
        """
        Updates the channel and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------------------+
        | Keys          | Values                            |
        +===============+===================================+
        | category      | ``ChannelCategory`` or ``Guild``  |
        +---------------+-----------------------------------+
        | name          | `str`                             |
        +---------------+-----------------------------------+
        | nsfw          | `bool`                            |
        +---------------+-----------------------------------+
        | overwrites    | `list` of ``PermOW``              |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm.clear()
        old_attributes = {}
        
        name=data['name']
        if self.name!=name:
            old_attributes['name']=self.name
            self.name=name
        
        nsfw=data.get('nsfw',False)
        if self.nsfw!=nsfw:
            old_attributes['nsfw']=self.nsfw
            self.nsfw=nsfw
        
        overwrites=self._parse_overwrites(data)
        if self.overwrites!=overwrites:
            old_attributes['overwrites']=self.overwrites
            self.overwrites=overwrites
        
        self._update_catpos(data, old_attributes)
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild=self.guild
        if guild is None:
            return
        
        self.guild=None
        del guild.all_channel[self.id]
        
        self.category.channels.remove(self)
        self.category=None
            
        self.overwrites.clear()
        self._cache_perm.clear()

    def permissions_for(self,user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        
        See Also
        --------
        .cached_permissions_for : Cached permission calculator.
        """
        if user==self.guild.owner:
            return Permission.permission_deny_both
        
        result=self._permissions_for(user)
        if not result.can_view_channel:
            return Permission.permission_none
        
        #store channels do not have text and voice related permissions
        result&=Permission.permission_deny_both
        
        return Permission(result)

    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        name : `str`, Optional
            The channel's ``.name``.
        nsfw : `int`, Optional
            Whether the channel is marked as nsfw.
        
        Returns
        -------
        channel : ``ChannelText``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 100)
                processable.append(('name', name))
            
            try:
                nsfw = kwargs.pop('nsfw')
            except KeyError:
                pass
            else:
                nsfw = preconvert_bool(nsfw, 'nsfw')
                processable.append(('nsfw', nsfw))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            channel=CHANNELS[channel_id]
        except KeyError:
            channel=object.__new__(cls)
            
            channel.id          = channel_id
            
            channel._cache_perm = {}
            channel.category    = None
            channel.guild       = None
            channel.overwrites  = []
            channel.position    = 0
            channel.name        = ''
            
            channel.nsfw        = False
            
            CHANNELS[channel_id]=channel
            
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel

CHANNEL_TYPES = (
    ChannelText,
    ChannelPrivate,
    ChannelVoice,
    ChannelGroup,
    ChannelCategory,
    ChannelText,
    ChannelStore,
        )

def cr_pg_channel_object(name, type_, overwrites=None, topic=None, nsfw=False, slowmode=0, bitrate=64000, user_limit=0,
        bitrate_limit=96000, category_id=None):
    """
    Creates a json serializable object representing a ``GuildChannelBase`` instance. The unused parameters of the
    created channel's type are ignored.
    
    Parameters
    ----------
    name : `str`
        The name of the channel. Can be between `2` and `100` characters.
    type_ : `int` or ``ChannelGuildBase`` subclass
        The channel's type.
    overwrites : `list` of ``cr_p_overwrite_object`` returns, Optional
        A list of permission overwrites of the channel. The list should contain json serializable permission
        overwrites made by the ``cr_p_overwrite_object`` function.
    topic : `str`, Optional
        The channel's topic.
    nsfw : `bool`, Optional
        Whether the channel is marked as nsfw.
    slowmode : int`, Optional
        The channel's slowmode value.
    bitrate : `int`, Optional
        The channel's bitrate.
    user_limit : `int`, Optional
        The channel's user limit.
    bitrate_limit : `int`, Optional
        What is the maximal allowed bitrate for the channel. If the passed `bitrate` is over the passed `bitrate_limit`
        raises `ValueError`.
    category_id : `int`, Optional
        The channel's category's id. If the category is under a guild, leave it empty.
    
    Returns
    -------
    channel_data : `dict` of (`str`, `Any`) items
    
    Raises
    ------
    TypeError
        If `type_` was not passed as `int` or as ``ChannelGuildBase`` instance.
    ValueError
        - If `type_` was passed as `int`, but as negative or if there is no channel type for the given value.
        - If `name`'s length is under `2` or over `100`.
        - If `topic`'s length is over `1024`.
        - If channel type is changed, but not to an expected one.
        - If `slowmode` is not between `0` and `21600`.
        - If `bitrate` is lower than `8000` or higher than `bitrate_limit`.
        - If `user_limit` is negative or over `99`.
    
    Notes
    -----
    `bitrate_limit` should be `96000`. `128000` max for vip, or `128000`, `256000`, `384000` max depending on the
    premium tier of the respective guild.
    """
    if type(type_) is int:
        if type_<0:
            raise ValueError(f'`type_` cannot be negative value, got `{type_!r}`.')
        if type_>=len(CHANNEL_TYPES):
            raise ValueError(f'`type_` exceeded the defined channel type limit. Limit: `{len(CHANNEL_TYPES)-1!r}`, '
                f'got `{type_}`.')
        
        if not issubclass(CHANNEL_TYPES[type_],ChannelGuildBase):
            raise TypeError(f'The function accepts type values refering to a {ChannelGuildBase.__name__}, meanwhile '
                f'it refers to {CHANNEL_TYPES[type_].__name__}.')
        
        type_value=type_
    
    elif isinstance(type_,type) and issubclass(type_,ChannelBase):
        if not isinstance(type_,ChannelGuildBase):
            raise TypeError(f'The function accepts only {ChannelGuildBase.__name__} instances, got {type_.__name__}.')
        type_value=type_.INTERCHANGE[0]
    
    else:
        if not issubclass(type_,type):
            type_ = type_.__class__
        raise ValueError(f'`type_` argument should be `int` or `{ChannelGuildBase.__name__}` subclass, '
            f'got {type.__name__}.')
    
    name_ln=len(name)
    if name_ln<2 or name_ln>100:
        raise ValueError(f'`name` length should be between 2-100, got `{name!r}`.')
    
    if overwrites is None:
        overwrites=[]
    
    channel_data = {
        'name'                  : name,
        'type'                  : type_value,
        'permission_overwrites' : overwrites,
            }
    
    # any Guild Text channel type
    if type_value in ChannelText.INTERCHANGE:
        if (topic is not None):
            topic_ln=len(topic)
            if topic_ln>1024:
                raise ValueError(f'`topic` length can be betwen 0-1024, got `{topic!r}`.')
            if topic_ln!=0:
                channel_data['topic']=topic
    
    # any Guild Text or any Guild Store channel type
    if (type_value in ChannelText.INTERCHANGE) or (type_value in ChannelStore.INTERCHANGE):
        if nsfw:
            channel_data['nsfw']=nsfw
    
    # Guild Text channel type only
    if type_value == ChannelText.INTERCHANGE[0]:
        if slowmode<0 or slowmode>21600:
            raise ValueError(f'Invalid `slowmode`, should be 0-21600, got `{slowmode!r}`.')
        channel_data['rate_limit_per_user']=slowmode
    
    # any Guild Voice channel type
    if type_value in ChannelVoice.INTERCHANGE:
        if bitrate<8000 or bitrate>bitrate_limit:
            raise ValueError(f'`bitrate` should be 8000-96000. 128000 max for vip, or 128000, 256000, 384000 max '
                f'depending on premium tier. Got `{bitrate!r}`.')
        channel_data['bitrate']=bitrate
        
        if user_limit<0 or user_limit>99:
            raise ValueError(f'`user_limit` should be 0 for unlimited or 1-99, got `{user_limit!r}`.')
        channel_data['user_limit']=user_limit
    
    if type_value not in ChannelCategory.INTERCHANGE:
        if (category_id is not None):
            channel_data['parent_id']=category_id
    
    return channel_data

#scopes

webhook.ChannelText = ChannelText
message.ChannelBase = ChannelBase
message.ChannelTextBase = ChannelTextBase
message.ChannelGuildBase = ChannelGuildBase
message.ChannelText = ChannelText
message.ChannelPrivate = ChannelPrivate
message.ChannelGroup = ChannelGroup
ratelimit.ChannelBase = ChannelBase
ratelimit.ChannelGuildBase = ChannelGuildBase
http.ChannelGuildBase = ChannelGuildBase

del message
del webhook
del URLS
del ratelimit
del DiscordEntity
del WeakSet
del http
