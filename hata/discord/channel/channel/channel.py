__all__ = ('Channel',)

import warnings
from collections import deque
from re import I as re_ignore_case, compile as re_compile, escape as re_escape, match as re_match, search as re_search

from scarletio import LOOP_TIME, copy_docs, export, include

from ....env import MESSAGE_CACHE_SIZE

from ...bases import DiscordEntity
from ...core import CHANNELS, GUILDS
from ...core import MESSAGES
from ...permission.permission import PERMISSION_STAGE_MODERATOR
from ...user import ZEROUSER, create_partial_user_from_id
from ...user.guild_profile.constants import (
    NICK_LENGTH_MAX as USER_NICK_LENGTH_MAX, NICK_LENGTH_MIN as USER_NICK_LENGTH_MIN
)
from ...user.user.constants import NAME_LENGTH_MAX as USER_NAME_LENGTH_MAX, NAME_LENGTH_MIN as USER_NAME_LENGTH_MIN
from ...user.user.matching import (
    USER_MATCH_WEIGHT_DISPLAY_NAME, USER_MATCH_WEIGHT_NAME, USER_MATCH_WEIGHT_NICK,
    _is_user_matching_name_with_discriminator, _parse_name_with_discriminator, _user_match_sort_key
)
from ...utils import DATETIME_FORMAT_CODE

from ..channel_metadata import ChannelMetadataBase, ChannelMetadataGuildMainBase
from ..forum_tag import create_forum_tag_from_id
from ..message_history import MessageHistory, MessageHistoryCollector, message_relative_index

from .preinstanced import ChannelType
from .fields import (
    parse_guild_id, parse_id, parse_type, put_guild_id_into, put_id_into, put_type_into, validate_guild_id, validate_id,
    validate_type
)
from .flags import (
    CHANNEL_TYPE_MASK_CONNECTABLE, CHANNEL_TYPE_MASK_FORUM, CHANNEL_TYPE_MASK_GUILD, CHANNEL_TYPE_MASK_GUILD_SORTABLE,
    CHANNEL_TYPE_MASK_GUILD_SYSTEM, CHANNEL_TYPE_MASK_INVITABLE, CHANNEL_TYPE_MASK_PRIVATE, CHANNEL_TYPE_MASK_TEXTUAL,
    CHANNEL_TYPE_MASK_THREAD, CHANNEL_TYPE_MASK_THREADABLE
)


create_partial_channel_from_id = include('create_partial_channel_from_id')
Message = include('Message')


CHANNEL_TYPE_MASK_GUILD_TEXTUAL = CHANNEL_TYPE_MASK_GUILD | CHANNEL_TYPE_MASK_TEXTUAL
CHANNEL_TYPE_MASK_GUILD_CONNECTABLE = CHANNEL_TYPE_MASK_GUILD | CHANNEL_TYPE_MASK_CONNECTABLE


USER_ALL_NAME_LENGTH_MAX = max(USER_NAME_LENGTH_MAX, USER_NICK_LENGTH_MAX)
USER_ALL_NAME_LENGTH_MIN = max(USER_NAME_LENGTH_MIN, USER_NICK_LENGTH_MIN)
USER_ALL_NAME_LENGTH_MAX_WITH_DISCRIMINATOR = USER_ALL_NAME_LENGTH_MAX + 5


