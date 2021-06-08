__all__ = ('ChannelBase', 'ChannelCategory', 'ChannelGroup', 'ChannelGuildBase', 'ChannelGuildMainBase',
    'ChannelGuildUndefined', 'ChannelPrivate', 'ChannelStage', 'ChannelStore', 'ChannelText', 'ChannelTextBase',
    'ChannelThread', 'ChannelVoice', 'MessageIterator', 'cr_pg_channel_object')

import re, warnings
from collections import deque
try:
    from _weakref import WeakSet
except ImportError:
    from weakref import WeakSet

from ..backend.utils import copy_docs
from ..backend.event_loop import LOOP_TIME
from ..backend.export import export, include

from .bases import DiscordEntity, IconSlot, ICON_TYPE_NONE, maybe_snowflake
from .core import CHANNELS, MESSAGES
from .permission import Permission, PermissionOverwrite
from .permission.permission import PERMISSION_NONE, PERMISSION_ALL, PERMISSION_PRIVATE, PERMISSION_PRIVATE_BOT, \
    PERMISSION_GROUP, PERMISSION_GROUP_OWNER, PERMISSION_TEXT_DENY, PERMISSION_VOICE_DENY, PERMISSION_STAGE_MODERATOR, \
    PERMISSION_VOICE_DENY_CONNECTION, PERMISSION_TEXT_AND_VOICE_DENY, PERMISSION_TEXT_AND_STAGE_DENY
from .message import Message
from .user import User, ZEROUSER, create_partial_user_from_id, thread_user_create
from .core import GC_CYCLER
from .webhook import Webhook, WebhookRepr
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_int, preconvert_bool, \
    preconvert_preinstanced_type
from .utils import DATETIME_FORMAT_CODE, parse_time
from .exceptions import DiscordException, ERROR_CODES
from .preinstanced import VoiceRegion, VideoQualityMode
from .limits import CHANNEL_THREAD_AUTO_ARCHIVE_AFTER_VALUES

from . import urls as module_urls

Client = include('Client')
Guild = include('Guild')

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

def create_partial_channel_from_data(data, partial_guild=None):
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


@export
def create_partial_channel_from_id(channel_id, channel_type, partial_guild=None):
    """
    Creates a new partial channel from the given identifier.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier.
    channel_type : `int`
        The channel's type identifier.
    partial_guild : `None` or ``Guild``, Optional
        A partial guild for the created channel.
    """
    try:
        return CHANNELS[channel_id]
    except KeyError:
        pass
    
    cls = CHANNEL_TYPES.get(channel_type, ChannelGuildUndefined)
    
    channel = cls._create_empty(channel_id, channel_type, partial_guild)
    CHANNELS[channel_id] = channel
    
    return channel


