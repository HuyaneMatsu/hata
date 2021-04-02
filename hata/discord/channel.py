# -*- coding: utf-8 -*-
__all__ = ('ChannelBase', 'ChannelCategory', 'ChannelGroup', 'ChannelGuildBase', 'ChannelPrivate', 'ChannelStage',
    'ChannelStore', 'ChannelText', 'ChannelTextBase', 'ChannelThread', 'ChannelVoice', 'MessageIterator',
    'cr_pg_channel_object', 'ChannelGuildUndefined',)

import re
from collections import deque
from weakref import WeakSet

from ..backend.utils import _spaceholder, DOCS_ENABLED
from ..backend.event_loop import LOOP_TIME

from .bases import DiscordEntity, IconSlot, ICON_TYPE_NONE
from .client_core import CHANNELS, USERS
from .permission import Permission, PERMISSION_NONE, PERMISSION_ALL, PERMISSION_PRIVATE, PERMISSION_PRIVATE_BOT, \
    PERMISSION_GROUP, PERMISSION_GROUP_OWNER, PERMISSION_TEXT_DENY, PERMISSION_VOICE_DENY, PERMISSION_STAGE_MODERATOR, \
    PERMISSION_VOICE_DENY_CONNECTION, PERMISSION_TEXT_AND_VOICE_DENY, PERMISSION_TEXT_AND_STAGE_DENY
from .http import URLS
from .message import Message, MESSAGES
from .user import User, ZEROUSER
from .role import PermissionOverwrite
from .client_core import GC_CYCLER
from .webhook import Webhook, WebhookRepr
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_int, preconvert_bool, \
    preconvert_preinstanced_type
from .utils import DATETIME_FORMAT_CODE
from .client_utils import maybe_snowflake
from .exceptions import DiscordException, ERROR_CODES
from .preinstanced import VoiceRegion, VideoQualityMode

from . import webhook as module_webhook, message as module_message, rate_limit as module_rate_limit

Client = NotImplemented
Guild = NotImplemented

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

def create_partial_channel(data, partial_guild=None):
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
    
    channel_id = int(data['id'])
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass
    
    cls = CHANNEL_TYPES.get(data['type'], ChannelGuildUndefined)
    
    channel = cls._from_partial_data(data, channel_id, partial_guild)
    CHANNELS[channel_id] = channel
    
    return channel

class ChannelBase(DiscordEntity, immortal=True):
    """
    Base class for Discord channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    
    Notes
    -----
    Channels support weakreferencing.
    """
    INTERCHANGE = ()
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a new channel from the channel data received from Discord. If the channel already exists and if it
        is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        
        Raises
        -------
        RuntimeError
            The respective channel type cannot be instanced.
        """
        raise RuntimeError(f'`{cls.__name__}` cannot be instanced.')
    
    def __repr__(self):
        """Returns the representation of the channel."""
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
        ```py
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
        ```
        """
        if not code:
            return self.__str__()
        
        if code == 'm':
            return f'<#{self.id}>'
        
        if code == 'd':
            return self.display_name
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
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
        if (not 1 < len(name) < 38):
            return default
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if user.discriminator == discriminator and user.name == name_:
                        return user
        
        if len(name) > 32:
            return default
        
        for user in users:
            if user.name == name:
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
        if (not 1 < len(name) < 38):
            return default
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if user.discriminator == discriminator and user.name == name_:
                        return user
        
        if len(name) > 32:
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        for user in users:
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
        result = []
        if (not 1 < len(name) < 38):
            return result
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if user.discriminator == discriminator and user.name == name_:
                        result.append(user)
                        break
        
        if len(name) > 32:
            return result
        
        pattern = re.compile(re.escape(name), re.I)
        for user in users:
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
        result = []
        for user in self.users:
            if type(user) is User:
                continue
            result.append(user)
        
        return result
    
    #for sorting channels
    def __gt__(self, other):
        """Returns whether this channel's id is greater than the other's."""
        if isinstance(other, ChannelBase):
            return self.id > other.id
        return NotImplemented
    
    def __ge__(self, other):
        """Returns whether this channel's id is greater or equal than the other's."""
        if isinstance(other, ChannelBase):
            return self.id >= other.id
        return NotImplemented
    
    def __eq__(self, other):
        """Returns whether this channel's id is equal to the other's."""
        if isinstance(other, ChannelBase):
            return self.id == other.id
        return NotImplemented
    
    def __ne__(self,other):
        """Returns whether this channel's id is not equal to the other's."""
        if isinstance(other, ChannelBase):
            return self.id != other.id
        return NotImplemented
    
    def __le__(self, other):
        """Returns whether this channel's id is less or equal than the other's."""
        if isinstance(other, ChannelBase):
            return self.id <= other.id
        return NotImplemented
    
    def __lt__(self, other):
        """Returns whether this channel's id is less than the other's."""
        if isinstance(other, ChannelBase):
            return self.id < other.id
        return NotImplemented
    
    @property
    def name(self):
        """
        Returns the channel's name.
        
        Subclasses should overwrite it.
        
        Returns
        -------
        name : `str`
        """
        return self.__class__.__name__
    
    def has_name_like(self, name):
        """
        Returns whether the channel's name is like the given string.
        
        Parameters
        ----------
        name : `str`
            The name of the channel
        
        Returns
        -------
        channel : ``ChannelBase`` instance
        """
        if name.startswith('#'):
            name = name[1:]
        
        target_name_length = len(name)
        if target_name_length<2 or target_name_length>100:
            return False
        
        if re.match(re.escape(name), self.name, re.I) is None:
            return False
        
        return True
    
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
        ``.cached_permissions_for`` : Cached permission calculator.
        
        Notes
        -----
        Always return empty permissions. Subclasses should implement this method.
        """
        return PERMISSION_NONE
    
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
        Mainly designed for getting clients' permissions and stores only their as well. Do not caches other user's
        permissions.
        
        Always return empty permissions. Subclasses should implement this method.
        """
        return PERMISSION_NONE
    
    def permissions_for_roles(self, *roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        
        Always return empty permissions. Subclasses should implement this method.
        """
        return PERMISSION_NONE

# sounds funny, but this is a class
# the chunk_size is 97, because it means 1 request for _load_messages_till
class MessageIterator:
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
        channel : ``ChannelTextBase`` or `int` instance
            The channel, what's messages the message iterator will iterates over.
        chunk_size : `int`, Optional
            The amount of messages, what the message iterator will extend it's channel's message history, each time, the
            loaded messages are exhausted. Limited to `97` as a maximal value.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``ChannelTextBase`` nor `int` instance.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `chunk_size` was not given as `int` instance.
            - If `chunk_size` is out of range [1:].
        """
        if __debug__:
            if not isinstance(chunk_size, int):
                raise AssertionError(f'`chunk_size` can be given as `int` instance, got {chunk_size.__class__.__name__}.')
            
            if chunk_size < 1:
                raise AssertionError(f'`chunk_size` is out from the expected [0:] range, got {chunk_size!r}.')
        
        if chunk_size > 99:
            chunk_size = 99
        
        if isinstance(channel, ChannelTextBase):
            pass
        else:
            channel_id = maybe_snowflake(channel)
            if channel_id is None:
                raise TypeError(f'`channel` can be given as `{ChannelTextBase.__name__}` instance, got'
                    f'{channel.__class__.__name__}.')
            
            channel = CHANNELS.get(channel_id)
            
            if channel is None:
                try:
                    messages = await client.message_get_chunk_from_zero(channel_id, 100)
                except BaseException as err:
                    if isinstance(err, DiscordException) and err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                                ):
                        pass
                    
                    else:
                        raise
                else:
                    if messages:
                        channel = messages[0].channel
                    else:
                        channel = await client._maybe_get_channel(channel_id)
        
        self = object.__new__(cls)
        self.client = client
        self.channel = channel
        self.chunk_size = chunk_size
        self._index = 0
        self._can_read_history = not channel.cached_permissions_for(client).can_read_message_history
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
        
        index = self._index
        messages = channel.messages
        if (messages is not None) and (len(messages) > index):
            self._index = index+1
            return channel.messages[index]
        
        if channel.message_history_reached_end or self._can_read_history:
            raise StopAsyncIteration
        
        try:
            await self.client._load_messages_till(channel, index+self.chunk_size)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                pass
            
            elif isinstance(err, DiscordException) and err.code in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # message's channel deleted
                ERROR_CODES.invalid_access, # client removed
                ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                    ):
                pass
            else:
                raise
        
        messages = channel.messages
        if (messages is not None) and (len(channel.messages) > index):
            self._index = index+1
            return channel.messages[index]
        
        raise StopAsyncIteration
    
    def __repr__(self):
        """Returns the representation of the message iterator."""
        return (f'<{self.__class__.__name__} of client {self.client.full_name}, at channel {self.channel.name!r} ('
            f'{self.channel.id})>')

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
    
    Class attributes
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
    
    def _get_message_keep_limit(self):
        return self._message_keep_limit
    
    def _set_message_keep_limit(self, limit):
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
    
    message_keep_limit = property(_get_message_keep_limit, _set_message_keep_limit)
    del _get_message_keep_limit, _set_message_keep_limit
    # If opt level is under2, set docstring
    if DOCS_ENABLED:
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
        
        try:
            return MESSAGES[message_id]
        except KeyError:
            pass
        
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
        delete_ln = len(delete_ids)
        if not delete_ln:
            return found, missed
        
        messages = self.messages
        delete_ids.sort(reverse=True)
        if messages is None:
            messages_ln = 0
        else:
            messages_ln = len(messages)
        
        if messages is None:
            messages_index = 0
        else:
            messages_index = message_relative_index(messages, delete_ids[0])
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
                        missed.append(delete_id)
                    else:
                        message.deleted = True
                        found.append(message)
                        
                    delete_index += 1
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
                
                message.deleted = True
                found.append(message)
                
                messages_ln -= 1
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