@export
class Channel(DiscordEntity, immortal = True):
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
    type : ``ChannelType``
        The channel's type.
    """
    __slots__ = ('_message_history', 'guild_id', 'metadata', 'type')
    
    def __new__(cls, *, channel_type = ..., **keyword_parameters):
        """
        Creates a partial channel with the given parameters.
        
        Parameters
        ----------
        channel_type : `None`, `int`, ``ChanelType``, Optional (Keyword only)
            The channel's type.
        
        **keyword_parameters : Keyword parameters
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application's identifier the channel is managed by.
        
        archived : `bool`, Optional (Keyword only)
            Whether the (thread) channel is archived.
        
        archived_at : `None`, `datetime`, Optional (Keyword only)
            When the thread's archive status was last changed.
        
        applied_tag_ids : `None`, `tuple` of (`int`, ``ForumTag``), Optional (Keyword only)
             The tags' identifier which have been applied to the thread. Applicable for threads of a forum.
        
        auto_archive_after: `int`, Optional (Keyword only)
            The channel's ``.auto_archive_after``.
        
        available_tags : `None`, `tuple` of ``ForumTag``, Optional (Keyword only)
            The available tags to assign to the child-thread channels.
        
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the channel was created.
        
        bitrate : `int`, Optional (Keyword only)
            The bitrate (in bits) of the voice channel.
        
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the (thread) channel was created.
        
        default_forum_layout : ``ForumLayout``, `int`, Optional (Keyword only)
            The default layout used to display threads of the forum.
        
        default_sort_order : ``SortOrder``, `int`, Optional (Keyword only)
            The default thread ordering of the forum.
        
        default_thread_auto_archive_after : `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        
        default_thread_reaction : `None`, ``Emoji``, Optional (Keyword only)
            The emoji to show in the add reaction button on a thread of the forum channel.
        
        default_thread_slowmode : `int`, Optional (Keyword only)
            The default slowmode applied to the channel's threads.
        
        flags : `int`, ``ChannelFlag``, Optional (Keyword only)
            The channel's flags.
        
        icon : `None`, ``Icon``, `str`, `bytes`, Optional (Keyword only)
            The channel's icon.
        
        invitable : `bool`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads.
        
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        
        open : `bool`, Optional (Keyword only)
            Whether the thread channel is open.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The channel's owner's or creator's identifier.
        
        parent_id : `None`, `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        
        permission_overwrites : `None`, list` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        
        position : `int`, Optional (Keyword only)
            The channel's position.
        
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's voice region.
        
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode.
        
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        user_limit : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the voice channel, or `0` if unlimited.
            
        users : `iterable` of (`int`, ``ClientUserBase``), Optional (Keyword only)
            The users in the channel.
            
        video_quality_mode : ``VideoQualityMode``, Optional (Keyword only)
            The video quality of the voice channel.
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        if channel_type is ...:
            channel_type = ChannelType.unknown
        else:
            channel_type = validate_type(channel_type)
        
        metadata = channel_type.metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Unused or unsettable attributes: {keyword_parameters!r}.'
            )
        
        self = cls._create_empty(0, channel_type, 0)
        self.metadata = metadata
        return self
    
    
    @classmethod
    def from_data(cls, data, client = None, guild_id = 0, *, strong_cache = True):
        """
        Creates a new channel from the channel data received from Discord. If the channel already exists and if it
        is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Channel data receive from Discord.
        client : `None`, ``Client`` = `None`, Optional
            The client, who received the channel's data, if any.
        guild_id : `int` = `0`, Optional
            The guild's identifier of the channel.
        strong_cache : `bool` = `True`, Optional (Keyword only)
            Whether the instance should be put into its strong cache.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        -------
        RuntimeError
            The respective channel type cannot be instanced.
        """
        channel_id = parse_id(data)
        channel_type = parse_type(data)
        
        if not guild_id:
            guild_id = parse_guild_id(data)
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            metadata = channel_type.metadata_type.from_data(data)
            
            self = object.__new__(cls)
            self._message_history = None
            self.id = channel_id
            self.guild_id = guild_id
            self.metadata = metadata
            self.type = channel_type
            
            metadata._created(self, client, strong_cache)
            CHANNELS[channel_id] = self
            
        else:
            if strong_cache and (not self.partial):
                if self.type is not channel_type:
                    metadata = channel_type.metadata_type.from_data(data)
                    self.metadata = metadata
                    self.type = channel_type
                    metadata._created(self, client, strong_cache)
            else:
                self.guild_id = guild_id
                self._message_history = None
                
                metadata = channel_type.metadata_type.from_data(data)
                self.metadata = metadata
                self.type = channel_type
                metadata._created(self, client, strong_cache)
        
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
        self : `instance<cls>`
        """
        self = cls._create_empty(channel_id, ChannelType.private, 0)
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
        metadata._created(self, client, True)
    
    
    def __repr__(self):
        """Returns the representation of the channel."""
        repr_parts = ['<', self.__class__.__name__]
        
        channel_id = self.id
        if channel_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(channel_id))
            repr_parts.append(',')
        
        metadata = self.metadata
        repr_parts.append(' name = ')
        repr_parts.append(repr(metadata._get_processed_name()))
        
        channel_type = self.type
        repr_parts.append(' type = ')
        repr_parts.append(channel_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(channel_type.value))
        
        if self.partial:
            repr_parts.append(' (partial)')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the channel's hash value."""
        channel_id = self.id
        if channel_id:
            return channel_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Calculates the channel's hash based on their fields.
        
        This method is called by ``.__hash__`` if the channel has no ``.id`` set.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # guild_id
        hash_value ^= self.guild_id
        
        # metadata
        hash_value ^= hash(self.metadata)
        
        # type
        hash_value ^= self.type.value
        
        return hash_value
    
    
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
        >>> channel = Channel.precreate(now_as_id(), name = 'GENERAL')
        >>> channel
        <Channel id = 710506058560307200, name = 'GENERAL'>
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
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"d"!r}, {"m"!r}.'
        )
    
    
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
        if self.id == 0:
            return True
        
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
    
    
    def get_user(self, name, default = None):
        """
        Tries to find the a user with the given name at the channel. Returns the first matched one.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase``, `default`
        """
        name_length = len(name)
        if (name_length < USER_ALL_NAME_LENGTH_MIN) or (name_length > USER_ALL_NAME_LENGTH_MAX_WITH_DISCRIMINATOR):
            return default
        
        users = self.metadata._get_users(self)
        
        # name with discriminator
        
        name_with_discriminator = _parse_name_with_discriminator(name)
        if (name_with_discriminator is not None):
            for user in users:
                if _is_user_matching_name_with_discriminator(user, name_with_discriminator):
                    return user
        
        if name_length > USER_ALL_NAME_LENGTH_MAX:
            return default
        
        # name
        for user in users:
            if user.name == name:
                return user
        
        # global_name
        for user in users:
            user_display_name = user.display_name
            if (user_display_name is not None) and (user_display_name == name):
                return user
        
        # nick
        guild_id = self.guild_id
        if guild_id:
            for user in users:
                try:
                    guild_profile = user.guild_profiles[guild_id]
                except KeyError:
                    pass
                else:
                    nick = guild_profile.nick
                    if (nick is not None) and (nick == name):
                        return user
        
        return default
    
    
    def get_user_like(self, name, default = None):
        """
        Searches a user, who's name or nick starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase``, `default`
        """
        name_length = len(name)
        if name_length > USER_ALL_NAME_LENGTH_MAX_WITH_DISCRIMINATOR:
            return default
        
        users = self.metadata._get_users(self)
        
        # name with discriminator
        
        name_with_discriminator = _parse_name_with_discriminator(name)
        if (name_with_discriminator is not None):
            for user in users:
                if _is_user_matching_name_with_discriminator(user, name_with_discriminator):
                    return user
        
        if name_length > USER_ALL_NAME_LENGTH_MAX:
            return default
        
        user_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        accurate_user = default
        accurate_match_key = None
        
        # name
        
        for user in users:
            parsed = user_name_pattern.search(user.name)
            if (parsed is None):
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            match_rate = (USER_MATCH_WEIGHT_NAME, match_length, match_start)
            if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                continue
            
            accurate_user = user
            accurate_match_key = match_rate
            continue
        
        if (accurate_match_key is not None):
            return accurate_user
        
        # display name

        for user in users:
            user_display_name = user.display_name
            if (user_display_name is None):
                continue
            
            parsed = user_name_pattern.search(user_display_name)
            if (parsed is None):
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            match_rate = (USER_MATCH_WEIGHT_DISPLAY_NAME, match_length, match_start)
            if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                continue
            
            accurate_user = user
            accurate_match_key = match_rate
            continue
        
        if (accurate_match_key is not None):
            return accurate_user
        
        # nick
        
        guild_id = self.id
        if guild_id:
            for user in users:
                try:
                    guild_profile = user.guild_profiles[guild_id]
                except KeyError:
                    continue
                
                user_nick = guild_profile.nick
                if (user_nick is None):
                    continue
                
                parsed = user_name_pattern.search(user_nick)
                if (parsed is None):
                    continue
                
                match_start = parsed.start()
                match_length = parsed.end() - match_start
                
                match_rate = (USER_MATCH_WEIGHT_NICK, match_length, match_start)
                if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                    continue
                
                accurate_user = user
                accurate_match_key = match_rate
                continue
        
        return accurate_user
    
    
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
        name_length = len(name)
        if name_length > USER_ALL_NAME_LENGTH_MAX_WITH_DISCRIMINATOR:
            return []
        
        users = self.metadata._get_users(self)
        
        # name with discriminator
        
        name_with_discriminator = _parse_name_with_discriminator(name)
        if (name_with_discriminator is not None):
            for user in users:
                if _is_user_matching_name_with_discriminator(user, name_with_discriminator):
                    return [user]
        
        if name_length > USER_ALL_NAME_LENGTH_MAX:
            return []
        
        user_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        matches = []
        guild_id = self.guild_id
        
        for user in users:
            # name
            
            parsed = user_name_pattern.search(user.name)
            if (parsed is not None):
                match_start = parsed.start()
                match_length = parsed.end() - match_start
                
                match_rate = (USER_MATCH_WEIGHT_NAME, match_length, match_start)
                
                matches.append((user, match_rate))
                continue
            
            # display_name
            
            user_display_name = user.display_name
            if (user_display_name is not None):
                parsed = user_name_pattern.search(user_display_name)
                if (parsed is not None):
                    match_start = parsed.start()
                    match_length = parsed.end() - match_start
                    
                    match_rate = (USER_MATCH_WEIGHT_DISPLAY_NAME, match_length, match_start)
                    
                    matches.append((user, match_rate))
                    continue
            
            # nick
            
            if guild_id:
                try:
                    guild_profile = user.guild_profiles[guild_id]
                except KeyError:
                    pass
                else:
                    user_nick = guild_profile.nick
                    if (user_nick is not None):
                        parsed = user_name_pattern.search(user_nick)
                        if (parsed is not None):
                            match_start = parsed.start()
                            match_length = parsed.end() - match_start
                            
                            match_rate = (USER_MATCH_WEIGHT_NICK, match_length, match_start)
                            
                            matches.append((user, match_rate))
                            continue
        
        return [item[0] for item in sorted(matches, key = _user_match_sort_key)]
    
    
    @property
    def users(self):
        """
        The users who can see this channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return self.metadata._get_users(self)
    
    
    def iter_users(self):
        """
        Iterates over the users who can see the channel.
        
        This method is a generator.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        yield from self.metadata._iter_users(self)
    
    
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
        
            match_start = False
        else:
            match_start = True
        
        target_name_length = len(name)
        if (target_name_length < 2) or (target_name_length > 100):
            return False
        
        if match_start:
            matching_function = re_search
        else:
            matching_function = re_match
        
        if matching_function(re_escape(name), self.name, re_ignore_case) is None:
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
        return self.metadata._get_permissions_for_roles(self, roles)
    
    
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
    
    
    def iter_threads(self):
        """
        Iterates over the channel's threads.
        
        This method is an iterable generator.
        
        Yields
        ------
        channel : ``Channel``
        """
        guild = self.guild
        if guild is None:
            return
        
        channel_id = self.id
        
        for thread in guild.threads.values():
            if thread.parent_id == channel_id:
                yield thread
    
    
    @property
    def threads(self):
        """
        Returns the channel's threads.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [*self.iter_threads()]
    
    
    def _update_attributes(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Channel data received from Discord.
        """
        channel_type = parse_type(data)
        
        if channel_type is self.type:
            self.metadata._update_attributes(data)
        else:
            self.metadata = channel_type.metadata_type.from_data(data)
        
        self.type = channel_type
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the channel and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Channel data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dict is optional.
            
            Might contain the following items:
            
            +---------------------------------------+-----------------------------------------------------------+
            | Keys                                  | Values                                                    |
            +=======================================+===========================================================+
            | applied_tag_ids                       | `None`, `tuple` of `int`                                  |
            +---------------------------------------+-----------------------------------------------------------+
            | archived                              | `bool`                                                    |
            +---------------------------------------+-----------------------------------------------------------+
            | archived_at                           | `None`, `datetime`                                        |
            +---------------------------------------+-----------------------------------------------------------+
            | auto_archive_after                    | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | available_tags                        | ``ForumTagChange``                                        |
            +---------------------------------------+-----------------------------------------------------------+
            | bitrate                               | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | default_forum_layout                  | ``ForumLayout``                                           |
            +---------------------------------------+-----------------------------------------------------------+
            | default_sort_order                    | ``SortOrder``                                             |
            +---------------------------------------+-----------------------------------------------------------+
            | default_thread_auto_archive_after     | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | default_thread_reaction               | `None`, ``Emoji``                                         |
            +---------------------------------------+-----------------------------------------------------------+
            | default_thread_slowmode               | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | flags                                 | ``ChannelFlag``                                           |
            +---------------------------------------+-----------------------------------------------------------+
            | icon                                  | ``Icon``                                                  |
            +---------------------------------------+-----------------------------------------------------------+
            | invitable                             | `bool`                                                    |
            +---------------------------------------+-----------------------------------------------------------+
            | metadata                              | ``ChannelMetadataBase``                                   |
            +---------------------------------------+-----------------------------------------------------------+
            | name                                  | `str`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | nsfw                                  | `bool`                                                    |
            +---------------------------------------+-----------------------------------------------------------+
            | open                                  | `bool`                                                    |
            +---------------------------------------+-----------------------------------------------------------+
            | owner_id                              | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | parent_id                             | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | permission_overwrites                 | `None`, `dict` of (`int`, ``PermissionOverwrite``) items  |
            +---------------------------------------+-----------------------------------------------------------+
            | position                              | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | region                                | `None`, ``VoiceRegion``                                   |
            +---------------------------------------+-----------------------------------------------------------+
            | slowmode                              | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | topic                                 | `None`, `str`                                             |
            +---------------------------------------+-----------------------------------------------------------+
            | type                                  | ``ChannelType``                                           |
            +---------------------------------------+-----------------------------------------------------------+
            | user_limit                            | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | video_quality_mode                    | ``VideoQualityMode``                                      |
            +---------------------------------------+-----------------------------------------------------------+
        """
        channel_type = parse_type(data)
        
        if channel_type is self.type:
            old_attributes = self.metadata._difference_update_attributes(data)
            
        else:
            old_attributes = {
                'metadata': self.metadata,
                'type': self.type
            }
            
            self.metadata = channel_type.metadata_type.from_data(data)
            self.type = channel_type
        
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
    
    
    def _iter_delete(self, client):
        """
        Called when a channel is deleted. Not like ``._delete`` this will apply deletion to all related channel as well,
        technically calling ``._delete`` on all.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        client : `None`, ``Client``
            The parent client entity.
        
        Yields
        ------
        channel : ``Channel``
        """
        yield from self.metadata._iter_delete(self, client)
    
    
    @classmethod
    def _from_partial_data(cls, data, channel_id, guild_id):
        """
        Creates a channel from partial data. Called by ``create_partial_channel_from_data`` when a new
        partial channel is needed to be created.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `object`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        guild_id : `int`
            The channel's guild's identifier if applicable.
        
        Returns
        -------
        self : `instance<cls>`
        """
        if not guild_id:
            guild_id = parse_guild_id(data)
        
        channel_type = parse_type(data)
        metadata = channel_type.metadata_type._from_partial_data(data)
        
        self = object.__new__(cls)
        self._message_history = None
        self.id = channel_id
        self.guild_id = guild_id
        self.metadata = metadata
        self.type = channel_type
        
        return self
    
    
    @classmethod
    def _create_empty(cls, channel_id, channel_type, guild_id):
        """
        Creates a partial channel from the given parameters.
        
        Parameters
        ----------
        channel_id : `int`
            The channel's identifier.
        channel_type : ``ChannelType``
            The channel's type.
        guild_id : `int`
            A partial guild's identifier for the created channel.
        
        Returns
        -------
        self : `instance<cls>`
            The created partial channel.
        """
        self = object.__new__(cls)
        self._message_history = None
        self.id = channel_id
        self.guild_id = guild_id
        self.metadata = channel_type.metadata_type._create_empty()
        self.type = channel_type
        return self
    
    
    def copy(self):
        """
        Copies the channel returning a new partial one.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        new._message_history = None
        new.id = 0
        new.guild_id = 0
        new.metadata = self.metadata.copy()
        new.type = self.type
        return new
    
    
    def copy_with(self, *, channel_type = ..., **keyword_parameters):
        """
        Copies the channel with the given fields.
        
        Parameters
        ----------
        channel_type : `int`, ``ChannelType`` = `None`, Optional (Keyword only)
            The new channel's type.
        **keyword_parameters : Keyword parameters
            Additional parameters to pass to the channel-type specific constructor.
        
        Other Parameters
        ----------------
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application's identifier the channel is managed by.
        
        archived : `bool`, Optional (Keyword only)
            Whether the (thread) channel is archived.
        
        archived_at : `None`, `datetime`, Optional (Keyword only)
            When the thread's archive status was last changed.
        
        applied_tag_ids : `None`, `tuple` of (`int`, ``ForumTag``), Optional (Keyword only)
             The tags' identifier which have been applied to the thread. Applicable for threads of a forum.
        
        auto_archive_after: `int`, Optional (Keyword only)
            The channel's ``.auto_archive_after``.
        
        available_tags : `None`, `tuple` of ``ForumTag``, Optional (Keyword only)
            The available tags to assign to the child-thread channels.
        
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the channel was created.
        
        bitrate : `int`, Optional (Keyword only)
            The bitrate (in bits) of the voice channel.
        
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the (thread) channel was created.
        
        default_forum_layout : ``ForumLayout``, `int`, Optional (Keyword only)
            The default layout used to display threads of the forum.
        
        default_sort_order : ``SortOrder``, `int`, Optional (Keyword only)
            The default thread ordering of the forum.
        
        default_thread_auto_archive_after : `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        
        default_thread_reaction : `None`, ``Emoji``, Optional (Keyword only)
            The emoji to show in the add reaction button on a thread of the forum channel.
        
        default_thread_slowmode : `int`, Optional (Keyword only)
            The default slowmode applied to the channel's threads.
        
        flags : `int`, ``ChannelFlag``, Optional (Keyword only)
            The channel's flags.
        
        icon : `None`, ``Icon``, `str`, `bytes`, Optional (Keyword only)
            The channel's icon.
        
        invitable : `bool`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads.
        
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        
        open : `bool`, Optional (Keyword only)
            Whether the thread channel is open.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The channel's owner's or creator's identifier.
        
        parent_id : `None`, `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        
        permission_overwrites : `None`, list` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        
        position : `int`, Optional (Keyword only)
            The channel's position.
        
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's voice region.
        
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode.
        
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        user_limit : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the voice channel, or `0` if unlimited.
        
        users : `iterable` of (`int`, ``ClientUserBase``), Optional (Keyword only)
            The users in the channel.
        
        video_quality_mode : ``VideoQualityMode``, Optional (Keyword only)
            The video quality of the voice channel.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - If extra or unused parameters were given.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_type
        if channel_type is ...:
            channel_type = self.type
        else:
            channel_type = validate_type(channel_type)
        
        # metadata
        metadata = self.metadata
        metadata_type = channel_type.metadata_type
        if metadata_type is type(metadata):
            metadata = metadata.copy_with_keyword_parameters(keyword_parameters)
        else:
            metadata = metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused keyword parameters: {keyword_parameters!r}.'
            )
        
        new = object.__new__(type(self))
        new._message_history = None
        new.id = 0
        new.guild_id = 0
        new.metadata = metadata
        new.type = channel_type
        return new
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the channel to json serializable representation dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether we want to include identifiers as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = self.metadata.to_data(defaults = defaults, include_internals = include_internals)
        
        # type
        put_type_into(self.type, data, defaults)
        
        if include_internals:
            # id
            put_id_into(self.id, data, defaults)
            
            # guild_id
            put_guild_id_into(self.guild_id, data, defaults)
        
        return data
    
    
    @property
    def created_at(self):
        """
        Returns when the channel was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        return self.metadata._get_created_at(self)
    
    
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
            
            if self_order_group < other_order_group:
                return False
            
            self_position = self_metadata.position
            other_position = other_metadata.position
            
            if self_position > other_position:
                return True
            
            if self_position < other_position:
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
            
            if self_order_group < other_order_group:
                return False
                
            self_position = self_metadata.position
            other_position = other_metadata.position
            
            if self_position > other_position:
                return True
            
            if self_position < other_position:
                return False
        
        
        return self.id >= other.id
        
    
    def __eq__(self, other):
        """Returns whether this channel's is equal to the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_time(other)
        
    
    def __ne__(self,other):
        """Returns whether this channel's is not equal to the other's."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_time(other)
    
    
    def _is_equal_same_time(self, other):
        """
        Returns whether the channel is equal to the other one.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other channel entity.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self_id == other_id:
                return True
            
            return False
        
        # guild_id
        # Internal field -> ignore
        
        # metadata
        if self.metadata != other.metadata:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
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
            
            if self_order_group > other_order_group:
                return False
            
            self_position = self_metadata.position
            other_position = other_metadata.position
            
            if self_position < other_position:
                return True
            
            if self_position > other_position:
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
            
            if self_order_group > other_order_group:
                return False
                
            self_position = self_metadata.position
            other_position = other_metadata.position
            
            if self_position < other_position:
                return True
            
            if self_position > other_position:
                return False
        
        
        return self.id < other.id
    
    # Fields
    
    @property
    @copy_docs(ChannelMetadataBase.application_id)
    def application_id(self):
        return self.metadata.application_id
    
    @property
    @copy_docs(ChannelMetadataBase.applied_tag_ids)
    def applied_tag_ids(self):
        return self.metadata.applied_tag_ids
    
    
    @property
    @copy_docs(ChannelMetadataBase.archived)
    def archived(self):
        return self.metadata.archived
    
    
    @property
    @copy_docs(ChannelMetadataBase.archived_at)
    def archived_at(self):
        return self.metadata.archived_at
    
    
    @property
    @copy_docs(ChannelMetadataBase.auto_archive_after)
    def auto_archive_after(self):
        return self.metadata.auto_archive_after
    
    
    @property
    @copy_docs(ChannelMetadataBase.available_tags)
    def available_tags(self):
        return self.metadata.available_tags
    
    
    @property
    @copy_docs(ChannelMetadataBase.bitrate)
    def bitrate(self):
        return self.metadata.bitrate
    
    
    @property
    @copy_docs(ChannelMetadataBase.default_forum_layout)
    def default_forum_layout(self):
        return self.metadata.default_forum_layout
    
    
    @property
    @copy_docs(ChannelMetadataBase.default_sort_order)
    def default_sort_order(self):
        return self.metadata.default_sort_order
    
    
    @property
    @copy_docs(ChannelMetadataBase.default_thread_auto_archive_after)
    def default_thread_auto_archive_after(self):
        return self.metadata.default_thread_auto_archive_after
    
    
    @property
    @copy_docs(ChannelMetadataBase.default_thread_reaction)
    def default_thread_reaction(self):
        return self.metadata.default_thread_reaction
    
    
    @property
    @copy_docs(ChannelMetadataBase.default_thread_slowmode)
    def default_thread_slowmode(self):
        return self.metadata.default_thread_slowmode
    
    
    @property
    @copy_docs(ChannelMetadataBase.flags)
    def flags(self):
        return self.metadata.flags
    
    
    @property
    @copy_docs(ChannelMetadataBase.icon)
    def icon(self):
        return self.metadata.icon
    
    
    @property
    @copy_docs(ChannelMetadataBase.invitable)
    def invitable(self):
        return self.metadata.invitable
    
    
    @property
    @copy_docs(ChannelMetadataBase.name)
    def name(self):
        return self.metadata.name
    
    
    @property
    @copy_docs(ChannelMetadataBase.nsfw)
    def nsfw(self):
        return self.metadata.nsfw
    
    
    @property
    @copy_docs(ChannelMetadataBase.open)
    def open(self):
        return self.metadata.open
    
    
    @property
    @copy_docs(ChannelMetadataBase.owner_id)
    def owner_id(self):
        return self.metadata.owner_id
    
    
    @property
    @copy_docs(ChannelMetadataBase.parent_id)
    def parent_id(self):
        return self.metadata.parent_id
    
    
    @property
    @copy_docs(ChannelMetadataBase.permission_overwrites)
    def permission_overwrites(self):
        return self.metadata.permission_overwrites
    
    
    @property
    @copy_docs(ChannelMetadataBase.position)
    def position(self):
        return self.metadata.position
    
    
    @property
    @copy_docs(ChannelMetadataBase.region)
    def region(self):
        return self.metadata.region
    
    
    @property
    @copy_docs(ChannelMetadataBase.slowmode)
    def slowmode(self):
        return self.metadata.slowmode
    
    
    @property
    @copy_docs(ChannelMetadataBase.topic)
    def topic(self):
        return self.metadata.topic
    
    
    @property
    @copy_docs(ChannelMetadataBase.thread_users)
    def thread_users(self):
        return self.metadata.thread_users
    
    
    @thread_users.setter
    def thread_users(self, thread_users):
        self.metadata.thread_users = thread_users
    
    
    @property
    @copy_docs(ChannelMetadataBase.user_limit)
    def user_limit(self):
        return self.metadata.user_limit
    
    
    @property
    @copy_docs(ChannelMetadataBase.video_quality_mode)
    def video_quality_mode(self):
        return self.metadata.video_quality_mode
    
    # Utility
    
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
            return create_partial_channel_from_id(parent_id, ChannelType.unknown, self.guild_id)
    
    
    @property
    def applied_tags(self):
        """
        Returns the applied tags to the thread.
        
        Returns
        -------
        applied_tags : `None`, `tuple` of ``ForumTag``
        """
        applied_tag_ids = self.applied_tag_ids
        if (applied_tag_ids is None):
            return None
        
        return tuple(create_forum_tag_from_id(forum_tag_id) for forum_tag_id in applied_tag_ids)
    
    
    def iter_applied_tag_ids(self):
        """
        Iterates over the applied tag identifiers of the channel.
        
        This method is an iterable generator.
        
        Yields
        ------
        applied_tag_id : `int`
        """
        applied_tag_ids = self.applied_tag_ids
        if (applied_tag_ids is not None):
            yield from applied_tag_ids
    
    
    def iter_applied_tags(self):
        """
        Iterates over the applied tags of the channels.
        
        This method is an iterable generator.
        
        Yields
        ------
        applied_tag : ``ForumTag``
        """
        applied_tag_ids = self.applied_tag_ids
        if (applied_tag_ids is not None):
            for forum_tag_id in applied_tag_ids:
                yield create_forum_tag_from_id(forum_tag_id)
    
    
    def iter_available_tags(self):
        """
        Iterates over the available tags of the the forum channel.
        
        This method is an iterable generator.
        
        Yields
        ------
        available_tag : ``ForumTag``
        """
        available_tags = self.available_tags
        if (available_tags is not None):
            yield from available_tags
    
    
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
    
    
    def iter_channels(self):
        """
        Iterates over the channels of the category.
        
        > Unordered.
        
        This method is an iterable generator.
        
        Yields
        ------
        channel : ``Channel``
        """
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
                        yield channel
    
    
    @property
    def channels(self):
        """
        Returns the channels of the category in a list in their display order.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return sorted(self.iter_channels())
    
    
    @property
    def channel_list(self):
        """
        Deprecated and will be removed in 2023 September. Please use ``.channels`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.channel_list` is deprecated and will be removed in '
                f'2023 September. Please use `.channels` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.channels
    
    
    def iter_voice_users(self):
        """
        Iterates over the users who are in the voice channel.
        
        This method is an iterable generator.
        
        Yields
        -------
        user : ``ClientUserBase``
        """
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
                        yield voice_state.user
    
    
    @property
    def voice_users(self):
        """
        Returns a list of the users who are in the voice channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return [*self.iter_voice_users()]
    
    
    def iter_audience(self):
        """
        Iterates over the audience in the stage channel.
        
        This method is an iterable generator.
        
        Yields
        -------
        user : ``ClientUserBase``
        """
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                channel_id = self.id
                
                for voice_states in guild.voice_states.values():
                    if (voice_states.channel_id == channel_id) and (not voice_states.speaker):
                        yield voice_states.user
    
    
    @property
    def audience(self):
        """
        Returns the audience in the stage channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return [*self.iter_audience()]
    
    
    def iter_speakers(self):
        """
        Iterates over the speakers in the stage channel.
        
        This method is an iterable generator.
        
        Yields
        -------
        user : ``ClientUserBase``
        """
        guild_id = self.guild_id
        if guild_id:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                pass
            else:
                channel_id = self.id
                
                for voice_states in guild.voice_states.values():
                    if (voice_states.channel_id == channel_id) and voice_states.speaker:
                        yield voice_states.user
    
    
    @property
    def speakers(self):
        """
        Returns the speakers in the stage channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return [*self.iter_speakers()]
    
    
    def iter_moderators(self):
        """
        Iterates over the moderators in the stage channel.
        
        This method is an iterable generator.
        
        Yields
        -------
        user : ``ClientUserBase``
        """
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
                            yield user
    
    
    @property
    def moderators(self):
        """
        Returns the moderators in the stage channel.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return [*self.iter_moderators()]
    
    
    @classmethod
    def precreate(cls, channel_id, *, channel_type = ..., guild_id = ..., **keyword_parameters):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precreated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int`, `str`
            The channel's id.
        
        channel_type : `None`, `int`, ``ChanelType``, Optional (Keyword only)
            The channel's type.

        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The channel's parent guild's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        application_id : `int`, ``Application``, Optional (Keyword only)
            The application's identifier the channel is managed by.
        
        archived : `bool`, Optional (Keyword only)
            Whether the (thread) channel is archived.
        
        archived_at : `None`, `datetime`, Optional (Keyword only)
            When the thread's archive status was last changed.
        
        applied_tag_ids : `None`, `tuple` of (`int`, ``ForumTag``), Optional (Keyword only)
             The tags' identifier which have been applied to the thread. Applicable for threads of a forum.
        
        auto_archive_after: `int`, Optional (Keyword only)
            The channel's ``.auto_archive_after``.
        
        available_tags : `None`, `tuple` of ``ForumTag``, Optional (Keyword only)
            The available tags to assign to the child-thread channels.
        
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the channel was created.
        
        bitrate : `int`, Optional (Keyword only)
            The bitrate (in bits) of the voice channel.
        
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the (thread) channel was created.
        
        default_forum_layout : ``ForumLayout``, `int`, Optional (Keyword only)
            The default layout used to display threads of the forum.
        
        default_sort_order : ``SortOrder``, `int`, Optional (Keyword only)
            The default thread ordering of the forum.
        
        default_thread_auto_archive_after : `int`, Optional (Keyword only)
            The channel's ``.default_thread_auto_archive_after``.
        
        default_thread_slowmode : `int`, Optional (Keyword only)
            The default slowmode applied to the channel's threads.
        
        default_thread_reaction : `None`, ``Emoji``, Optional (Keyword only)
            The emoji to show in the add reaction button on a thread of the forum channel.
        
        flags : `int`, ``ChannelFlag``, Optional (Keyword only)
            The channel's flags.
        
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The channel's icon.
            
            > Mutually exclusive with `icon_type` and `icon_hash` parameters.
        
        icon_type : ``IconType``, Optional (Keyword only)
            The channel's icon's type.
            
            > Mutually exclusive with the `icon` parameter.
        
        icon_hash : `int`, Optional (Keyword only)
            The channel's icon's hash.
            
            > Mutually exclusive with the `icon` parameter.
        
        invitable : `bool`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads.
        
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        
        open : `bool`, Optional (Keyword only)
            Whether the thread channel is open.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The channel's owner's or creator's identifier.
        
        parent_id : `None`, `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        
        permission_overwrites : `None`, list` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        
        position : `int`, Optional (Keyword only)
            The channel's position.
        
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's voice region.
        
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode.
        
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        user_limit : `int`, Optional (Keyword only)
            The channel's ``.user_limit``.
            
        users : `iterable` of (`int`, ``ClientUserBase``), Optional (Keyword only)
            The users in the channel.
            
        video_quality_mode : ``VideoQualityMode``, Optional (Keyword only)
            The video quality of the voice channel.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        channel_id = validate_id(channel_id)
        
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        if channel_type is ...:
            channel_type = ChannelType.unknown
        else:
            channel_type = validate_type(channel_type)
        
        metadata = channel_type.metadata_type.from_keyword_parameters(keyword_parameters)
        
        if keyword_parameters:
            raise TypeError(
                f'Unused or unsettable attributes: {keyword_parameters!r}.'
            )
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, channel_type, guild_id)
            CHANNELS[channel_id] = self
        else:
            if self.partial:
                self.type = channel_type
            
            else:
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
        message_data : `dict` of (`str`, `object`) items
            Message data received from Discord.
        
        Returns
        -------
        message : ``Message``
        """
        message, was_up_to_date = Message._create_message_was_up_to_date(message_data)
        if was_up_to_date:
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
        message_data : `dict` of (`str`, `object`) items
            Message data received from Discord.
        
        Returns
        -------
        message : ``Message``
        
        Notes
        -----
        The created message cannot be added to the channel's message history, if it has no more spaces.
        """
        message = Message.from_data(message_data)
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
        message_data : `dict` of (`str`, `object`) items
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
        
        message = Message.from_data(message_data)
        
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
                    self.messages = messages = deque(maxlen = None)
            else:
                self.messages = messages = deque(maxlen = message_keep_limit)
        else:
            
            max_length = messages.maxlen
            if (max_length is not None) and (len(messages) == max_length):
                if self._message_history_collector is None:
                    self.message_history_reached_end = False
                else:
                    self.messages = messages = deque(messages, maxlen = None)
        
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
        delete_ids.sort(reverse = True)
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
        Deprecated and will be removed in 2023 January. Please use ``.is_in_group_textual`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_in_group_messageable` is deprecated and will be removed in '
                f'2023 January. Please use `.is_in_group_textual` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.is_in_group_textual()
    
    
    def is_in_group_textual(self):
        """
        Returns whether the channel is messageable.
        
        Returns
        -------
        is_in_group_textual : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_TEXTUAL == CHANNEL_TYPE_MASK_TEXTUAL
    
    
    def is_in_group_guild_messageable(self):
        """
        Deprecated and will be removed in 2023 January. Please use ``.is_in_group_guild_textual`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_in_group_guild_messageable` is deprecated and will be removed in '
                f'2023 January. Please use `.is_in_group_guild_textual` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.is_in_group_guild_textual()
    
    
    def is_in_group_guild_textual(self):
        """
        Returns whether the channel is a guild and messageable one.
        
        Returns
        -------
        is_in_group_guild_textual : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_GUILD_TEXTUAL == CHANNEL_TYPE_MASK_GUILD_TEXTUAL
    
    
    def is_in_group_guild_main_text(self):
        """
        Deprecated and will be removed in 2023 January. Please use ``.is_in_group_guild_system`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_in_group_guild_main_text` is deprecated and will be removed in '
                f'2023 January. Please use `.is_in_group_guild_system` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.is_in_group_guild_system()
    
    
    def is_in_group_guild_system(self):
        """
        Returns whether the channel a guild text like channel.
        
        > Excludes connectable and thread channels.
        
        Returns
        -------
        is_in_group_guild_system : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_GUILD_SYSTEM == CHANNEL_TYPE_MASK_GUILD_SYSTEM
    
    
    def is_in_group_connectable(self):
        """
        Returns whether the channel is connectable.
        
        > Includes private connectable channels. Bots cannot connect to those, so you might want to use
        > ``.is_guild_connectable`` instead.
        
        Returns
        -------
        is_in_group_connectable : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_CONNECTABLE == CHANNEL_TYPE_MASK_CONNECTABLE
    
    
    def is_in_group_guild_connectable(self):
        """
        Returns whether the channel is a guild connectable channel.
        
        Returns
        -------
        is_in_group_guild_connectable : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_GUILD_CONNECTABLE == CHANNEL_TYPE_MASK_GUILD_CONNECTABLE
    
    
    def is_in_group_private(self):
        """
        Returns whether the channel is a private channel.
        
        Returns
        -------
        is_in_group_private : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_PRIVATE == CHANNEL_TYPE_MASK_PRIVATE
    
    
    def is_in_group_guild(self):
        """
        Returns whether the channel is a guild channel.
        
        Returns
        -------
        is_in_group_guild : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_GUILD == CHANNEL_TYPE_MASK_GUILD
    
    
    def is_in_group_thread(self):
        """
        Returns whether the channel is a thread.
        
        Returns
        -------
        is_in_group_thread : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_THREAD == CHANNEL_TYPE_MASK_THREAD
    
    
    def is_in_group_can_contain_threads(self):
        """
        Deprecated and will be removed in 2023 January. Please use ``.is_in_group_threadable`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_in_group_can_contain_threads` is deprecated and will be removed in '
                f'2023 January. Please use `.is_in_group_threadable` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.is_in_group_threadable()
    
    
    def is_in_group_threadable(self):
        """
        Returns whether the channel can have threads.
        
        Returns
        -------
        is_in_group_threadable : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_THREADABLE == CHANNEL_TYPE_MASK_THREADABLE
    
    
    def is_in_group_can_create_invite_to(self):
        """
        Deprecated and will be removed in 2023 January. Please use ``.is_in_group_invitable`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_in_group_can_create_invite_to` is deprecated and will be removed in '
                f'2023 January. Please use `.is_in_group_invitable` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.is_in_group_invitable()
    
    
    def is_in_group_invitable(self):
        """
        Returns whether the channel have invites created to.
        
        Returns
        -------
        is_in_group_invitable : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_INVITABLE == CHANNEL_TYPE_MASK_INVITABLE
    
    
    def is_in_group_guild_movable(self):
        """
        Deprecated and will be removed in 2023 January. Please use ``.is_in_group_guild_sortable`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_in_group_guild_movable` is deprecated and will be removed in '
                f'2023 January. Please use `.is_in_group_guild_sortable` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.is_in_group_guild_sortable()
    
    
    def is_in_group_guild_sortable(self):
        """
        Returns whether the channel is a sortable guild channel.
        
        Returns
        -------
        is_in_group_guild_sortable : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_GUILD_SORTABLE == CHANNEL_TYPE_MASK_GUILD_SORTABLE
    
    
    def is_in_group_forum(self):
        """
        Returns whether the channel is a forum channel. Can be either `forum` or `media`.
        
        Returns
        -------
        is_in_group_forum : `bool`
        """
        return self.type.flags & CHANNEL_TYPE_MASK_FORUM == CHANNEL_TYPE_MASK_FORUM
    
    
    def is_guild_text(self):
        """
        Returns whether the channel is a guild text channel.
        
        > Excludes Announcements and thread channels.
        
        Returns
        -------
        is_guild_text : `int`
        """
        return self.type is ChannelType.guild_text
    
    
    def is_private(self):
        """
        Returns whether the channel is a private or direct message (DM) channel.
        
        Returns
        -------
        is_private : `int`
        """
        return self.type is ChannelType.private
        
        
    def is_guild_voice(self):
        """
        Returns whether the guild is a guild voice channel.
        
        > Excludes stage channels.
        
        Returns
        -------
        is_guild_voice : `int`
        """
        return self.type is ChannelType.guild_voice
    
    
    def is_private_group(self):
        """
        Returns whether the channel is a private group channel.
        
        Returns
        -------
        is_private_group : `int`
        """
        return self.type is ChannelType.private_group
    
    
    def is_guild_category(self):
        """
        Returns whether the guild is a guild directory channel.
        
        Returns
        -------
        is_guild_category : `int`
        """
        return self.type is ChannelType.guild_category
    
    
    def is_guild_announcements(self):
        """
        Returns whether the channel is a guild announcements channel.
        
        Returns
        -------
        is_guild_announcements : `int`
        """
        return self.type is ChannelType.guild_announcements
    
    
    def is_guild_store(self):
        """
        Returns whether the channel is a guild store channels.
        
        > Store channels are deprecated & removed from Discord.
        
        Returns
        -------
        is_guild_store : `int`
        """
        return self.type is ChannelType.guild_store
    
    
    def is_thread(self):
        """
        Returns whether the channel is a thread channel.
        
        > This thread channel type never made into Discord.
        
        Returns
        -------
        is_thread : `bool`
        """
        return self.type is ChannelType.thread
    
    
    def is_guild_thread_announcements(self):
        """
        Returns whether the channel is a guild announcements thread.
        
        Returns
        -------
        is_guild_thread_announcements : `bool`
        """
        return self.type is ChannelType.guild_thread_announcements
    
    
    def is_guild_thread_public(self):
        """
        Returns whether the channel is a guild public thread.
        
        Returns
        -------
        is_guild_thread_public : `bool`
        """
        return self.type is ChannelType.guild_thread_public
    
    
    def is_guild_thread_private(self):
        """
        Returns whether the channel is a guild private thread.
        
        Returns
        -------
        is_guild_thread_private : `bool`
        """
        return self.type is ChannelType.guild_thread_private
    
    
    def is_guild_stage(self):
        """
        Returns whether the channel is a guild stage channel.
        
        Returns
        -------
        is_guild_stage : `bool`
        """
        return self.type is ChannelType.guild_stage
    
    
    def is_guild_directory(self):
        """
        Returns whether the channel is a guild directory channel.
        
        Returns
        -------
        is_guild_directory : `bool`
        """
        return self.type is ChannelType.guild_directory
    
    
    def is_guild_forum(self):
        """
        Returns whether the channel is a guild forum channel.
        
        Returns
        -------
        is_guild_forum : `bool`
        """
        return self.type is ChannelType.guild_forum
    
    
    def is_guild_media(self):
        """
        Returns whether the channel is a guild media channel.
        
        Returns
        -------
        is_guild_media : `bool`
        """
        return self.type is ChannelType.guild_media