@export
class ChannelBase(DiscordEntity, immortal=True):
    """
    Base class for Discord channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `0`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    
    Notes
    -----
    Channels support weakreferencing.
    """
    DEFAULT_TYPE = 0
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
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase`` or `None`
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
        Searches a user, who's name or nick starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase`` or `default`
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
        Searches the users, who's name or nick starts with the given string.
        
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
        The users who can see this channel.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``)
        """
        return []
    
    def iter_users(self):
        """
        Iterates over the users who can see the channel.
        
        This method is a generator.
        
        Yields
        ------
        user : ``Client`` or ``User``
        """
        yield from self.users
    
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
    
    # for sorting channels
    def __gt__(self, other):
        """Returns whether this channel's id is greater than the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id > other.id
        
    
    def __ge__(self, other):
        """Returns whether this channel's id is greater or equal than the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id >= other.id
        
    
    def __eq__(self, other):
        """Returns whether this channel's id is equal to the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id == other.id
        
    
    def __ne__(self,other):
        """Returns whether this channel's id is not equal to the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id != other.id
        
    
    def __le__(self, other):
        """Returns whether this channel's id is less or equal than the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id <= other.id
        
    
    def __lt__(self, other):
        """Returns whether this channel's id is less than the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id < other.id
        
    
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
            The user, who's permissions will be returned.
        
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
    
    
    @property
    def guild(self):
        """
        Returns the channel's guild. At the case of private channels this is always `None`.
        
        Returns
        -------
        guild : `None`
        """
        return None
    
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        pass

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
        """
        return {}
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        pass

    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a channel from partial data. Called by ``create_partial_channel_from_data`` when a new
        partial channel is needed to be created.
        
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
        channel : ``ChannelBase``
        """
        try:
            channel_type = data['type']
        except KeyError:
            channel_type = cls.DEFAULT_TYPE
        
        self = cls._create_empty(channel_id, channel_type, partial_guild)
        
        return self
    
    @classmethod
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        """
        Creates a partial channel from the given parameters.
        
        Parameters
        ----------
        channel_id : `int`
            The channel's identifier.
        channel_type : `int`
            The channel's type identifier.
        partial_guild : `None` or ``Guild``
            A partial guild for the created channel.
        
        Returns
        -------
        channel : ``ChannelBase`` instance
            The created partial channel.
        """
        self = object.__new__(cls)
        self.id = channel_id
        return self


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
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
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


@export
class ChannelGuildBase(ChannelBase):
    """
    Base class for guild channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `0`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    """
    __slots__ = ('parent', 'guild', 'name', )
    
    ORDER_GROUP = 0
    
    @copy_docs(ChannelBase.__str__)
    def __str__(self):
        return self.name
    
    @property
    @copy_docs(ChannelBase.users)
    def users(self):
        return list(self.iter_users())
    
    
    @copy_docs(ChannelBase.iter_users)
    def iter_users(self):
        guild = self.guild
        if (guild is not None):
            for user in guild.users.values():
                if self.permissions_for(user).can_view_channel:
                    yield user
    
    
    @property
    @copy_docs(ChannelBase.clients)
    def clients(self):
        guild = self.guild
        if guild is None:
            return []
        
        return guild.clients
    
    @copy_docs(ChannelBase.get_user)
    def get_user(self, name, default=None):
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
    
    @copy_docs(ChannelBase.get_user_like)
    def get_user_like(self, name, default=None):
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
    
    @copy_docs(ChannelBase.get_users_like)
    def get_users_like(self, name):
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
    
    @classmethod
    @copy_docs(ChannelBase._from_partial_data)
    def _from_partial_data(cls, data, channel_id, partial_guild):
        self = super(ChannelGuildBase, cls)._from_partial_data(data, channel_id, partial_guild)
        
        try:
            name = data['name']
        except KeyError:
            pass
        else:
            self.name = name
        
        return self
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelGuildBase, cls)._create_empty(channel_id, channel_type, partial_guild)
        self.parent = None
        self.guild = partial_guild
        self.name = ''
        return self


@export
class ChannelGuildMainBase(ChannelGuildBase):
    """
    Base class for main guild channels not including thread channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
    guild : `None` or ``Guild``
        The channel's guild. If the channel is deleted, set to `None`.
    name : `str`
        The channel's name.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    overwrites : `list` of ``PermissionOverwrite`` objects
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `0`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    """
    __slots__ = ('_cache_perm', 'overwrites', 'position', )
    
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
    
    def _init_parent_and_position(self, data, guild):
        """
        Initializes the `.parent` and the `.position` of the channel. If a channel is under the ``Guild``,
        and not in a parent (parent channels are all like these), then their `.parent` is the ``Guild`` itself.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        guild : ``Guild``
            The guild of the channel.
        """
        self.guild = guild
        guild.channels[self.id] = self
        
        parent_id = data.get('parent_id', None)
        if (parent_id is None):
            parent = None
        else:
            parent = guild.channels[int(parent_id)]
        
        self.parent = parent
        
        self.position = data.get('position', 0)
    
    
    def _set_parent_and_position(self, data):
        """
        Similar to the ``._init_parent_and_position`` method, but this method applies the changes too, so moves the channel
        between categories and moves the channel inside of the parent too, to keep the order.
        
        Called from `._update_no_return` when updating a guild channel.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord
        """
        guild = self.guild
        if guild is None:
            return
        
        new_parent_id = data.get('parent_id', None)
        if new_parent_id is None:
            new_parent = None
        else:
            new_parent = guild.channels[int(new_parent_id)]
        
        position = data.get('position', 0)
        
        parent = self.parent
        if parent is new_parent:
            if self.position != position:
                self.position = position
        
        else:
            self.position = position
            self.parent = new_parent
    
    
    def _update_parent_and_position(self, data, old_attributes):
        """
        Acts same as ``._set_parent_and_position``, but it sets the modified attributes' previous value to
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
        
        new_parent_id = data.get('parent_id', None)
        if new_parent_id is None:
            new_parent = None
        else:
            new_parent = guild.channels[int(new_parent_id)]
        
        position = data.get('position', 0)
        
        parent = self.parent
        if parent is new_parent:
            if self.position != position:
                old_attributes['position'] = self.position
                self.position = position
        else:
            old_attributes['parent'] = parent
            old_attributes['position'] = self.position
            
            self.position = position
            self.parent = parent
    
    
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
        
        default_role = guild.roles.get(guild.id, None)
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
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        guild = self.guild
        if guild is None:
            return PERMISSION_NONE
        
        if user.id == guild.owner_id:
            return PERMISSION_ALL
        
        result = self._permissions_for(user)
        if not result.can_view_channel:
            result = PERMISSION_NONE
        
        return result
    
    @copy_docs(ChannelBase.cached_permissions_for)
    def cached_permissions_for(self, user):
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
        
        default_role = guild.roles.get(guild.id, None)
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
    
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
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
    
    @property
    def category(self):
        """
        Deprecated, please use ``.parent`` instead. Will be removed in 2021 july.
        """
        warnings.warn(
            f'`{self.__class__.__name__}.category` is deprecated, and will be removed in 2021 july. '
            f'Please use `{self.__class__.__name__}.parent` instead.',
            FutureWarning)
        
        return self.parent
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelGuildMainBase, cls)._create_empty(channel_id, channel_type, partial_guild)
        self._cache_perm = None
        self.overwrites = []
        self.position = 0
        return self