class ChannelGuildBase(ChannelBase):
    """
    Base class for guild channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
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

    def _init_category_and_position(self, data, guild):
        """
        Initializes the `.category` and the `.position` of the channel. If a channel is under the ``Guild.md``,
        and not in a category (category channels are all like these), then their `.category` is the ``Guild`` itself.
        This method is used when we initialize a guild channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        guild : ``Guild``
            The guild of the channel.
        """
        self.guild = guild
        guild.channels[self.id] = self
        
        self.position = data.get('position', 0)
        
        category_id = data.get('parent_id')
        if category_id is None:
            category = guild
        else:
            category = guild.channels[int(category_id)]
        
        self.category = category
    
    def _set_category_and_position(self, data):
        """
        Similar to the ``._init_category_and_position`` method, but this method applies the changes too, so moves the channel
        between categories and moves the channel inside of the category too, to keep the order.
        
        Called from `._update_no_return` when updating a guild channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord
        """
        guild = self.guild
        if guild is None:
            return
        
        new_category_id = data.get('parent_id')
        if new_category_id is None:
            new_category = guild
        else:
            new_category = guild.channels[int(new_category_id)]
        
        position=data.get('position',0)
        
        category = self.category
        if category is new_category:
            if self.position != position:
                self.position = position
        
        else:
            self.position = position
            self.category = new_category
    
    def _update_category_and_position(self, data, old_attributes):
        """
        Acts same as ``._set_category_and_position``, but it sets the modified attributes' previous value to
        `old_attributes`.
        
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
        
        new_category_id = data.get('parent_id')
        if new_category_id is None:
            new_category = guild
        else:
            new_category = guild.channels[int(new_category_id)]
        
        position = data.get('position', 0)
        
        category = self.category
        if category is new_category:
            if self.position != position:
                old_attributes['position'] = self.position
                self.position = position
        else:
            old_attributes['category'] = category
            old_attributes['position'] = self.position
            
            self.position = position
            self.category = category
    
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
            return PERMISSION_NONE
        
        default_role =  guild.roles.get(guild.id)
        if default_role is None:
            base = 0
        else:
            base = default_role.permissions
        
        try:
            guild_profile = user.guild_profiles[guild]
        except KeyError:
            if isinstance(user, (Webhook, WebhookRepr)) and user.channel is self:
                
                overwrites = self.overwrites
                if overwrites:
                    overwrite = overwrites[0]
                    
                    if overwrite.target_role is default_role:
                        base = (base&~overwrite.deny)|overwrite.allow
                
                return Permission(base)
            
            return PERMISSION_NONE
        
        roles = guild_profile.roles
        if (roles is not None):
            roles.sort()
            for role in roles:
                base |= role.permissions
        
        if Permission.can_administrator(base):
            return PERMISSION_ALL
        
        overwrites = self.overwrites
        if overwrites:
            overwrite = overwrites[0]
            
            if overwrite.target_role is default_role:
                base = (base&~overwrite.deny)|overwrite.allow
            
            for overwrite in overwrites:
                overwrite_target_role = overwrite.target_role
                if (overwrite_target_role is not None):
                    if roles is None:
                        continue
                    
                    if overwrite_target_role not in roles:
                        continue
                
                else:
                    if overwrite.target_user_id != user.id:
                        continue
                
                base = (base&~overwrite.deny)|overwrite.allow
        
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
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_ALL
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            result = PERMISSION_NONE
        
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
        Mainly designed for getting clients' permissions and stores only their as well. Do not caches other user's
        permissions.
        """
        if not isinstance(user, Client):
            return self.permissions_for(user)
        
        cache_perm = self._cache_perm
        if cache_perm is None:
            self._cache_perm = cache_perm = {}
        else:
            try:
                return cache_perm[user.id]
            except KeyError:
                pass
        
        permissions = self.permissions_for(user)
        cache_perm[user.id] = permissions
        return permissions
    
    def _permissions_for_roles(self, roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles. This method is called
        first by subclasses to apply their own related permissions on it.
        
        Parameters
        ----------
        roles : `tuple` of ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        default_role =  guild.roles.get(guild.id)
        if default_role is None:
            base = 0
        else:
            base = default_role.permissions
        
        for role in sorted(roles):
            if role.guild is self:
                base |= role.permissions
        
        if Permission.can_administrator(base):
            return PERMISSION_ALL
        
        roles = set(roles)
        
        overwrites = self.overwrites
        if overwrites:
            overwrite = overwrites[0]
            
            if overwrite.target_role is default_role:
                base = (base&~overwrite.deny)|overwrite.allow
            
            for overwrite in overwrites:
                overwrite_target_role = overwrite.target_role
                if (overwrite_target_role is None):
                    continue
                
                if overwrite_target_role not in roles:
                    continue
                
                base = (base&~overwrite.deny)|overwrite.allow
        
        return Permission(base)
    
    def permissions_for_roles(self, *roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            result = PERMISSION_NONE
        
        return result
    
    def _parse_overwrites(self, data):
        """
        Parses the permission overwrites from the given data and returns them.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items) elements
            A list of permission overwrites' data.
        
        Returns
        -------
        overwrites : `list` of ``PermissionOverwrite``
        """
        overwrites = []
        try:
            overwrites_data = data['permission_overwrites']
        except KeyError:
            return overwrites
        
        if not overwrites_data:
            return overwrites
        
        default_role = self.guild.default_role
        
        for overwrite_data in overwrites_data:
            overwrite = PermissionOverwrite(overwrite_data)
            if overwrite.target_role is default_role:
                overwrites.insert(0, overwrite)
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
        guild = self.guild
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
        
        if (not 1 < len(name) < 38):
            return default
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if user.discriminator == discriminator and user.name == name_:
                        return user
        
        if len(name) > 32:
            return default

        for user in users:
            if user.name == name:
                return user
        
        guild = self.guild
        for user in users:
            nick = user.guild_profiles[guild]
            if nick is None:
                continue
            
            if nick == name:
                return user
        
        return default
    
    def get_user_like(self, name, default=None):
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
        guild = self.guild
        if guild is None:
            return default
        
        if not 1 < len(name) < 38:
            return default
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in guild.users.values():
                    if not self.permissions_for(user).can_view_channel:
                        continue
                    
                    if user.discriminator == discriminator and user.name == name_:
                        return user
        
        if len(name) > 32:
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        
        for user in guild.users.values():
            if not self.permissions_for(user).can_view_channel:
                continue
            
            if pattern.match(user.name) is not None:
                return user
            
            nick = user.guild_profiles[guild].nick
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
        guild = self.guild
        if guild is None:
            return result
        
        if (not 1 < len(name) < 38):
            return result
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if not self.permissions_for(user).can_view_channel:
                        continue
                    
                    if user.discriminator == discriminator and user.name == name_:
                        result.append(user)
                        break
        
        if len(name) > 32:
            return result
        
        pattern = re.compile(re.escape(name), re.I)
        
        for user in guild.users.values():
            if not self.permissions_for(user).can_view_channel:
                continue
            
            if pattern.match(user.name) is not None:
                result.append(user)
                continue
            
            nick = user.guild_profiles[guild].nick
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
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The LOOP_TIME time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    nsfw : `bool`
        Whether the channel is marked as non safe for work.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages` or `manage_channel` permissions are unaffected
    topic : `None` or `str`
        The channel's topic.
    type : `int`
        The channel's Discord side type. Can be any of `.INTERCHANGE`.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(0, 5,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    DEFAULT_TYPE : `int` = `0`
        The preferred channel type, if there is no channel type included.
    """
    __slots__ = ('nsfw', 'slowmode', 'topic', 'type',) # guild text channel related
    
    ORDER_GROUP = 0
    INTERCHANGE = (0, 5,)
    DEFAULT_TYPE = 0
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a guild text channel from the channel data received from Discord. If the channel already exists and if
        it is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (guild is not None), f'`guild` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
            self._messageable_init()
        else:
            if self.clients:
                return self
        
        self._cache_perm = None
        self.name = data['name']
        self.type = data['type']
        
        self._init_category_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        self.topic = data.get('topic')
        self.nsfw = data.get('nsfw', False)
        self.slowmode = int(data.get('rate_limit_per_user', 0))
        
        return self
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelText`` from partial data. Called by ``create_partial_channel`` when a new partial channel is
        needed to be created.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : ``Guild`` or `None`
            The channel's guild if applicable.
        
        Returns
        -------
        channel : ``ChannelText``
        """
        self = object.__new__(cls)
        self._messageable_init()
        
        self._cache_perm = None
        self.category = None
        self.guild = partial_guild
        self.id = channel_id
        
        self.nsfw = False
        self.overwrites = []
        self.position = 0
        self.slowmode = 0
        self.topic = None
        
        if data is None:
            name = ''
            type_ = cls.DEFAULT_TYPE
        else:
            name = data.get('name', '')
            type_ = data['type']
        
        self.name = name
        self.type = type_
        
        return self
    
    @property
    def display_name(self):
        """
        A text channel's display name is it's name with lowercase characters.
        
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
        self._cache_perm = None
        self._set_category_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.type = data['type']
        self.topic = data.get('topic')
        self.nsfw = data.get('nsfw', False)
        self.slowmode = int(data.get('rate_limit_per_user', 0))
    
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
        | overwrites    | `list` of ``PermissionOverwrite``              |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        | slowmode      | `int`                             |
        +---------------+-----------------------------------+
        | topic         | `None` or `str`                   |
        +---------------+-----------------------------------+
        | type          | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        type_ = data['type']
        if self.type != type_:
            old_attributes['type'] = self.type
            self.type = type_
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        topic = data.get('topic')
        if self.topic != topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        nsfw = data.get('nsfw', False)
        if self.nsfw != nsfw:
            old_attributes['nsfw'] = self.nsfw
            self.nsfw = nsfw
        
        slowmode = int(data.get('rate_limit_per_user', 0))
        if self.slowmode != slowmode:
            old_attributes['slowmode'] = self.slowmode
            self.slowmode = slowmode
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        self._update_category_and_position(data, old_attributes)
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]

        if self is guild.system_channel:
            guild.system_channel = None
        if self is guild.widget_channel:
            guild.widget_channel = None
        if self is guild.rules_channel:
            guild.rules_channel = None
        if self is guild.public_updates_channel:
            guild.public_updates_channel = None
        
        self.category = None
        
        self.overwrites.clear()
        self._cache_perm = None
        
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
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_VOICE_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # text channels don't have voice permissions
        result &= PERMISSION_VOICE_DENY
        
        if self.type and (not Permission.can_manage_messages(result)):
            result = result&PERMISSION_TEXT_DENY
            return Permission(result)
        
        if not Permission.can_send_messages(result):
            result = result&PERMISSION_TEXT_DENY
        
        return Permission(result)
    
    def permissions_for_roles(self, *roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # text channels don't have voice permissions
        result &= PERMISSION_VOICE_DENY
        
        if self.type and (not Permission.can_manage_messages(result)):
            result = result&PERMISSION_TEXT_DENY
            return Permission(result)
        
        if not Permission.can_send_messages(result):
            result = result&PERMISSION_TEXT_DENY
        
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
        topic : `None` or `str`, Optional
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
            
            try:
                value = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(value, 'name', 2, 100)
                processable.append(('name', name))
            
            try:
                topic = kwargs.pop('topic')
            except KeyError:
                pass
            else:
                if (topic is not None):
                    topic = preconvert_str(topic, 'topic', 0, 1024)
                    if topic:
                        processable.append(('topic', topic))
            
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
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)

            channel.id = channel_id

            channel._cache_perm = None
            channel.category = None
            channel.guild = None
            channel.overwrites = []
            channel.position = 0
            channel.name = ''
            channel.type = cls.DEFAULT_TYPE
            channel.nsfw = False
            channel.slowmode = 0
            channel.topic = None
            
            channel._messageable_init()
            
            CHANNELS[channel_id] = channel
            
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
        Unique identifier of the channel.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The LOOP_TIME time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
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
    __slots__ = ('users',) # private related
    
    INTERCHANGE = (1,)
    type = 1
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a private channel from the channel data received from Discord. If the channel already exists and if it
        is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (client is not None), f'`client` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
            self._messageable_init()
            self.users = users = []
        else:
            users = self.users
            if len(users) == 2:
                return self
            
            users.clear()
        
        for user_data in data['recipients']:
            user = User(user_data)
            users.append(user)
        
        if client not in users:
            users.append(client)
        
        users.sort()
        
        user = users[0]
        if user is client:
            user = users[1]
        
        client.private_channels[user.id] = self
        return self
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelPrivate`` from partial data. Called by ``create_partial_channel`` when a new partial channel
        is needed to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : `None`
            compatibility parameter with the other channel types.
        
        Returns
        -------
        channel : ``ChannelPrivate``
        """
        self = object.__new__(cls)
        self._messageable_init()
        self.id = channel_id
        # exactly what partial private channel data contains?
        self.users = []
        
        return self
    
    @classmethod
    def _create_dataless(cls, channel_id):
        """
        Creates a private channel from a channel id. Might be called by parsers, when a message's channel is not found
        and it is a private channel.
        
        Parameters
        ----------
        channel_id : `int`
            The channel's respective id.
        
        Returns
        -------
        channel : ``ChannelPrivate``
            The created channel.
        """
        self = object.__new__(cls)
        self._messageable_init()
        self.id = channel_id
        self.users = []
        CHANNELS[channel_id] = self
        
        return self
    
    def _finish_dataless(self, client, user):
        """
        Finishes the initialization of the channel after a ``.create_dataless`` call.
        
        Parameters
        ----------
        client : ``Client``
            The client recipient of the channel.
        user : ``User`` or ``Client``
            The other recipient of the channel.
        """
        users = self.users
        users.append(client)
        users.append(user)
        users.sort()
        
        client.private_channels[user.id] = self
    
    def __str__(self):
        """Returns the channel's name."""
        users = self.users
        if users:
            name = f'Direct Message {users[0].full_name} with {users[1].full_name}'
        else:
            name = f'Direct Message (partial)'
        return name
    
    def _delete(self, client):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        
        Parameters
        ----------
        client : ``Client``
            The client, who's private channel was deleted.
        """
        users = self.users
        if client is users[0]:
            user = users[1]
        else:
            user = users[0]
        
        del client.private_channels[user.id]
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        This method is just for compatibility with the other channel types.
        
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
        
        This method is just for compatibility with the other channel types, what means it always returns an empty
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
    if DOCS_ENABLED:
        name.__doc__ = (
        """
        Returns the channel's name.
        
        Returns
        -------
        name : `str`
        """)
    
    display_name = property(__str__)
    if DOCS_ENABLED:
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
                return PERMISSION_PRIVATE_BOT
            else:
                return PERMISSION_PRIVATE
            
        return PERMISSION_NONE
    
    cached_permissions_for = permissions_for
    
    @property
    def guild(self):
        """
        Returns the private channel's guild, which is `None` every time.
        
        This property is just for compatibility with the other channel types.
        
        Returns
        -------
        guild : `None`
        """
        return None
    
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
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)
            
            channel.id = channel_id
            
            channel.users = []
            
            channel._messageable_init()
            
            CHANNELS[channel_id] = channel
        
        return channel


class ChannelVoiceBase(ChannelGuildBase):
    """
    Base class for guild voice channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    region : `None` or ``VoiceRegion``
        The voice region of the channel. If set as `None`, defaults to the voice channel's guild's.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `2`
        An order group what defined which guild channel type comes after the other one.
    """
    __slots__ = ('bitrate', 'region', 'user_limit') # Voice related.
    
    ORDER_GROUP = 2
    
    @property
    def voice_users(self):
        """
        Returns a list of the users, who are in the voice channel.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        users = []
        guild = self.guild
        if guild is None:
            return users
        
        for state in guild.voice_states.values():
            if state.channel is self:
                users.append(state.user)
        
        return users

    @property
    def display_name(self):
        """
        A voice channel's display name is same as it's `.name`.
        
        Returns
        -------
        display_name : `str`
        """
        return self.name

