__all__ = ('Channel',)

from collections import deque
from re import I as re_ignore_case, escape as re_escape, search as re_search

from scarletio import LOOP_TIME, export

from ...env import MESSAGE_CACHE_SIZE

from ..bases import DiscordEntity
from ..core import CHANNELS, GUILDS
from ..core import MESSAGES
from ..message import Message
from ..permission import Permission
from ..permission.permission import PERMISSION_STAGE_MODERATOR
from ..preconverters import preconvert_int, preconvert_snowflake
from ..user import ZEROUSER, create_partial_user_from_id
from ..utils import DATETIME_FORMAT_CODE

from . import channel_types as CHANNEL_TYPES
from .message_history import MessageHistory, MessageHistoryCollector, message_relative_index
from .metadata import ChannelMetadataBase, ChannelMetadataGuildMainBase
from .metadata.utils import get_channel_metadata_type
from .utils import get_channel_type_name


@export
class Channel(DiscordEntity, immortal=True):
    """
    Represents a Discord channel.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    _message_history : `None`, ``MessageHistory``
        The channel's message history if any.
    guild_id : `int`
        The channel's guild's identifier. Defaults to `0`.
    metadata : ``ChannelMetadataBase``
        The channel's metadata storing it's type specific information.
    """
    __slots__ = ('_message_history', 'guild_id', 'metadata')
    
    def __new__(cls, data, client, guild_id):
        """
        Creates a new channel from the channel data received from Discord. If the channel already exists and if it
        is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None`, ``Client``
            The client, who received the channel's data, if any.
        guild_id : `int`
            The guild's identifier of the channel.
        
        Raises
        -------
        RuntimeError
            The respective channel type cannot be instanced.
        """
        channel_id = int(data['id'])
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            metadata = get_channel_metadata_type(data['type'])(data)
            
            self = object.__new__(cls)
            self._message_history = None
            self.id = channel_id
            self.guild_id = guild_id
            self.metadata = metadata
            
            metadata._created(self, client)
            CHANNELS[channel_id] = self
            
        else:
            if self.partial:
                self.guild_id = guild_id
                self._message_history = None
                
                metadata = get_channel_metadata_type(data['type'])(data)
                self.metadata = metadata
                metadata._created(self, client)
                
            else:
        
                channel_type = data['type']
                if self.type != channel_type:
                    metadata = get_channel_metadata_type(channel_type)(data)
                    self.metadata = metadata
                    metadata._created(self, client)
        
        return self
    
    
    @classmethod
    def _create_private_data_less(cls, channel_id):
        """
        Creates a private channel from a channel id. Might be called by events, when a message's channel is not found
        and it is a private channel.
        
        Parameters
        ----------
        channel_id : `int`
            The channel's respective id.
        
        Returns
        -------
        self : ``Channel``
        """
        self = cls._create_empty(channel_id, CHANNEL_TYPES.private, 0)
        CHANNELS[channel_id] = self
        return self
    
    
    def _finish_private_data_less(self, client, user):
        """
        Finishes the initialization of the channel after a ``._create_private_data_less`` call.
        
        Parameters
        ----------
        client : ``Client``
            The client recipient of the channel.
        user : ``ClientUserBase``
            The other recipient of the channel.
        """
        metadata = self.metadata
        metadata.users.append(user)
        metadata._created(self, client)
    
    
    
    def __repr__(self):
        """Returns the representation of the channel."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' id=')
        repr_parts.append(repr(self.id))
        
        metadata = self.metadata
        
        repr_parts.append(', name=')
        repr_parts.append(repr(metadata._get_processed_name()))
        
        channel_type = metadata.type
        repr_parts.append(' type=')
        repr_parts.append(repr(get_channel_type_name(channel_type)))
        repr_parts.append('~')
        repr_parts.append(repr(channel_type))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
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
        >>> from hata import Channel, now_as_id
        >>> channel = Channel.precreate(now_as_id(), name='GENERAL')
        >>> channel
        <Channel id=710506058560307200, name='GENERAL'>
        >>> # no code stands for `channel.name`.
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
            return self.metadata._get_processed_name()
        
        if code == 'm':
            return self.mention
        
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
        return self.metadata._get_display_name()
    
    
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
    

    @property
    def clients(self):
        """
        The clients, who can access this channel.
        
        Returns
        -------
        clients : `list` of ``Client``
        """
        return self.metadata._get_clients(self)
    
    
    def get_user(self, name, default=None):
        """
        Tries to find the a user with the given name at the channel. Returns the first matched one.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase``, `default`
        """
        return self.metadata._get_user(self, name, default)
    
    
    def get_user_like(self, name, default=None):
        """
        Searches a user, who's name or nick starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase``, `default`
        """
        return self.metadata._get_user_like(self, name, default)
    
    
    def get_users_like(self, name):
        """
        Searches the users, who's name or nick starts with the given string.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return self.metadata._get_users_like(self, name, default)
    
    
    @property
    def users(self):
        """
        The users who can see this channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return self.metadata._get_users(self)
    
    
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
    
    
    def iter_users(self):
        """
        Iterates over the users who can see the channel.
        
        This method is a generator.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        yield from self.metadata._iter_users(self)
    
    
    @property
    def name(self):
        """
        Returns the channel's name.
        
        Returns
        -------
        name : `str`
        """
        return self.metadata.name
    
    
    def has_name_like(self, name):
        """
        Returns whether the channel's name is like the given string.
        
        Parameters
        ----------
        name : `str`
            The name of the channel.
        
        Returns
        -------
        has_name_like : `bool`
        """
        if name.startswith('#'):
            name = name[1:]
        
        target_name_length = len(name)
        if (target_name_length < 2) or (target_name_length > 100):
            return False
        
        if re_search(re_escape(name), self.name, re_ignore_case) is None:
            return False
        
        return True

    
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        user : ``UserBase``
            The user to calculate it's permissions of.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
            
        
        See Also
        --------
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        return self.metadata._get_permissions_for(self, user)
    
    
    def cached_permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel. If the user's permissions are not cached, calculates
        and stores them first.
        
        Parameters
        ----------
        user : ``UserBase``
            The user to calculate it's permissions of.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
        """
        return self.metadata._get_cached_permissions_for(self, user)
    
    
    def permissions_for_roles(self, *roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
        """
        return self.metadata._get_permissions_for_roles(self, user)
    
    
    @property
    def guild(self):
        """
        Returns the channel's guild. At the case of private channels this is always `None`.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def _update_attributes(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        channel_type = data['type']
        metadata = self.metadata
        if metadata.type == channel_type:
            metadata._update_attributes(data)
        else:
            self.metadata = get_channel_metadata_type(channel_type)(data)
    
    
    def _difference_update_attributes(self, data):
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
            
            Might contain the following items:
            
            +-------------------------------+-----------------------------------------------------------+
            | Keys                          | Values                                                    |
            +===============================+===========================================================+
            | archived                      | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | archived_at                   | `None`, `datetime`                                        |
            +-------------------------------+-----------------------------------------------------------+
            | auto_archive_after            | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | bitrate                       | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | default_auto_archive_after    | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | flags                         | ``ChannelFlag``                                           |
            +-------------------------------+-----------------------------------------------------------+
            | icon                          | ``Icon``                                                  |
            +-------------------------------+-----------------------------------------------------------+
            | invitable                     | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | metadata                      | ``ChannelMetadataBase``                                   |
            +-------------------------------+-----------------------------------------------------------+
            | name                          | `str`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | nsfw                          | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | open                          | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | owner_id                      | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | parent_id                     | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | permission_overwrites         | `None`, `dict` of (`int`, ``PermissionOverwrite``) items  |
            +-------------------------------+-----------------------------------------------------------+
            | position                      | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | region                        | `None`, ``VoiceRegion``                                   |
            +-------------------------------+-----------------------------------------------------------+
            | slowmode                      | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | topic                         | `None`, `str`                                             |
            +-------------------------------+-----------------------------------------------------------+
            | type                          | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | user_limit                    | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | video_quality_mode            | ``VideoQualityMode``                                      |
            +-------------------------------+-----------------------------------------------------------+
        """
        new_channel_type = data['type']
        
        metadata = self.metadata
        old_channel_type = metadata.type
        
        if new_channel_type == old_channel_type:
            old_attributes = metadata._difference_update_attributes(data)
            
        else:
            old_attributes = {
                'type': old_channel_type,
                'metadata': metadata,
            }
            
            self.metadata = get_channel_metadata_type(new_channel_type)(data)
        
        return old_attributes
    
    
    def _delete(self, client):
        """
        Called when the channel is deleted.
        
        Removes the channel's references.
        
        Parameters
        ----------
        client : `None`, ``Client``
            The parent client entity.
        """
        self.metadata._delete(self, client)
    
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, guild_id):
        """
        Creates a channel from partial data. Called by ``create_partial_channel_from_data`` when a new
        partial channel is needed to be created.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        guild_id : `int`
            The channel's guild's identifier if applicable.
        
        Returns
        -------
        channel : ``Channel``
        """
        self = object.__new__(cls)
        self._message_history = None
        self.id = channel_id
        self.guild_id = guild_id
        self.metadata = get_channel_metadata_type(data.get('type', -1))._from_partial_data(data)
        
        CHANNELS.setdefault(channel_id, self)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, channel_id, channel_type, guild_id):
        """
        Creates a partial channel from the given parameters.
        
        Parameters
        ----------
        channel_id : `int`
            The channel's identifier.
        channel_type : `int`
            The channel's type identifier.
        guild_id : `int`
            A partial guild's identifier for the created channel.
        
        Returns
        -------
        channel : ``Channel``
            The created partial channel.
        """
        self = object.__new__(cls)
        self._message_history = None
        self.id = channel_id
        self.guild_id = guild_id
        self.metadata = get_channel_metadata_type(channel_type)._create_empty()
        return self
    
    
    def to_data(self):
        """
        Converts the channel to json serializable representation dictionary.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = self.metadata._to_data()
        
        # id
        data['id'] = str(self.id)
        
        # type
        data['type'] = self.type
        
        # guild_id
        guild_id = self.guild_id
        if guild_id:
            guild_id = str(guild_id)
        else:
            guild_id = None
        
        data['guild_id'] = guild_id
        
        return data
    
    
    @property
    def created_at(self):
        """
        Returns when the channel was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        return self._metadata._get_created_at(self)
    
    
    @property
    def type(self):
        """
        Returns the channel's type.
        
        Returns
        -------
        type : `int`
        """
        return self.metadata.type
    
    
    @property
    def order_group(self):
        """
        Returns the channel's order group.
        
        Returns
        -------
        order_group : `int`
        """
        return self.metadata.order_group
    
    
    # for sorting channels
    def __gt__(self, other):
        """Returns whether this channel's is greater than the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        
        self_metadata = self.metadata
        other_metadata = other.metadata
        
        if (
            isinstance(self_metadata, ChannelMetadataGuildMainBase) and
            isinstance(other_metadata, ChannelMetadataGuildMainBase)
        ):
            self_order_group = self_metadata.order_group
            other_order_group = other_metadata.order_group
            
            if self_order_group > other_order_group:
                return True
            
            if self_order_group != self_order_group:
                return False
                
            self_position = self_metadata.position
            other_position = other_metadata.position
            
            if self_position > other_position:
                return True
            
            if self_position != other_position:
                return False
        
        
        return self.id > other.id
    
    
    def __ge__(self, other):
        """Returns whether this channel's is greater or equal than the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_metadata = self.metadata
        other_metadata = other.metadata
        
        if (
            isinstance(self_metadata, ChannelMetadataGuildMainBase) and
            isinstance(other_metadata, ChannelMetadataGuildMainBase)
        ):
            self_order_group = self_metadata.order_group
            other_order_group = other_metadata.order_group
            
            if self_order_group > other_order_group:
                return True
            
            if self_order_group != self_order_group:
                return False
                
            self_position = self_metadata.position
            other_position = other_metadata.position
            
            if self_position > other_position:
                return True
            
            if self_position != other_position:
                return False
        
        
        return self.id >= other.id
        
    
    def __eq__(self, other):
        """Returns whether this channel's is equal to the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.id == other.id
        
    
    def __ne__(self,other):
        """Returns whether this channel's is not equal to the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.id != other.id
        
    
    def __le__(self, other):
        """Returns whether this channel's is less or equal than the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_metadata = self.metadata
        other_metadata = other.metadata
        
        if (
            isinstance(self_metadata, ChannelMetadataGuildMainBase) and
            isinstance(other_metadata, ChannelMetadataGuildMainBase)
        ):
            self_order_group = self_metadata.order_group
            other_order_group = other_metadata.order_group
            
            if self_order_group < other_order_group:
                return True
            
            if self_order_group != self_order_group:
                return False
            
            self_position = self_metadata.position
            other_position = other_metadata.position
            
            if self_position < other_position:
                return True
            
            if self_position != other_position:
                return False
        
        
        return self.id <= other.id
        
    
    def __lt__(self, other):
        """Returns whether this channel's is less than the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_metadata = self.metadata
        other_metadata = other.metadata
        
        if (
            isinstance(self_metadata, ChannelMetadataGuildMainBase) and
            isinstance(other_metadata, ChannelMetadataGuildMainBase)
        ):
            self_order_group = self_metadata.order_group
            other_order_group = other_metadata.order_group
            
            if self_order_group < other_order_group:
                return True
            
            if self_order_group != self_order_group:
                return False
                
            self_position = self_metadata.position
            other_position = other_metadata.position
            
            if self_position < other_position:
                return True
            
            if self_position != other_position:
                return False
        
        
        return self.id < other.id
    
    
    @property
    def parent_id(self):
        """
        Returns the channel's parent's identifier.
        
        If the channel has no parent, or if not applicable for the specific channel type returns `0`.
        
        Returns
        -------
        parent_id : `int`
        """
        return self.metadata.parent_id
    
        
    @property
    def parent(self):
        """
        Returns the channel's parent.
        
        If the channel has no parent, or if not applicable for the specific channel type returns `None`.
        
        Returns
        -------
        parent : `None`, ``Channel``
        """
        parent_id = self.metadata.parent_id
        if parent_id:
            return CHANNELS.get(parent_id, None)
    
    
    @property
    def permission_overwrites(self):
        """
        Returns the channel's permission overwrites.
        
        If the channel has no permission overwrites returns `None`.
        
        Returns
        -------
        permission_overwrites : `None`, `dict` of (`int`, ``PermissionOverwrite``) items
        """
        return self.metadata.permission_overwrites
    
    
    @property
    def position(self):
        """
        Returns the channel's position.
        
        If the channel has no position, returns `0`.
        
        Returns
        -------
        position : `int`
        """
        return self.metadata.position
    
    
    @property
    def nsfw(self):
        """
        Returns whether the channel is not safe for work.
        
        Defaults to `False`.
        
        Returns
        -------
        nsfw : `bool`
        """
        return self.metadata.nsfw
    
    
    @property
    def slowmode(self):
        """
        Returns the slowmode of the channel.
        
        If the channel has no slowmode, returns `0`.
        
        Returns
        -------
        slowmode : `int`
        """
        return self.metadata.slowmode
    
    
    @property
    def topic(self):
        """
        Returns the channel's topic.
        
        If the channel has no topic, returns `None`.
        
        Returns
        -------
        topic : `None`, `str`
        """
        return self.metadata.topic
    
    
    @property
    def bitrate(self):
        """
        Returns the bitrate (in bits) of the voice channel.
        
        If the channel has no bitrate, returns `0`.
        
        Returns
        -------
        bitrate : `int`
        """
        return self.metadata.bitrate
    
    
    @property
    def region(self):
        """
        Returns the voice region of the channel.
        
        If the channel has no voice region, returns `None`.
        
        Returns
        -------
        region : `None`, ``VoiceRegion``
        """
        return self.metadata.region
    
    
    @property
    def user_limit(self):
        """
        Returns the maximal amount of users, who can join the voice channel
        
        If the channel has not user limit, returns `0`.
        
        Returns
        -------
        user_limit : `int`
        """
        return self.metadata.user_limit
    
    
    @property
    def video_quality_mode(self):
        """
        Returns the video quality of the voice channel.
        
        If the channel has no video quality mode, returns `VideoQualityMode.none`.
        
        Returns
        -------
        video_quality_mode : ``VideoQualityMode``
        """
        return self.metadata.video_quality_mode
        
    
    @property
    def icon(self):
        """
        Returns the channel's icon.
        
        Returns
        -------
        icon : ``Icon``
        """
        return self.metadata.icon
    
    
    @property
    def archived(self):
        """
        Returns whether the thread is archived.
        
        If the channel is not a thread on,e returns `False`.
        
        Returns
        -------
        archived : `bool`
        """
        return self.metadata.archived
    
    
    @property
    def archived_at(self):
        """
        Returns when the thread was archived.
        
        Returns `None` if the the channel is nto a thread one or if it is not archived.
        
        Returns
        -------
        archived_at : `None`, `datetime`
        """
        return self.metadata.archived_at
    
    
    @property
    def auto_archive_after(self):
        """
        Returns the duration in seconds to automatically archive the thread after recent activity. Can be one of:
        `3600`, `86400`, `259200`, `604800`.
        
        Returns `3600` if the channel is not a thread one.
        
        Returns
        -------
        auto_archive_after : `None`, `datetime`
        """
        return self.metadata.auto_archive_after
    
    
    @property
    def invitable(self):
        """
        Whether non-moderators can invite other non-moderators to the threads. Only applicable for private threads.
        
        Returns `True` by default.
        
        Returns
        -------
        invitable : `bool`
        """
        return self.metadata.invitable
    
    
    @property
    def open(self):
        """
        Returns whether the thread channel is open.
        
        If the channel is not a thread one, will return `True`.
        
        Returns
        -------
        open : `bool`
        """
        return self.metadata.open
    
    
    @property
    def flags(self):
        """
        Returns the channel's flags.
        
        Returns empty channel flags by default.
        
        Returns
        -------
        flags : ``ChannelFlag``
        """
        return self.metadata.flags
    
    
    @property
    def thread_users(self):
        """
        Returns the users inside of the thread if any.
        
        If the channel has no users, or if it is not a thread channel, will return `None`.
        
        Returns
        -------
        thread_users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        """
        return self.metadata.thread_users
    
    
    @property
    def channel_list(self):
        """
        Returns the channels of the category in a list in their display order.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        channels = []
        
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                channel_id = self.id
                
                for channel in guild.channels.values():
                    if channel.parent_id == channel_id:
                        channels.append(channel)
                
                channels.sort()
        
        return channels
    
    
    @property
    def voice_users(self):
        """
        Returns a list of the users who are in the voice channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        users = []
        
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                channel_id = self.id
                
                for voice_state in guild.voice_states.values():
                    if voice_state.channel_id == channel_id:
                        users.append(voice_state.user)
        
        return users
    
    

    @property
    def audience(self):
        """
        Returns the audience in the stage channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        users = []
        
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                channel_id = self.id
                
                for voice_states in guild.voice_states.values():
                    if (voice_states.channel_id == channel_id) and voice_states.is_speaker:
                        users.append(voice_states.user)
        
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
        
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                channel_id = self.id
                
                for voice_states in guild.voice_states.values():
                    if (voice_states.channel_id == channel_id) and (not voice_states.is_speaker):
                        users.append(voice_states.user)
        
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
        
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                channel_id = self.id
                
                for voice_states in guild.voice_states.values():
                    if (voice_states.channel_id == channel_id):
                        user = voice_states.user
                        if self.permissions_for(user) >= PERMISSION_STAGE_MODERATOR:
                            users.append(user)
        
        return users
    
    
    @classmethod
    def precreate(cls, channel_id, *, channel_type=None, **keyword_parameters):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precreated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int`, `str`
            The channel's id.
        channel_type : `None`, `int`, Optional = `None`
            The channel's type.
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        auto_archive_after: `int`, Optional (Keyword only)
            The channel's ``.auto_archive_after``.
        
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the channel was created.
        
        bitrate : `int`, Optional (Keyword only)
            The channel's ``.bitrate``.
        
        default_auto_archive_after : `int`, Optional (Keyword only)
            The channel's ``.default_auto_archive_after``.
        
        flags : `int`, ``ChannelFlag``, Optional (Keyword only)
            The channel's ``.flags``.
        
        icon : `None`, ``Icon``, `str`, Optional (Keyword only)
            The channel's icon.
            
            > Mutually exclusive with `icon_type` and `icon_hash` parameters.
        
        icon_type : ``IconType``, Optional (Keyword only)
            The channel's icon's type.
            
            > Mutually exclusive with the `icon` parameter.
        
        icon_hash : `int`, Optional (Keyword only)
            The channel's icon's hash.
            
            > Mutually exclusive with the `icon` parameter.
        
        invitable : `bool`, Optional (Keyword only)
            The channel's `..invitable``.
        
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        
        nsfw : `int`, Optional (Keyword only)
            The channel's ``.nsfw``.
        
        open : `bool`, Optional (Keyword only)
            The channel's ``.open``.
        
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's voice region.
        
        slowmode : `int`, Optional (Keyword only)
            The channel's ``.slowmode``.
        
        topic : `None`, `str`, Optional (Keyword only)
            The channel's ``.topic``.
        
        user_limit : `int`, Optional (Keyword only)
            The channel's ``.user_limit``.
        
        video_quality_mode : ``VideoQualityMode``, Optional (Keyword only)
            The video quality of the voice channel.
        
        Returns
        -------
        channel : ``Channel``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if channel_type is None:
            metadata_type = ChannelMetadataBase
        else:
            channel_type = preconvert_int(channel_type, 'channel_type', 0, 256)
            metadata_type = get_channel_metadata_type(channel_type)
        
        metadata = metadata_type._precreate(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(f'Unused or unsettable attributes: {keyword_parameters!r}.')
        
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, -1, 0)
            CHANNELS[channel_id] = self
        else:
            if not self.partial:
                return self
        
        self.metadata = metadata
        return self
    
    
    # ---- Messaging ----
    
    @property
    def message_history_reached_end(self):
        message_history = self._message_history
        if message_history is None:
            message_history_reached_end = False
        else:
            message_history_reached_end = message_history.message_history_reached_end
        
        return message_history_reached_end
    
    @message_history_reached_end.setter
    def message_history_reached_end(self, message_history_reached_end):
        message_history = self._message_history
        if message_history is None:
            message_history = MessageHistory(MESSAGE_CACHE_SIZE)
            self._message_history = message_history
        
        message_history.message_history_reached_end = message_history_reached_end
    
    
    @property
    def _message_history_collector(self):
        message_history = self._message_history
        if message_history is None:
            message_history_collector = None
        else:
            message_history_collector = message_history._message_history_collector
        
        return message_history_collector
    
    @_message_history_collector.setter
    def _message_history_collector(self, message_history_collector):
        message_history = self._message_history
        if message_history is None:
            message_history = MessageHistory(MESSAGE_CACHE_SIZE)
            self._message_history = message_history
        
        message_history._message_history_collector = message_history_collector
    
    
    @property
    def _message_keep_limit(self):
        message_history = self._message_history
        if message_history is None:
            message_keep_limit = MESSAGE_CACHE_SIZE
        else:
            message_keep_limit = message_history._message_keep_limit
        
        return message_keep_limit
    
    @_message_keep_limit.setter
    def _message_keep_limit(self, message_keep_limit):
        message_history = self._message_history
        if message_history is None:
            message_history = MessageHistory(MESSAGE_CACHE_SIZE)
            self._message_history = message_history
        
        message_history._message_keep_limit = message_keep_limit
    
    
    @property
    def messages(self):
        message_history = self._message_history
        if message_history is None:
            messages = None
        else:
            messages = message_history.messages
        
        return messages
    
    @messages.setter
    def messages(self, messages):
        message_history = self._message_history
        if message_history is None:
            message_history = MessageHistory(MESSAGE_CACHE_SIZE)
            self._message_history = message_history
        
        message_history.messages = messages
    
    
    @property
    def message_keep_limit(self):
        """
        A property for getting or setting how much message the channel can store before removing the last.
        
        Returns and accepts an `int`.
        """
        message_history = self._message_history
        if (message_history is None):
            message_keep_limit = MESSAGE_CACHE_SIZE
        else:
            message_keep_limit = message_history._message_keep_limit
        
        return message_keep_limit
    
    @message_keep_limit.setter
    def message_keep_limit(self, message_keep_limit):
        if message_keep_limit <= 0:
            self._message_history = None
        
        else:
            message_history = self._message_history
            if (message_history is None):
                self._message_history = MessageHistory(message_keep_limit)
            else:
                message_history._set_message_keep_limit(message_keep_limit)
    
    
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
        messages : `deque`, `None`
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
                    maxlen = limit,
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
        message : `None`, ``Message``
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
    
    # ---- Utility methods ----
    
    def is_in_group_messageable(self):
        """
        Returns whether the channel is messageable.
        
        Returns
        -------
        is_in_group_messageable : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_MESSAGEABLE
    
    
    def is_in_group_guild_messageable(self):
        """
        Returns whether the channel is a guild and messageable one.
        
        Returns
        -------
        is_in_group_guild_messageable : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_GUILD_MESSAGEABLE
    
    
    def is_in_group_guild_main_text(self):
        """
        Returns whether the channel a guild text like channel.
        
        > Excludes connectable and thread channels.
        
        Returns
        -------
        is_in_group_guild_main_text : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_GUILD_MAIN_TEXT
    
    
    def is_in_group_connectable(self):
        """
        Returns whether the channel is connectable.
        
        > Includes private connectable channels. Bots cannot connect to those, so you might want to use
        > ``.is_guild_connectable`` instead.
        
        Returns
        -------
        is_in_group_connectable : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_CONNECTABLE
    
    
    def is_in_group_guild_connectable(self):
        """
        Returns whether the channel is a guild connectable channel.
        
        Returns
        -------
        is_in_group_guild_connectable : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_GUILD_CONNECTABLE
    
    
    def is_in_group_private(self):
        """
        Returns whether the channel is a private channel.
        
        Returns
        -------
        is_in_group_private : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_PRIVATE
    
    
    def is_in_group_guild(self):
        """
        Returns whether the channel is a guild channel.
        
        Returns
        -------
        is_in_group_guild : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_GUILD
    
    
    def is_in_group_thread(self):
        """
        Returns whether the channel is a thread.
        
        Returns
        -------
        is_in_group_thread : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_THREAD
    
    
    def is_in_group_can_contain_threads(self):
        """
        Returns whether the channel can have threads.
        
        Returns
        -------
        is_in_group_can_contain_threads : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_CAN_CONTAIN_THREADS
    
    
    def is_in_group_can_create_invite_to(self):
        """
        Returns whether the channel have invites created to.
        
        Returns
        -------
        is_in_group_can_create_invite_to : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_CAN_CREATE_INVITE_TO
    
    
    def is_in_group_guild_movable(self):
        """
        Returns whether the channel is a movable guild channel.
        
        Returns
        -------
        is_in_group_guild_movable : `bool`
        """
        return self.metadata.type in CHANNEL_TYPES.GROUP_GUILD_MOVABLE
    
    
    def is_guild_text(self):
        """
        Returns whether the channel is a guild text channel.
        
        > Excludes Announcements and thread channels.
        
        Returns
        -------
        is_guild_text : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_text
    
    
    def is_private(self):
        """
        Returns whether the channel is a private or direct message (DM) channel.
        
        Returns
        -------
        is_private : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.private
        
        
    def is_guild_voice(self):
        """
        Returns whether the guild is a guild voice channel.
        
        > Excludes stage channels.
        
        Returns
        -------
        is_guild_voice : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_voice
    
    
    def is_private_group(self):
        """
        Returns whether the channel is a private group channel.
        
        Returns
        -------
        is_private_group : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.private_group
    
    
    def is_guild_category(self):
        """
        Returns whether the guild is a guild directory channel.
        
        Returns
        -------
        is_guild_category : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_category
    
    
    def is_guild_announcements(self):
        """
        Returns whether the channel is a guild announcements channel.
        
        Returns
        -------
        is_guild_announcements : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_announcements
    
    
    def is_guild_store(self):
        """
        Returns whether the channel is a guild store channels.
        
        > Store channels are deprecated & removed from Discord.
        
        Returns
        -------
        is_guild_store : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_store
    
    
    def is_thread(self):
        """
        Returns whether the channel is a thread channel.
        
        > This thread channel type never made into Discord.
        
        Returns
        -------
        is_thread : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.thread
    
    
    def is_guild_thread_announcements(self):
        """
        Returns whether the channel is a guild announcements thread.
        
        Returns
        -------
        is_guild_thread_announcements : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_thread_announcements
    
    
    def is_guild_thread_public(self):
        """
        Returns whether the channel is a guild public thread.
        
        Returns
        -------
        is_guild_thread_public : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_thread_public
    
    
    def is_guild_thread_private(self):
        """
        Returns whether the channel is a guild private thread.
        
        Returns
        -------
        is_guild_thread_private : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_thread_private
    
    
    def is_guild_stage(self):
        """
        Returns whether the channel is a guild stage channel.
        
        Returns
        -------
        is_guild_stage : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_stage
    
    
    def is_guild_directory(self):
        """
        Returns whether the channel is a guild directory channel.
        
        Returns
        -------
        is_guild_directory : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_directory
    
    
    def is_guild_forum(self):
        """
        Returns whether the channel is a guild forum channel.
        
        Returns
        -------
        is_guild_forum : `bool`
        """
        return self.metadata.type == CHANNEL_TYPES.guild_forum