@export
class ChannelText(ChannelGuildMainBase, ChannelTextBase):
    """
    Represents a ``Guild`` text channel or an announcements channel. So the type of the channel is interchangeable
    between them. The channel's Discord side channel type is 0 (text) or 5 (announcements).
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
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
        `manage_messages` or `manage_channel` permissions are unaffected.
    topic : `None` or `str`
        The channel's topic.
    type : `int`
        The channel's Discord side type. Can be any of `.INTERCHANGE`.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `0`
        The preferred channel type, if there is no channel type included.
    INTERCHANGE : `tuple` of `int` = `(0, 5,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    """
    __slots__ = ('nsfw', 'slowmode', 'topic', 'type',) # guild text channel related
    
    ORDER_GROUP = 0
    INTERCHANGE = (0, 5,)
    
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
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        self.topic = data.get('topic', None)
        self.nsfw = data.get('nsfw', False)
        self.slowmode = int(data.get('rate_limit_per_user', 0))
        
        return self
    
    @copy_docs(ChannelBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        try:
            type_name = CHANNEL_TEXT_NAMES[self.type]
        except KeyError:
            type_name = repr(self.type)
        
        if (type_name is not None):
            repr_parts.append(' (')
            repr_parts.append(repr_parts)
            repr_parts.append(')')
            
        repr_parts.append(' id=')
        repr_parts.append(repr(self.id))
        repr_parts.append(', name=')
        repr_parts.append(repr(self.__str__()))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelText, cls)._create_empty(channel_id, channel_type, partial_guild)
        self._messageable_init()
        
        self.nsfw = False
        self.slowmode = 0
        self.topic = None
        self.type = channel_type
        
        return self
    
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name.lower()
    
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.type = data['type']
        self.topic = data.get('topic', None)
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
        | parent        | ``ChannelCategory``               |
        +---------------+-----------------------------------+
        | name          | `str`                             |
        +---------------+-----------------------------------+
        | nsfw          | `bool`                            |
        +---------------+-----------------------------------+
        | overwrites    | `list` of ``PermissionOverwrite`` |
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
        
        topic = data.get('topic', None)
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
        
        self._update_parent_and_position(data, old_attributes)
        
        return old_attributes
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        
        try:
            del guild.channels[self.id]
        except KeyError:
            pass
        
        if self is guild.system_channel:
            guild.system_channel = None
        if self is guild.widget_channel:
            guild.widget_channel = None
        if self is guild.rules_channel:
            guild.rules_channel = None
        if self is guild.public_updates_channel:
            guild.public_updates_channel = None
        
        self.parent = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
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
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
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
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        topic : `None` or `str`, Optional (Keyword only)
            The channel's ``.topic``.
        slowmode : `int`, Optional (Keyword only)
            The channel's ``.slowmode``.
        type : `int`, Optional (Keyword only)
            The channel's ``.type``.
        nsfw : `int`, Optional (Keyword only)
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
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.DEFAULT_TYPE, None)
            CHANNELS[channel_id] = self
            
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self