class ChannelVoice(ChannelVoiceBase):
    """
    Represents a ``Guild`` voice channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    region : `None` or ``VoiceRegion``
        The voice region of the channel. If set as `None`, defaults to the voice channel's guild's.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    video_quality_mode : ``VideoQualityMode``
        The video quality of the voice channel.
    
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
    __slots__ = ('video_quality_mode',) # Voice channel related
    
    INTERCHANGE = (2,)
    type = 2
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a voice channel from the channel data received from Discord. If the channel already exists and if it is
        partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (guild is not None), f'`guild` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
        else:
            if self.clients:
                return self
        
        # Guild base
        self._cache_perm = None
        self.name = data['name']
        
        self._init_category_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        # Voice base
        region = data.get('rtc_region')
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        # Voice
        self.video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
        
        return self
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelVoice`` from partial data. Called by ``create_partial_channel`` when a new partial channel
        is needed to be created.
        
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
        self = object.__new__(cls)
        
        self._cache_perm = None
        
        self.category = None
        self.guild = partial_guild
        self.id = channel_id
        self.name = data.get('name', '')
        self.overwrites = []
        self.position = 0
        
        self.bitrate = 0
        self.region = None
        self.user_limit = 0
        
        self.video_quality_mode = VideoQualityMode.auto
        
        return self
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.category = None
        
        # safe delete
        if self is guild.afk_channel:
            guild.afk_channel = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        self._cache_perm = None
        self._set_category_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        region = data.get('rtc_region')
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
    
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
        
        +-----------------------+-----------------------------------+
        | Keys                  | Values                            |
        +=======================+===================================+
        | bitrate               | `int`                             |
        +-----------------------+-----------------------------------+
        | category              | ``ChannelCategory`` or ``Guild``  |
        +-----------------------+-----------------------------------+
        | name                  | `str`                             |
        +-----------------------+-----------------------------------+
        | overwrites            | `list` of ``PermissionOverwrite`` |
        +-----------------------+-----------------------------------+
        | position              | `int`                             |
        +-----------------------+-----------------------------------+
        | region                | `None` or ``VoiceRegion``         |
        +-----------------------+-----------------------------------+
        | user_limit            | `int`                             |
        +-----------------------+-----------------------------------+
        | video_quality_mode    | ``VideoQualityMode``              |
        +-----------------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        bitrate = data['bitrate']
        if self.bitrate != bitrate:
            old_attributes['bitrate'] = self.bitrate
            self.bitrate = bitrate
        
        user_limit = data['user_limit']
        if self.user_limit != user_limit:
            old_attributes['user_limit'] = self.user_limit
            self.user_limit = user_limit
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        region = data.get('rtc_region')
        if (region is not None):
            region = VoiceRegion.get(region)
        
        if self.region is not region:
            old_attributes['region'] = self.region
            self.region = region
        
        self._update_category_and_position(data, old_attributes)
        
        video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
        if self.video_quality_mode is not video_quality_mode:
            old_attributes['video_quality_mode'] = self.video_quality_mode
            self.video_quality_mode = video_quality_mode
        
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
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_TEXT_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        #voice channels don't have text permissions
        result &= PERMISSION_TEXT_AND_STAGE_DENY
        
        if not Permission.can_connect(result):
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
    
    def permissions_for_roles(self, *roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_TEXT_AND_STAGE_DENY
        
        if not Permission.can_connect(result):
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
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
        bitrate : `int`, Optional
            The channel's ``.bitrate``.
        user_limit : `int`, Optional
            The channel's ``.user_limit``.
        region : `None`, ``VoiceRegion`` or `str`, Optional
            The channel's voice region.
        video_quality_mode : ``VideoQualityMode``
            The video quality of the voice channel.
        
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
                processable.append(('name', name))
            
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
            
            for key, type_, nullable in (
                    ('region', VoiceRegion, True),
                    ('video_quality_mode', VideoQualityMode, False)
                        ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    if nullable and (value is None):
                        continue
                    
                    value = preconvert_preinstanced_type(value, key, type_)
                    processable.append((key, value))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)
            
            channel.id = channel_id
            
            channel._cache_perm = None
            channel.category = None
            channel.guild = None
            channel.overwrites = []
            channel.position = 0
            channel.name = ''
            
            channel.bitrate = 64000
            channel.user_limit = 0
            channel.region = None
            
            channel.video_quality_mode = VideoQualityMode.auto
            
            CHANNELS[channel_id] = channel
        
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
        Unique identifier of the channel.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The LOOP_TIME time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
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
    owner_id : `int`
        The group channel's owner's id.
    
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
        'name', 'owner_id',) # group channel related
    
    icon = IconSlot('icon', 'icon', URLS.channel_group_icon_url, URLS.channel_group_icon_url_as)
    
    INTERCHANGE = (3,)
    type = 3
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a channel from the channel data received from Discord. If the channel already exists and if it is
        partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (client is not None), f'`client` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
            self._messageable_init()
            self.users = users = []
        else:
            users = self.users
            if len(users) == len(data['recipients']):
                return self
            
            users.clear()
        
        name = data.get('name')
        self.name = '' if name is None else name
        self._set_icon(data)
        self.owner_id = int(data['owner_id'])
        
        for user_data in data['recipients']:
            user = User(user_data)
            users.append(user)
        
        users.sort()
        
        client.group_channels[channel_id] = self
        return self
    
    @property
    def owner(self):
        """
        Returns the group channel's owner.
        
        Returns
        -------
        owner : ``User`` or ``Client``
            Defaults to `ZEROUSER`.
        """
        try:
            owner = USERS[self.owner_id]
        except KeyError:
            owner = ZEROUSER
        return owner
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelGroup`` from partial data. Called by ``create_partial_channel`` when a new partial channel
        is needed to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : `None`
            compatibility parameter with the other channel types.
        
        Returns
        -------
        channel : ``ChannelGroup``
        """
        self = object.__new__(cls)
        self._messageable_init()
        self.id = channel_id
        # even if we get recipients, we will ignore them
        self.users = []
        
        self._set_icon(data)
        
        name = data.get('name',None)
        # should we transfer the recipients to name?
        self.name = '' if name is None else name
        
        self.owner = ZEROUSER
        
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
        name = data.get('name')
        self.name = '' if name is None else name
        
        self._set_icon(data)
        
        users = [User(user) for user in data['recipients']]
        users.sort()
        self.users = users
        
        self.owner_id = int(data['owner_id'])
    
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
        | owner_id      | `int`                                 |
        +---------------+---------------------------------------+
        | users         | `list` of (``User`` or ``Client``)    |
        +---------------+---------------------------------------+
        """
        old_attributes = {}
        
        name = data.get('name')
        if name is None:
            name=''
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        self._update_icon(data, old_attributes)
        
        users = [User(user) for user in data['recipients']]
        users.sort()
        
        if self.users != users:
            old_attributes['users'] = self.users
            self.users = users
        
        owner_id = int(data['owner_id'])
        if self.owner_id != owner_id:
            old_attributes['owner_id'] = self.owner_id
            self.owner_id = owner_id
        
        return old_attributes
    
    def __str__(self):
        """Returns the channel's name."""
        name = self.name
        if name:
            return name
        
        users = self.users
        if users:
            return ', '.join([user.name for user in users])
        
        return 'Unnamed'
    
    display_name = property(__str__)
    if DOCS_ENABLED:
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
        if self.owner_id == user.id:
            return PERMISSION_GROUP_OWNER
        elif user in self.users:
            return PERMISSION_GROUP
        else:
            return PERMISSION_NONE
    
    cached_permissions_for = permissions_for
    
    @property
    def guild(self):
        """
        Returns the group channel's guild what is `None` every time.
        
        This property is just for compatibility with the other channel types.
        
        Returns
        -------
        guild : `None`
        """
        return None
    
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
        owner_id : `int` Optional
            The channel's owner's id.
        
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
                owner_id = kwargs.pop('owner_id')
            except KeyError:
                pass
            else:
                owner_id = preconvert_snowflake(owner_id, 'owner_id')
                processable.append(('owner_id', owner_id))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)
            
            channel.id = channel_id
            
            channel.users = []
            
            channel.name = ''
            channel.icon_hash = 0
            channel.icon_type = ICON_TYPE_NONE
            channel.owner_id = 0
            
            channel._messageable_init()
            
            CHANNELS[channel_id] = channel
            
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
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None` or ``Guild``
        The channel's category. Category channels can not be in an other category, so it is always set to their
        `.guild`. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    
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
    __slots__=() #channel category related
    
    ORDER_GROUP = 4
    INTERCHANGE = (4,)
    type = 4
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a category channel from the channel data received from Discord. If the channel already exists and if it
        is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (guild is not None), f'`guild` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
        else:
            if self.clients:
                return self
        
        self._cache_perm = None
        self.name = data['name']
        
        self._init_category_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        return self
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelCategory`` from partial data. Called by ``create_partial_channel`` when a new partial
        channel is needed to be created.
        
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
        self = object.__new__(cls)
        
        self._cache_perm = None
        self.category = None
        self.guild = partial_guild
        self.id = channel_id
        self.name = data.get('name', '')
        self.overwrites = []
        self.position = 0
        
        return self
    
    @property
    def display_name(self):
        """
        A category channel's display name is it's name with uppercase characters.
        
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
        self._cache_perm = None
        self._set_category_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        
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
        | overwrites    | `list` of ``PermissionOverwrite`` |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}

        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        self._update_category_and_position(data, old_attributes)
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.category = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
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
        channel : ``ChannelCategory``
        
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
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)

            channel.id = channel_id

            channel._cache_perm = None
            channel.category = None
            channel.guild = None
            channel.overwrites = []
            channel.position = 0
            channel.name = ''
            
            CHANNELS[channel_id] = channel
            
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel
    
    @property
    def channel_list(self):
        """
        Returns the channels of the category in a list in their display order.
        
        Returns
        -------
        channels : `list` of ``ChannelGuildBase`` instances
        """
        guild = self.guild
        if guild is None:
            return []
        
        return sorted(channel for channel in guild.channels.values() if channel.category is self)


class ChannelStore(ChannelGuildBase):
    """
    Represents a ``Guild`` store channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
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
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a store channel from the channel data received from Discord. If the channel already exists and if
        it is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (guild is not None), f'`guild` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
        else:
            if self.clients:
                return self
        
        self._cache_perm = None
        self.name = data['name']
        self.nsfw = data.get('nsfw', False)
        
        self._init_category_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        return self
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelStore`` from partial data. Called by ``create_partial_channel`` when a new partial channel
        is needed to be created.
        
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
        self = object.__new__(cls)
        
        self._cache_perm = None
        self.category = None
        self.guild = partial_guild
        self.id = channel_id
        self.name = data.get('name', '')
        self.nsfw = False
        self.overwrites = []
        self.position = 0
        
        return self
        
    @property
    def display_name(self):
        """
        A store channel's display name is it's name with lowercase characters.
        
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
        self._cache_perm = None
        self._set_category_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.nsfw = data.get('nsfw', False)
        
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
        | overwrites    | `list` of ``PermissionOverwrite``              |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        nsfw = data.get('nsfw', False)
        if self.nsfw != nsfw:
            old_attributes['nsfw'] = self.nsfw
            self.nsfw = nsfw
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        self._update_category_and_position(data, old_attributes)
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.category = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
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
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_TEXT_AND_VOICE_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # store channels do not have text and voice related permissions
        result &= PERMISSION_TEXT_AND_VOICE_DENY
        
        return Permission(result)
    
    def permissions_for_roles(self, *roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # store channels do not have text and voice related permissions
        result &= PERMISSION_TEXT_AND_VOICE_DENY
    
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
        channel : ``ChannelStore``
        
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
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)
            
            channel.id = channel_id
            
            channel._cache_perm = None
            channel.category = None
            channel.guild = None
            channel.overwrites = []
            channel.position = 0
            channel.name = ''
            
            channel.nsfw = False
            
            CHANNELS[channel_id] = channel
            
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel


class ChannelThread(ChannelGuildBase):
    """
    Represents a ``Guild`` thread channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(9,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `9`
        The channel's Discord side type.
    """
    __slots__ = () #guild channel thread related
    
    ORDER_GROUP = 0
    INTERCHANGE = (9,)
    type = 9
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a thread channel from the channel data received from Discord. If the channel already exists and if it
        is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (guild is not None), f'`guild` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
        else:
            if self.clients:
                return self
        
        self._cache_perm = None
        self.name = data['name']
        self._init_category_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        return self
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelThread`` from partial data. Called by ``create_partial_channel`` when a new partial channel
        is needed to be created.
        
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
        self = object.__new__(cls)
        
        self._cache_perm = None
        self.category = None
        self.guild = partial_guild
        self.id = channel_id
        self.name = data.get('name', '')
        self.overwrites = []
        self.position = 0
        
        return self
    
    @property
    def display_name(self):
        """
        A thread channel's display name is it's name with lowercase characters.
        
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
        self._cache_perm = None
        self._set_category_and_position(data)
        self.overwrites=self._parse_overwrites(data)
        
        self.name = data['name']
        
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
        | overwrites    | `list` of ``PermissionOverwrite`` |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        self._update_category_and_position(data, old_attributes)
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.category = None
        
        self.overwrites.clear()
        self._cache_perm = None

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
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_TEXT_AND_VOICE_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # thread channels do not have text and voice related permissions?
        # result&=PERMISSION_TEXT_AND_VOICE_DENY
        
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
        
        Returns
        -------
        channel : ``ChannelThread``
        
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
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)
            
            channel.id = channel_id
            
            channel._cache_perm = None
            channel.category = None
            channel.guild  = None
            channel.overwrites = []
            channel.position = 0
            channel.name = ''
            
            CHANNELS[channel_id] = channel
            
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel

class ChannelGuildUndefined(ChannelGuildBase):
    """
    Represents an undefined  ``Guild`` channel. This class is a place-holder for future classes. Expectedly for channel
    type 7 and 8.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    type : `int`
        The channel's type.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    IGNORED_NAMES : `tuple` or `str`
        Attribute names, which will not be set automatically, because they are set by other modules.
    DEFAULT_TYPE : `int` = `7`
        The default type, what ``ChannelGuildUndefined`` represents.
    REPRESENTED_TYPES : `tuple` = (`7`, `8`,)
        The types value what ``ChannelGuildUndefined`` might represent.
    
    Notes
    -----
    This type supports dynamic attributes.
    """
    __slots__ = ('type', '__dict__', )
    INTERCHANGE = ()
    ORDER_GROUP = 0
    
    IGNORED_NAMES = ('type', 'name', 'position', 'parent_id', 'permission_overwrites', )
    DEFAULT_TYPE = 7
    REPRESENTED_TYPES = (7, 8,)
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates an undefined guild channel from the channel data received from Discord. If the channel already exists
        and if it is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (guild is not None), f'`guild` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
        else:
            if self.clients:
                return self
        
        self._cache_perm = None
        self.name = data['name']
        self.type = data['type']
        
        self._init_category_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            setattr(self, key, data[key])
        
        return self
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelThread`` from partial data. Called by ``create_partial_channel`` when a new partial channel
        is needed to be created.
        
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
        self = object.__new__(cls)
        
        self._cache_perm = None
        self.category = None
        self.guild = partial_guild
        self.id = channel_id
        self.name = data.get('name', '')
        self.overwrites = []
        self.position = 0
        self.type = data['type']
        
        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            setattr(self, key, data[key])
        
        return self
    
    @property
    def display_name(self):
        """
        Returns the channel's display name.
        
        Returns
        -------
        display_name : `str`
        """
        return self.name
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        self._cache_perm = None
        self._set_category_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        
        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            setattr(self, key, data[key])
    
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
            All item in the returned dict is optional, and it might contain extra items.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------------------+
        | Keys          | Values                            |
        +===============+===================================+
        | category      | ``ChannelCategory`` or ``Guild``  |
        +---------------+-----------------------------------+
        | name          | `str`                             |
        +---------------+-----------------------------------+
        | overwrites    | `list` of ``PermissionOverwrite``              |
        +---------------+-----------------------------------+
        | position      | `int`                             |
        +---------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        self._update_category_and_position(data, old_attributes)

        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            old_value = getattr(self, key, _spaceholder)
            new_value = data[key]
            
            if old_value is _spaceholder:
                setattr(self, key, new_value)
            else:
                if old_value != new_value:
                    setattr(self, key, new_value)
                    old_attributes[key] = old_value
        
        return old_attributes
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.category = None
        
        self.overwrites.clear()
        self._cache_perm = None

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
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_TEXT_AND_VOICE_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
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
        type : `int`, Optional
            The channel's ``.type``.
        
        Returns
        -------
        channel : ``ChannelThread``
        
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
                type_ = kwargs.pop('type')
            except KeyError:
                pass
            else:
                type_ = preconvert_int(type_, 'type', 0, 255)
                processable.append(('type', type_))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)
            
            channel.id = channel_id
            
            channel._cache_perm = None
            channel.category = None
            channel.guild = None
            channel.overwrites = []
            channel.position = 0
            channel.name = ''
            channel.type = cls.DEFAULT_TYPE
            
            CHANNELS[channel_id] = channel
            
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel


class ChannelStage(ChannelVoiceBase):
    """
    Represents a Discord stage channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    category : `None`, ``ChannelCategory`` or ``Guild``
        The channel's category. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    region : `None` or ``VoiceRegion``
        The voice region of the channel. If set as `None`, defaults to the voice channel's guild's.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    topic : `None` or `str`
        The channel's topic.
    
    Class Attributes
    ----------------
    INTERCHANGE : `tuple` of `int` = `(13,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `2`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `13`
        The channel's Discord side type.
    """
    __slots__ = ('topic',) # Stage channel related
    
    INTERCHANGE = (13,)
    type = 13
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a stage channel from the channel data received from Discord. If the channel already exists and if it is
        partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        assert (guild is not None), f'`guild` argument cannot be `None` when calling `{cls.__name__}.__new__`.'
        
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
        else:
            if self.clients:
                return self
        
        # Guild base
        self._cache_perm = None
        self.name = data['name']
        
        self._init_category_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        # Voice base
        region = data.get('rtc_region')
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        self.topic = data.get('topic')
        
        return self
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a ``ChannelVoice`` from partial data. Called by ``create_partial_channel`` when a new partial channel
        is needed to be created.
        
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
        self = object.__new__(cls)
        
        self._cache_perm = None
        
        self.category = None
        self.guild = partial_guild
        self.id = channel_id
        self.name = data.get('name', '')
        self.overwrites = []
        self.position = 0
        
        self.bitrate = 0
        self.region = None
        self.user_limit = 0
        
        self.topic = None
        
        return self
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.category = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        self._cache_perm = None
        self._set_category_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        region = data.get('rtc_region')
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.topic = None
    
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
        
        +-----------------------+-----------------------------------+
        | Keys                  | Values                            |
        +=======================+===================================+
        | bitrate               | `int`                             |
        +-----------------------+-----------------------------------+
        | category              | ``ChannelCategory`` or ``Guild``  |
        +-----------------------+-----------------------------------+
        | name                  | `str`                             |
        +-----------------------+-----------------------------------+
        | overwrites            | `list` of ``PermissionOverwrite`` |
        +-----------------------+-----------------------------------+
        | position              | `int`                             |
        +-----------------------+-----------------------------------+
        | region                | `None` or ``VoiceRegion``         |
        +-----------------------+-----------------------------------+
        | user_limit            | `int`                             |
        +-----------------------+-----------------------------------+
        | topic                 | `None` or `int`                   |
        +-----------------------+-----------------------------------+
        """
        self._cache_perm = None
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        bitrate = data['bitrate']
        if self.bitrate != bitrate:
            old_attributes['bitrate'] = self.bitrate
            self.bitrate = bitrate
        
        user_limit = data['user_limit']
        if self.user_limit != user_limit:
            old_attributes['user_limit'] = self.user_limit
            self.user_limit = user_limit
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        region = data.get('rtc_region')
        if (region is not None):
            region = VoiceRegion.get(region)
        
        if self.region is not region:
            old_attributes['region'] = self.region
            self.region = region
        
        self._update_category_and_position(data, old_attributes)
        
        topic = data.get('topic')
        if self.topic != topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
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
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_TEXT_DENY
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_TEXT_DENY
        
        if not Permission.can_connect(result):
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
        return Permission(result)
    
    def permissions_for_roles(self, *roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        result = self._permissions_for_roles(roles)
        if not result.can_view_channel:
            return PERMISSION_NONE
        
        # voice channels don't have text permissions
        result &= PERMISSION_TEXT_DENY
        
        if not Permission.can_connect(result):
            result &= PERMISSION_VOICE_DENY_CONNECTION
        
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
        bitrate : `int`, Optional
            The channel's ``.bitrate``.
        user_limit : `int`, Optional
            The channel's ``.user_limit``.
        region : `None`, ``VoiceRegion`` or `str`, Optional
            The channel's voice region.
        topic : `None` or `str`, Optional
            The channel's topic.
        
        Returns
        -------
        channel : ``ChannelStage``
        
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
            
            try:
                region = kwargs.pop('region')
            except KeyError:
                pass
            else:
                if (region is not None):
                    region = preconvert_preinstanced_type(region, 'type_', VoiceRegion)
                    processable.append(('region', region))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
            
            try:
                topic = kwargs.pop('topic')
            except KeyError:
                pass
            else:
                if (topic is not None):
                    topic = preconvert_str(topic, 'topic', 0, 120)
                    if topic:
                        processable.append((topic, topic))
        
        else:
            processable = None
        
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            channel = object.__new__(cls)
            
            channel.id = channel_id
            
            channel._cache_perm = None
            channel.category = None
            channel.guild = None
            channel.overwrites = []
            channel.position = 0
            channel.name = ''
            
            channel.bitrate = 64000
            channel.user_limit = 0
            channel.region = None
            
            CHANNELS[channel_id] = channel
        
        else:
            if not channel.partial:
                return channel
        
        if (processable is not None):
            for item in processable:
                setattr(channel, *item)
        
        return channel
    
    @property
    def audience(self):
        """
        Returns the audience in the stage channel.
        
        Returns
        -------
        users : `list` of (``User``, ``Client``)
        """
        users = []
        guild = self.guild
        if guild is None:
            return users
        
        for state in guild.voice_states.values():
            if (state.channel is self) and state.is_speaker:
                users.append(state.user)
        
        return users

    @property
    def speakers(self):
        """
        Returns the speakers in the stage channel.
        
        Returns
        -------
        users : `list` of (``User``, ``Client``)
        """
        users = []
        guild = self.guild
        if guild is None:
            return users
        
        for state in guild.voice_states.values():
            if (state.channel is self) and (not state.is_speaker):
                users.append(state.user)
        
        return users
    
    @property
    def moderators(self):
        """
        Returns the moderators in the stage channel.
        
        Returns
        -------
        users : `list` of (``User``, ``Client``)
        """
        users = []
        guild = self.guild
        if guild is None:
            return users
        
        for state in guild.voice_states.values():
            if (state.channel is self):
                user = state.user
                if self.permissions_for(user) >= PERMISSION_STAGE_MODERATOR:
                    users.append(user)
        
        return users



CHANNEL_TYPES = {
     0: ChannelText,
     1: ChannelPrivate,
     2: ChannelVoice,
     3: ChannelGroup,
     4: ChannelCategory,
     5: ChannelText,
     6: ChannelStore,
     9: ChannelThread,
    13: ChannelStage,
        }

def cr_pg_channel_object(name, type_, *, overwrites=None, topic=None, nsfw=None, slowmode=None, bitrate=None,
        user_limit=None, region=None, video_quality_mode=None, category=None, guild=None):
    """
    Creates a json serializable object representing a ``GuildChannelBase`` instance.
    
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
    region : `None`, ``VoiceRegion`` or `str`, Optional
        The channel's voice region.
    video_quality_mode : `None`, ``VideoQualityMode`` or `int`, Optional
        The channel's video quality mode.
    category : `None`, ``ChannelCategory``, ``Guild`` or `int`, Optional
        The channel's category. If the category is under a guild, leave it empty.
    guild : `None` or ``Guild``, Optional
        Reference guild used for validation purposes. Defaults to `None`.
    
    Returns
    -------
    channel_data : `dict` of (`str`, `Any`) items
    
    Raises
    ------
    TypeError
        - If `type_` was not passed as `int` or as ``ChannelGuildBase`` instance.
        - If `category` was not given as `None`, ``ChannelCategory``, ``Guild`` or `int` instance.
        - If `region` was not given either as `None`, `str` nor ``VoiceRegion`` instance.
        - If `video_quality_mode` was not given neither as `None`, `VideoQualityMode`` nor as `int` instance.
    AssertionError
        - if `guild` is given, but not as `None` nor ``Guild`` instance.
        - If `type_` was given as `int`, and is less than `0`.
        - If `type_` was given as `int` and exceeds the defined channel type limit.
        - If `name` was not given as `str` instance.
        - If `name`'s length is under `2` or over `100`.
        - If `overwrites` was not given as `None`, neither as `list` of `dict`-s.
        - If `topic` was not given as `str` instance.
        - If `topic`'s length is over `1024` or `120` depending on channel type.
        - If `topic` was given, but the respective channel type is not ``ChannelText`` nor ``ChannelStage``.
        - If `nsfw` was given meanwhile the respective channel type is not ``ChannelText`` or ``ChannelStore``.
        - If `nsfw` was not given as `bool`.
        - If `slowmode` was given, but the respective channel type is not ``ChannelText``.
        - If `slowmode` was not given as `int` instance.
        - If `slowmode` was given, but it's value is less than `0` or greater than `21600`.
        - If `bitrate` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `bitrate` was not given as `int` instance.
        - If `bitrate`'s value is out of the expected range.
        - If `user_limit` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `user_limit` was not given as `int` instance.
        - If `user_limit`' was given, but is out of the expected [0:99] range.
        - If `category` was given, but the respective channel type cannot be put under other categories.
        - If `region` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `video_quality_mode` was given, but the respective channel is not ``ChannelVoice`` instance.
    """
    if __debug__:
        if (guild is not None) and (not isinstance(guild, Guild)):
            raise AssertionError('`guild` is given, but not as `None` nor `Guild` instance, got '
                f'{guild.__class__.__name__}.')
    
    if isinstance(type_, int):
        if __debug__:
            if type_ < 0:
                raise AssertionError(f'`type_` cannot be negative value, got `{type_!r}`.')
            if type_ not in CHANNEL_TYPES:
                raise AssertionError(f'`type_` is not in an of the existing channel types: {set(CHANNEL_TYPES)!r}, '
                    f'got `{type_}`.')
        
        channel_type = CHANNEL_TYPES.get(type_, ChannelGuildUndefined)
        channel_type_value = type_
    
    elif issubclass(type_, ChannelBase):
        channel_type = type_
        channel_type_value = type_.INTERCHANGE[0]
    else:
        raise TypeError(f'The given `type_` is not, neither refers to a channel a type, got {type_!r}.')
    
    if not issubclass(channel_type, ChannelGuildBase):
        raise TypeError(f'`type_` not refers to a `{ChannelGuildBase.__name__}` instance, but to '
            f'{channel_type.__name__}. Got {type_!r}.')
    
    
    if __debug__:
        if not isinstance(name, str):
            raise AssertionError(f'`name` can be given as `str` instance, got {name.__class__.__name__}.')
        
        name_ln = len(name)
        
        if name_ln < 2 or name_ln > 100:
            raise AssertionError(f'`name` length can be in range [2:100], got {name_ln}; {name!r}.')
    
    
    if overwrites is None:
        overwrites = []
    else:
        if __debug__:
            if not isinstance(overwrites, list):
                raise AssertionError(f'`overwrites` can be given as `None` or `list` of `cr_p_overwrite_object` '
                     f'returns, got {overwrites.__class__.__name__}')
            
            for index, element in enumerate(overwrites):
                if not isinstance(element, dict):
                    raise AssertionError(f'`overwrites`\'s element {index} should be `dict` instance, but got '
                        f'{element.__class__.__name__}')
    
    
    channel_data = {
        'name'                  : name,
        'type'                  : channel_type_value,
        'permission_overwrites' : overwrites,
            }
    
    
    if (topic is not None):
        if __debug__:
            if not issubclass(channel_type, (ChannelText, ChannelStage)):
                raise AssertionError(f'`topic` is a valid parameter only for `{ChannelText.__name__}` and for '
                    f'{ChannelStage.__name__} instances, got {channel_type.__name__}.')
            
            if not isinstance(topic, str):
                raise AssertionError(f'`topic` can be given as `str` instance, got {topic.__class__.__name__}.')
            
            if issubclass(channel_type, ChannelText):
                topic_length_limit = 1024
            else:
                topic_length_limit = 120
            
            if topic_length > topic_length_limit:
                raise AssertionError(f'`topic` length can be in range [0:{topic_length_limit}], got {topic_length}; '
                    f'{topic!r}.')
        
        channel_data['topic'] = topic
    
    
    if (nsfw is not None):
        if __debug__:
            if not issubclass(channel_type, (ChannelText, ChannelStore)):
                raise AssertionError(f'`nsfw` is a valid parameter only for `{ChannelText.__name__}` and '
                    f'`{ChannelStore.__name__}` instances, but got {channel_type.__name__}.')
            
            if not isinstance(nsfw, bool):
                raise AssertionError(f'`nsfw` can be given as `bool` instance, got {nsfw.__class__.__name__}.')
        
        channel_data['nsfw'] = nsfw
    
    
    if (slowmode is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelText):
                raise AssertionError(f'`slowmode` is a valid parameter only for `{ChannelText.__name__}` instances, '
                    f'but got {channel_type.__name__}.')
            
            if not isinstance(slowmode, int):
                raise AssertionError('`slowmode` can be given as `int` instance, got '
                    f'{slowmode.__class__.__name__}.')
            
            if slowmode < 0 or slowmode > 21600:
                raise AssertionError(f'`slowmode` can be in range [0:21600], got: {slowmode!r}.')
        
        channel_data['rate_limit_per_user'] = slowmode
    
    

    if (bitrate is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelVoiceBase):
                raise AssertionError(f'`bitrate` is a valid parameter only for `{ChannelVoiceBase.__name__}` instances, '
                    f'but got {channel_type.__name__}.')
                
            if not isinstance(bitrate, int):
                raise AssertionError('`bitrate` can be given as `int` instance, got '
                    f'{bitrate.__class__.__name__}.')
            
            # Get max bitrate
            if guild is None:
                bitrate_limit = 384000
            else:
                bitrate_limit = guild.bitrate_limit
            
            if bitrate < 8000 or bitrate > bitrate_limit:
                raise AssertionError(f'`bitrate` is out of the expected [8000:{bitrate_limit}] range, got {bitrate!r}.')
        
        channel_data['bitrate'] = bitrate
    
    
    if (user_limit is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelVoiceBase):
                raise AssertionError(f'`user_limit` is a valid parameter only for `{ChannelVoiceBase.__name__}` '
                    f'instances, but got {channel_type.__name__}.')
            
            if user_limit < 0 or user_limit > 99:
                raise AssertionError('`user_limit`\'s value is out of the expected [0:99] range, got '
                    f'{user_limit!r}.')
        
        channel_data['user_limit'] = user_limit
    
    
    if (region is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelVoiceBase):
                raise AssertionError(f'`region` is a valid parameter only for `{ChannelVoiceBase.__name__}` '
                    f'instances, but got {channel_type.__name__}.')
        
        if isinstance(region, VoiceRegion):
            region_value = region.value
        elif isinstance(region, str):
            region_value = region
        else:
            raise TypeError(f'`region` can be given either as `None`, `str` or as `{VoiceRegion.__name__}` instance, '
                f'{region.__class__.__name__}.')
        
        data['rtc_region'] = region_value
    
    
    if (video_quality_mode is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelVoice):
                raise AssertionError(f'`video_quality_mode` is a valid parameter only for `{ChannelVoice.__name__}` '
                    f'instances, but got {channel_type.__name__}.')
        
        if isinstance(video_quality_mode, VideoQualityMode):
            video_quality_mode_value = video_quality_mode.value
        elif isinstance(video_quality_mode, int):
            video_quality_mode_value = video_quality_mode
        else:
            raise TypeError(f'`video_quality_mode` can be given either as `None`, `str` or as '
                f'`{VideoQualityMode.__name__}` instance, {video_quality_mode.__class__.__name__}.')
        
        data['video_quality_mode'] = video_quality_mode_value
    
    
    if category is None:
        category_id = 0
    elif isinstance(category, ChannelCategory):
        category_id = category.id
    elif isinstance(category, Guild):
        category_id = 0
    else:
        category_id = maybe_snowflake(category)
        if category_id is None:
            raise TypeError(f'`category` can be given as `{ChannelCategory.__name__}`, `{Guild.__name__}` or `int` '
                f'instance, got {category.__class__.__name__}.')
    
    if category_id:
        if __debug__:
            if issubclass(channel_type, ChannelCategory):
                raise AssertionError(f'`category` was given, but the respective channel type is '
                    f'{channel_type.__name__}, which cannot be put under other categories.')
        
        channel_data['parent_id'] = category_id
    
    return channel_data


# Scopes

module_webhook.ChannelText = ChannelText
module_message.ChannelBase = ChannelBase
module_message.ChannelTextBase = ChannelTextBase
module_message.ChannelGuildBase = ChannelGuildBase
module_message.ChannelText = ChannelText
module_message.ChannelPrivate = ChannelPrivate
module_message.ChannelGroup = ChannelGroup
module_rate_limit.ChannelBase = ChannelBase
module_rate_limit.ChannelGuildBase = ChannelGuildBase
URLS.ChannelGuildBase = ChannelGuildBase

del module_message
del module_webhook
del module_rate_limit