@export
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
    DEFAULT_TYPE : `int` = `1`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `(1,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    type : `int` = `1`
        The channel's Discord side type.
    """
    __slots__ = ('users',) # private related
    
    DEFAULT_TYPE = 1
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
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelPrivate, cls)._create_empty(channel_id, channel_type, partial_guild)
        self._messageable_init()
        self.users = []
        
        return self
    
    
    @classmethod
    def _create_dataless(cls, channel_id):
        """
        Creates a private channel from a channel id. Might be called by events, when a message's channel is not found
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
    
    @copy_docs(ChannelBase.__str__)
    def __str__(self):
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
    
    
    name = property(__str__)
    copy_docs(ChannelBase.name)(name)
    
    display_name = property(__str__)
    copy_docs(ChannelBase.display_name)(display_name)
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        if user in self.users:
            if user.is_bot:
                return PERMISSION_PRIVATE_BOT
            else:
                return PERMISSION_PRIVATE
            
        return PERMISSION_NONE
    
    
    cached_permissions_for = permissions_for
    
    
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
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.type, None)
            CHANNELS[channel_id] = self
        
        return self


@export
class ChannelVoiceBase(ChannelGuildMainBase):
    """
    Base class for guild voice channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
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
    DEFAULT_TYPE : `int` = `2`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `2`
        An order group what defined which guild channel type comes after the other one.
    """
    __slots__ = ('bitrate', 'region', 'user_limit') # Voice related.
    
    DEFAULT_TYPE = 2
    ORDER_GROUP = 2
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelVoiceBase, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.bitrate = 0
        self.region = None
        self.user_limit = 0
        
        return self
    
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
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name


@export
class ChannelVoice(ChannelVoiceBase):
    """
    Represents a ``Guild`` voice channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
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
    DEFAULT_TYPE : `int` = `2`
        The default type, what the channel represents.
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
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        # Voice base
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        # Voice
        self.video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
        
        return self
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelVoice, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.video_quality_mode = VideoQualityMode.auto
        
        return self
    
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.parent = None
        
        # safe delete
        if self is guild.afk_channel:
            guild.afk_channel = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        region = data.get('rtc_region', None)
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
        | parent                | ``ChannelCategory``               |
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
        
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        
        if self.region is not region:
            old_attributes['region'] = self.region
            self.region = region
        
        self._update_parent_and_position(data, old_attributes)
        
        video_quality_mode = VideoQualityMode.get(data.get('video_quality_mode', 1))
        if self.video_quality_mode is not video_quality_mode:
            old_attributes['video_quality_mode'] = self.video_quality_mode
            self.video_quality_mode = video_quality_mode
        
        return old_attributes
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
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
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
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
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        bitrate : `int`, Optional (Keyword only)
            The channel's ``.bitrate``.
        user_limit : `int`, Optional (Keyword only)
            The channel's ``.user_limit``.
        region : `None`, ``VoiceRegion`` or `str`, Optional (Keyword only)
            The channel's voice region.
        video_quality_mode : ``VideoQualityMode``, Optional (Keyword only)
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
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.DEFAULT_TYPE, None)
            CHANNELS[channel_id] = self
        
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self


@export
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
    DEFAULT_TYPE : `int` = `3`
        The default type, what the channel represents.
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
    
    icon = IconSlot('icon', 'icon', module_urls.channel_group_icon_url, module_urls.channel_group_icon_url_as)
    
    DEFAULT_TYPE = 3
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
        
        name = data.get('name', None)
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
        owner : ``ClientUserBase``
            Defaults to `ZEROUSER`.
        """
        owner_id = self.owner_id
        if owner_id:
            owner = create_partial_user_from_id(owner_id)
        else:
            owner = ZEROUSER
        return owner
    
    @classmethod
    @copy_docs(ChannelBase._from_partial_data)
    def _from_partial_data(cls, data, channel_id, partial_guild):
        self = super(ChannelGroup, cls)._from_partial_data(data, channel_id, partial_guild)
        
        name = data.get('name', None)
        if (name is not None):
            self.name = name
        
        return self
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelGroup, cls)._create_empty(channel_id, channel_type, partial_guild)
        self._messageable_init()
        
        self.users = []
        
        self.name = None
        self.owner_id = 0
        
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        
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
    
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        name = data.get('name', None)
        self.name = '' if name is None else name
        
        self._set_icon(data)
        
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
        """
        old_attributes = {}
        
        name = data.get('name', None)
        if name is None:
            name = ''
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        self._update_icon(data, old_attributes)
        
        owner_id = int(data['owner_id'])
        if self.owner_id != owner_id:
            old_attributes['owner_id'] = self.owner_id
            self.owner_id = owner_id
        
        return old_attributes
    
    @copy_docs(ChannelBase.__str__)
    def __str__(self):
        name = self.name
        if name:
            return name
        
        users = self.users
        if users:
            return ', '.join([user.name for user in users])
        
        return 'Unnamed'
    
    display_name = property(__str__)
    copy_docs(ChannelBase.display_name)(display_name)
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        if self.owner_id == user.id:
            return PERMISSION_GROUP_OWNER
        elif user in self.users:
            return PERMISSION_GROUP
        else:
            return PERMISSION_NONE
    
    cached_permissions_for = permissions_for
    
    
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
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        icon : `int`, Optional (Keyword only)
            The channel's ``.icon``.
        owner_id : `int`, Optional (Keyword only)
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
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.type, None)
            CHANNELS[channel_id] = self
            
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self


@export
class ChannelCategory(ChannelGuildMainBase):
    """
    Represents a ``Guild`` channel category.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent : `None` or ``Guild``
        The channel's parent. Category channels can not be in an other parent, so it is always set to their
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
    DEFAULT_TYPE : `int` = `4`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `(4,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `4`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `4`
        The channel's Discord side type.
    """
    __slots__ = () # channel category related
    
    DEFAULT_TYPE = 4
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
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        return self
    
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name.upper()
    
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
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
        
        self._update_parent_and_position(data, old_attributes)
        
        return old_attributes
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.parent = None
        
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
        name : `str`, Optional (Keyword only)
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
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.type, None)
            CHANNELS[channel_id] = self
            
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    @property
    def channel_list(self):
        """
        Returns the channels of the category in a list in their display order.
        
        Returns
        -------
        channels : `list` of ``ChannelGuildMainBase`` instances
        """
        guild = self.guild
        if guild is None:
            return []
        
        return sorted(channel for channel in guild.channels.values() if channel.parent is self)


@export
class ChannelStore(ChannelGuildMainBase):
    """
    Represents a ``Guild`` store channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
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
    DEFAULT_TYPE : `int` = `6`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `(6,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `6`
        The channel's Discord side type.
    """
    __slots__ = ('nsfw',) #guild channel store related
    
    DEFAULT_TYPE = 6
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
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        return self
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelStore, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.nsfw = False
        
        return self
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name.lower()
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
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
        | parent        | ``ChannelCategory``               |
        +---------------+-----------------------------------+
        | name          | `str`                             |
        +---------------+-----------------------------------+
        | nsfw          | `bool`                            |
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
        
        nsfw = data.get('nsfw', False)
        if self.nsfw != nsfw:
            old_attributes['nsfw'] = self.nsfw
            self.nsfw = nsfw
        
        overwrites = self._parse_overwrites(data)
        if self.overwrites != overwrites:
            old_attributes['overwrites'] = self.overwrites
            self.overwrites = overwrites
        
        self._update_parent_and_position(data, old_attributes)
        
        return old_attributes
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.parent = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
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
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
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
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        nsfw : `int`, Optional (Keyword only)
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
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.type, None)
            CHANNELS[channel_id] = self
            
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self



@export
class ChannelThread(ChannelGuildBase, ChannelTextBase):
    """
    Represents a ``Guild`` thread channel
    
    Attributes
    ----------
    id : `int`
        The unique identifier of the channel.
    parent : `None` or ``ChannelText``
        The text channel from where the thread is created from.
    name : `str`
        The channel's name.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The LOOP_TIME time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    archived : `bool`
        Whether the thread s archived.
    archived_at : `None` or `datetime`
        When the thread's archive status was last changed.
    archiver_id : `int`
        The (un)archiver's identifier number.
    auto_archive_after : `int`
        Duration in minutes to automatically archive the thread after recent activity. Can be one of: `60`, `1440`,
        `4320`, `10080`.
    open : `bool`
        Whether the thread channel is open.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages` or `manage_channel` permissions are unaffected.
    thread_users : `None` or `dict` of (`int`, ``ClientUserBase``) items
        The users inside of the thread if any.
    type : `int` = `12`
        The channel's Discord side type.
    owner_id : `int`
        The channel's creator's identifier. Defaults to `0`.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `12`
        The preferred channel type, if there is no channel type included.
    INTERCHANGE : `tuple` of `int` = `(10, 11, 12,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `9`
        An order group what defined which guild channel type comes after the other one.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    REPRESENTED_TYPES : `tuple` = (`10`, `11`, `12`,)
        The type values which ``ChannelThread`` might represent.
    """
    __slots__ = ('archived', 'archived_at', 'archiver_id', 'auto_archive_after', 'open', 'owner_id', 'slowmode',
        'thread_users', 'type')
    
    DEFAULT_TYPE = 12
    ORDER_GROUP = 9
    INTERCHANGE = ()
    REPRESENTED_TYPES = (10, 11, 12,)
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a guild thread channel from the channel data received from Discord. If the channel already exists and
        if it is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
            self._messageable_init()
            self.thread_users = None
            update = True
        else:
            if self.clients:
                update = False
            else:
                update = True
        
        if update:
            self.type = data['type']
            self._init_parent(data, guild)
            self._update_no_return(data)
        
        if (client is not None):
            try:
                thread_user_data = data['member']
            except KeyError:
                pass
            else:
                thread_user_create(self, client, thread_user_data)
        
        return self
    
    @copy_docs(ChannelBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        try:
            type_name = CHANNEL_THREAD_NAMES[self.type]
        except KeyError:
            type_name = repr(self.type)
        
        if (type_name is not None):
            repr_parts.append(' (')
            repr_parts.append(repr_parts)
            repr_parts.append(')')
            
        repr_parts.append(' id=')
        repr_parts.append(repr(self.id))
        repr_parts.append(', name=')
        repr_parts.append(repr(self.__str__()))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    @property
    def owner(self):
        """
        Returns the thread threads's creator.
        
        Returns
        -------
        owner : ``UserClientBase``
            If user the guild has no owner, returns `ZEROUSER`.
        """
        owner_id = self.owner_id
        if owner_id:
            owner = create_partial_user_from_id(owner_id)
        else:
            owner = ZEROUSER
        
        return owner
    
    @property
    def archiver(self):
        """
        Returns who (un)archived the thread last.
        
        Returns
        -------
        owner : `None` or ``UserClientBase``
            Defaults to `None`.
        """
        archiver_id = self.archiver_id
        if archiver_id:
            archiver = create_partial_user_from_id(archiver_id)
        else:
            archiver = None
        
        return archiver
    
    def is_announcements(self):
        """
        Returns whether the thread channel is bound to an announcements channel.
        
        Returns
        -------
        is_announcements : `bool`
        """
        return self.type == 10
    
    def is_public(self):
        """
        Returns whether the thread channel is public.
        
        Returns
        -------
        is_public : `bool`
        """
        return self.type == 11
    
    def is_private(self):
        """
        Returns whether the thread channel is private.
        
        Returns
        -------
        is_private : `bool`
        """
        return self.type == 12
    
    def _init_parent(self, data, guild):
        """
        Initializes the `.parent` attribute of the channel. If a channel is under the ``Guild``, and not in a parent
        (parent channels are all like these), then their `.parent` is the ``Guild`` itself.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        guild : ``Guild``
            The guild of the channel.
        """
        self.guild = guild
        
        if (guild is not None):
            guild.threads[self.id] = self
        
        parent_id = data.get('parent_id', None)
        if (parent_id is None):
            parent = None
        else:
            parent_id = int(parent_id)
            
            if guild is None:
                parent = CHANNELS.get(parent_id, None)
            else:
                parent = guild.channels.get(parent_id, None)
        
        self.parent = parent
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelThread, cls)._create_empty(channel_id, channel_type, partial_guild)
        self._messageable_init()
        
        self.archived = False
        self.archived_at = None
        self.archiver_id = 0
        self.auto_archive_after = 60
        self.open = False
        self.owner_id = 0
        self.slowmode = 0
        self.type = channel_type
        
        return self
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name.lower()
    
    
    @property
    @copy_docs(ChannelBase.users)
    def users(self):
        thread_users = self.thread_users
        if thread_users is None:
            users = []
        else:
            users = list(thread_users.values())
        
        return users
    
    @copy_docs(ChannelBase.iter_users)
    def iter_users(self):
        thread_users = self.thread_users
        if (thread_users is not None):
            yield from thread_users.values()
    
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self.name = data['name']
        self.slowmode = int(data.get('rate_limit_per_user', 0))
        
        # Move to sub data
        data = data['thread_metadata']
        
        self.archived = data.get('archived', False)
        
        archiver_id = data.get('archiver_id', None)
        if archiver_id is None:
            archiver_id = 0
        else:
            archiver_id = int(archiver_id)
        
        self.archiver_id = archiver_id
        
        self.auto_archive_after = data['auto_archive_after']
        
        archived_at_data = data.get('archive_timestamp', None)
        if archived_at_data is None:
            archived_at = None
        else:
            archived_at = parse_time(archived_at_data)
        self.archived_at = archived_at
        
        self.open = not data.get('locked', True)
    
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
        
        +-----------------------+-----------------------------------+
        | Keys                  | Values                            |
        +=======================+===================================+
        | archived              | `bool`                            |
        +-----------------------+-----------------------------------+
        | archived_at           | `None` or `datetime`              |
        +-----------------------+-----------------------------------+
        | archiver_id           | `int`                             |
        +-----------------------+-----------------------------------+
        | auto_archive_after    | `int`                             |
        +-----------------------+-----------------------------------+
        | name                  | `str`                             |
        +-----------------------+-----------------------------------+
        | open                  | `bool`                            |
        +-----------------------+-----------------------------------+
        | slowmode              | `int`                             |
        +-----------------------+-----------------------------------+
        """
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        slowmode = int(data.get('rate_limit_per_user', 0))
        if self.slowmode != slowmode:
            old_attributes['slowmode'] = self.slowmode
            self.slowmode = slowmode
        
        
        # Move to sub data
        data = data['thread_metadata']
        
        
        archived = data.get('archived', False)
        if (self.archived != archived):
            old_attributes['archived'] = self.archived
            self.archived = archived
        
        
        archiver_id = data.get('archiver_id', None)
        if archiver_id is None:
            archiver_id = 0
        else:
            archiver_id = int(archiver_id)
        if (self.archiver_id != archiver_id):
            old_attributes['archiver_id'] = self.archiver_id
            self.archiver_id = archiver_id
        
        
        auto_archive_after = data['auto_archive_after']
        if (self.auto_archive_after != auto_archive_after):
            old_attributes['auto_archive_after'] = self.auto_archive_after
            self.auto_archive_after = auto_archive_after
        
        
        archived_at_data = data.get('archive_timestamp', None)
        if archived_at_data is None:
            archived_at = None
        else:
            archived_at = parse_time(archived_at_data)
        if (self.archived_at != archived_at):
            old_attributes['archived_at'] = self.archived_at
            self.archived_at = archived_at
        
        open_ = not data.get('locked', True)
        if (self.open != open_):
            old_attributes['open'] = self.open
            self.open = open_
        
        return old_attributes
    
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        parent = self.parent
        if parent is None:
            return
        
        self.parent = None
        
        guild = self.guild
        if (guild is not None):
            self.guild = None
            del guild.threads[self.id]
        
        thread_users = self.thread_users
        if (thread_users is not None):
            self.thread_users = None
            for user in thread_users.values():
                thread_profiles = user.thread_profiles
                if (thread_profiles is not None):
                    try:
                        del thread_profiles[self]
                    except KeyError:
                        pass
                    else:
                        if (not thread_profiles):
                            user.thread_profiles = None
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        parent = self.parent
        if parent is None:
            return PERMISSION_NONE
        
        return parent.permissions_for(user)

    @copy_docs(ChannelBase.cached_permissions_for)
    def cached_permissions_for(self, user):
        parent = self.parent
        if parent is None:
            return PERMISSION_NONE
        
        return parent.cached_permissions_for(user)
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
        parent = self.parent
        if parent is None:
            return PERMISSION_NONE
        
        return parent.permissions_for_roles(*roles)
    
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
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        slowmode : `int`, Optional (Keyword only)
            The channel's ``.slowmode``.
        type : `int`, Optional (Keyword only)
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
                value = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(value, 'name', 2, 100)
                processable.append(('name', name))
            
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
                if (type_ not in cls.REPRESENTED_TYPES):
                    raise ValueError(f'`type` should be one of: {cls.REPRESENTED_TYPES!r}')
                
                processable.append(('type', type_))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.DEFAULT_TYPE, None)
            CHANNELS[channel_id] = self
        
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self


@export
class ChannelGuildUndefined(ChannelGuildMainBase):
    """
    Represents an undefined  ``Guild`` channel. This class is a place-holder for future classes. Expectedly for channel
    type `7` and `8`.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
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
    DEFAULT_TYPE : `int` = `7`
        The default type, what ``ChannelGuildUndefined`` represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `0`
        An order group what defined which guild channel type comes after the other one.
    IGNORED_NAMES : `frozenset` or `str`
        Attribute names, which will not be set automatically, because they are set by other modules.
    REPRESENTED_TYPES : `tuple` = (`7`, `8`,)
        The type values which ``ChannelGuildUndefined`` might represent.
    
    Notes
    -----
    This type supports dynamic attributes.
    """
    __slots__ = ('type', '__dict__', )
    
    DEFAULT_TYPE = 7
    IGNORED_NAMES = frozenset(('type', 'name', 'position', 'parent_id', 'permission_overwrites', ))
    INTERCHANGE = ()
    ORDER_GROUP = 0
    REPRESENTED_TYPES = (7, 8, )
    
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
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            setattr(self, key, data[key])
        
        return self
    
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        self = super(ChannelGuildUndefined, cls)._from_partial_data(data, channel_id, partial_guild)
        
        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            setattr(self, key, data[key])
        
        return self
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelGuildUndefined, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.type = channel_type
        
        return self
    
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name
    
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
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
        | parent        | ``ChannelCategory``               |
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
        
        self._update_parent_and_position(data, old_attributes)

        for key in data.keys():
            if key in self.IGNORED_NAMES:
                continue
            
            old_value = getattr(self, key, ...)
            new_value = data[key]
            
            if old_value is ...:
                setattr(self, key, new_value)
            else:
                if old_value != new_value:
                    setattr(self, key, new_value)
                    old_attributes[key] = old_value
        
        return old_attributes
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        
        try:
            del guild.channels[self.id]
        except KeyError:
            pass
        
        self.parent = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self,user):
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
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        type : `int`, Optional (Keyword only)
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
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.DEFAULT_TYPE, None)
            CHANNELS[channel_id] = self
            
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self


@export
class ChannelStage(ChannelVoiceBase):
    """
    Represents a Discord stage channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _cache_perm : `None` or `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent : `None`, ``ChannelCategory``
        The channel's parent. If the channel is deleted, set to `None`.
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
    DEFAULT_TYPE : `int` = `13`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `(13,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `2`
        An order group what defined which guild channel type comes after the other one.
    type : `int` = `13`
        The channel's Discord side type.
    """
    __slots__ = ('topic',) # Stage channel related
    
    DEFAULT_TYPE = 13
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
        
        self._init_parent_and_position(data, guild)
        self.overwrites = self._parse_overwrites(data)
        
        # Voice base
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
        
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        self.topic = data.get('topic', None)
        
        return self
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelStage, cls)._create_empty(channel_id, channel_type, partial_guild)
        
        self.topic = None
        
        return self
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        guild = self.guild
        if guild is None:
            return
        
        self.guild = None
        del guild.channels[self.id]
        
        self.parent = None
        
        self.overwrites.clear()
        self._cache_perm = None
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self._cache_perm = None
        self._set_parent_and_position(data)
        self.overwrites = self._parse_overwrites(data)
        
        self.name = data['name']
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        region = data.get('rtc_region', None)
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
        | parent                | ``ChannelCategory``  |
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
        
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        
        if self.region is not region:
            old_attributes['region'] = self.region
            self.region = region
        
        self._update_parent_and_position(data, old_attributes)
        
        topic = data.get('topic', None)
        if self.topic != topic:
            old_attributes['topic'] = self.topic
            self.topic = topic
        
        return old_attributes

    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
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
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
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
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        bitrate : `int`, Optional (Keyword only)
            The channel's ``.bitrate``.
        user_limit : `int`, Optional (Keyword only)
            The channel's ``.user_limit``.
        region : `None`, ``VoiceRegion`` or `str`, Optional (Keyword only)
            The channel's voice region.
        topic : `None` or `str`, Optional (Keyword only)
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
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.DEFAULT_TYPE, None)
            CHANNELS[channel_id] = self
        
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    @property
    def audience(self):
        """
        Returns the audience in the stage channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
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
        users : `list` of ``ClientUserBase``
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
        users : `list` of ``ClientUserBase``
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
    10: ChannelThread,
    11: ChannelThread,
    12: ChannelThread,
    13: ChannelStage,
}

export(CHANNEL_TYPES, 'CHANNEL_TYPES')

CHANNEL_TEXT_NAMES = {
     0: None,
     5: 'announcements',
}


CHANNEL_THREAD_NAMES = {
     9: None,
    10: 'announcements',
    11: 'public',
    12: 'private',
}

def cr_pg_channel_object(name, type_, *, overwrites=None, topic=None, nsfw=None, slowmode=None, bitrate=None,
        user_limit=None, region=None, video_quality_mode=None, archived=None, archived_at=None,
        auto_archive_after=None, open_=None, parent=None, category=None, guild=None):
    """
    Creates a json serializable object representing a ``GuildChannelBase`` instance.
    
    Parameters
    ----------
    name : `str`
        The name of the channel. Can be between `2` and `100` characters.
    type_ : `int` or ``ChannelGuildBase`` subclass
        The channel's type.
    overwrites : `list` of ``cr_p_overwrite_object`` returns, Optional (Keyword only)
        A list of permission overwrites of the channel. The list should contain json serializable permission
        overwrites made by the ``cr_p_overwrite_object`` function.
    topic : `str`, Optional (Keyword only)
        The channel's topic.
    nsfw : `bool`, Optional (Keyword only)
        Whether the channel is marked as nsfw.
    slowmode : int`, Optional (Keyword only)
        The channel's slowmode value.
    bitrate : `int`, Optional (Keyword only)
        The channel's bitrate.
    user_limit : `int`, Optional (Keyword only)
        The channel's user limit.
    region : `None`, ``VoiceRegion`` or `str`, Optional (Keyword only)
        The channel's voice region.
    video_quality_mode : `None`, ``VideoQualityMode`` or `int`, Optional (Keyword only)
        The channel's video quality mode.
    archived : `None` or `bool`, Optional (Keyword only)
        Whether the thread channel is archived.
    archived_at : `None` or `datetime`, Optional (Keyword only)
        When the thread's archive status was last changed.
    auto_archive_after : `None` or `int`, Optional (Keyword only)
        Duration in minutes to automatically archive the thread after recent activity. Can be one of: `60`, `1440`,
        `4320`, `10080`.
    open_ : `bool`, Optional (Keyword only)
        Whether the thread channel is open.
    parent : `None`, ``ChannelCategory`` or `int`, Optional (Keyword only)
        The channel's parent. If the parent is under a guild, leave it empty.
    category : `None`, ``ChannelCategory`` or `int`, Optional (Keyword only)
        Deprecated, please use `parent` parameter instead.
    guild : `None` or ``Guild``, Optional (Keyword only)
        Reference guild used for validation purposes. Defaults to `None`.
    
    Returns
    -------
    channel_data : `dict` of (`str`, `Any`) items
    
    Raises
    ------
    TypeError
        - If `type_` was not passed as `int` or as ``ChannelGuildBase`` instance.
        - If `parent` was not given as `None`, ``ChannelCategory`` or `int` instance.
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
        - If `slowmode` was given, but the respective channel type is not ``ChannelText`` or ``ChannelThread``.
        - If `slowmode` was not given as `int` instance.
        - If `slowmode` was given, but it's value is less than `0` or greater than `21600`.
        - If `bitrate` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `bitrate` was not given as `int` instance.
        - If `bitrate`'s value is out of the expected range.
        - If `user_limit` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `user_limit` was not given as `int` instance.
        - If `user_limit`' was given, but is out of the expected [0:99] range.
        - If `parent` was given, but the respective channel type cannot be put under other categories.
        - If `region` was given, but the respective channel type is not ``ChannelVoiceBase``.
        - If `video_quality_mode` was given, but the respective channel is not ``ChannelVoice`` instance.
        - If `archived` was given meanwhile the respective channel type is not ``ChannelThread``.
        - If `archived` was given, but not as `None` or `bool` instance.
        - If `archived_at` was given meanwhile the respective channel type is not ``ChannelThread``.
        - If `archived_at` was given, but not as `None` or `datetime` instance.
        - If `auto_archive_after` was given, but the respective channel's type is not ``ChannelThread``.
        - If `auto_archive_after` was given, but not as `None` or `int` instance.
        - If `auto_archive_after` was ot given neither as `60`, `1440`, `4320`, `10080`.
        - If `open_` was given meanwhile the respective channel type is not ``ChannelThread``.
        - If `open_` was given, but not as `None` or `bool` instance.
    """
    if __debug__:
        if (guild is not None) and (not isinstance(guild, Guild)):
            raise AssertionError('`guild` is given, but not as `None` nor `Guild` instance, got '
                f'{guild.__class__.__name__}.')
    
    if (category is not None):
        warnings.warn(
            f'`cr_pg_channel_object`\'s `category` parameter is deprecated, and will be removed in 2021 july. '
            f'Please use `parent` instead.',
            FutureWarning)
        
        parent = category
    
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
        
        name_length = len(name)
        
        if name_length < 2 or name_length > 100:
            raise AssertionError(f'`name` length can be in range [2:100], got {name_length}; {name!r}.')
    
    channel_data = {
        'name': name,
        'type': channel_type_value,
    }
    
    if not issubclass(channel_type, ChannelThread):
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
    
        channel_data['permission_overwrites'] = overwrites
    
    
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
            
            topic_length = len(topic)
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
            if not issubclass(channel_type, (ChannelText, ChannelThread)):
                raise AssertionError(f'`slowmode` is a valid parameter only for `{ChannelText.__name__}` and for '
                    f'`{ChannelThread.__name__}` instances, but got {channel_type.__name__}.')
            
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
        
        channel_data['rtc_region'] = region_value
    
    
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
        
        channel_data['video_quality_mode'] = video_quality_mode_value
    
    if (archived is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelThread):
                raise AssertionError(f'`archived` is a valid parameter only for `{ChannelThread.__name__}` '
                    f'instances, but got {channel_type.__name__}.')
            
            if not isinsatnce(archived, bool):
                raise AssertionError(f'`archived` can be given as `None` or as `bool` instance, got '
                    f'{archived.__class__.__name__}.')
        
        channel_data['archived'] = archived
    
    
    if (archived_at is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelThread):
                raise AssertionError(f'`archived_at` is a valid parameter only for `{ChannelThread.__name__}` '
                    f'instances, but got {channel_type.__name__}.')
            
            if not isinstance(archived_at, datetime):
                raise AssertionError(f'`archived_at` can be given as `None` or as `datetime` instance, got '
                    f'{archived_at.__class__.__name__}.')
        
        channel_data['archive_timestamp'] =  archived_at.isoformat()
    
    
    if (auto_archive_after is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelThread):
                raise AssertionError(f'`auto_archive_after` is a valid parameter only for `{ChannelThread.__name__}` '
                    f'instances, but got {channel_type.__name__}.')
            
            if not isinstance(auto_archive_after, int):
                raise AssertionError(f'`auto_archive_after` can be given as `None` or as `datetime` instance, got '
                    f'{auto_archive_after.__class__.__name__}.')
            
            if auto_archive_after not in CHANNEL_THREAD_AUTO_ARCHIVE_AFTER_VALUES:
                raise AssertionError(f'`auto_archive_after` can be any of: '
                    f'{CHANNEL_THREAD_AUTO_ARCHIVE_AFTER_VALUES}, got {auto_archive_after}.')
        
        channel_data['auto_archive_after'] = auto_archive_after
    
    
    if (open_ is not None):
        if __debug__:
            if not issubclass(channel_type, ChannelThread):
                raise AssertionError(f'`open_` is a valid parameter only for `{ChannelThread.__name__}` '
                    f'instances, but got {channel_type.__name__}.')
            
            if not isinsatnce(open_, bool):
                raise AssertionError(f'`open_` can be given as `None` or as `bool` instance, got '
                    f'{open_.__class__.__name__}.')
        
        channel_data['locked'] = not open_
    
    
    if parent is None:
        parent_id = 0
    elif isinstance(parent, ChannelCategory):
        parent_id = parent.id
    else:
        parent_id = maybe_snowflake(parent)
        if parent_id is None:
            raise TypeError(f'`parent` can be given as `{ChannelCategory.__name__}`, `{Guild.__name__}` or `int` '
                f'instance, got {parent.__class__.__name__}.')
    
    if parent_id:
        if __debug__:
            if issubclass(channel_type, ChannelCategory):
                raise AssertionError(f'`parent` was given, but the respective channel type is '
                    f'{channel_type.__name__}, which cannot be put under other categories.')
        
        channel_data['parent_id'] = parent_id
    
    return channel_data
