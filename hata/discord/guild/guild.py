__all__ = (
    'COMMUNITY_FEATURES', 'EMOJI_UPDATE_DELETE', 'EMOJI_UPDATE_EDIT', 'EMOJI_UPDATE_CREATE', 'EMOJI_UPDATE_NONE',
    'Guild', 'LARGE_GUILD_LIMIT', 'STICKER_UPDATE_DELETE', 'STICKER_UPDATE_EDIT', 'STICKER_UPDATE_CREATE',
    'STICKER_UPDATE_NONE', 'VOICE_STATE_JOIN', 'VOICE_STATE_LEAVE', 'VOICE_STATE_NONE', 'VOICE_STATE_MOVE',
    'VOICE_STATE_UPDATE'
)

import warnings
from datetime import datetime
from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from scarletio import WeakValueDictionary, export, include

from ...env import CACHE_PRESENCE, CACHE_USER

from ..bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ..channel import Channel
from ..core import GUILDS
from ..emoji import Emoji
from ..http import urls as module_urls
from ..localization.utils import DEFAULT_LOCALE, get_locale
from ..permission import Permission
from ..permission.permission import PERMISSION_ALL, PERMISSION_MASK_ADMINISTRATOR, PERMISSION_NONE
from ..preconverters import preconvert_bool, preconvert_preinstanced_type, preconvert_snowflake, preconvert_str
from ..role import Role
from ..scheduled_event import ScheduledEvent
from ..sticker import Sticker
from ..user import ClientUserBase, User, VoiceState, ZEROUSER, create_partial_user_from_id
from ..utils import DATETIME_FORMAT_CODE, EMOJI_NAME_RP

from .embedded_activity_state import EmbeddedActivityState
from .emoji_counts import EmojiCounts
from .fields import parse_features, parse_premium_tier, validate_features, validate_premium_tier
from .flags import SystemChannelFlag
from .guild_premium_perks import TIER_MAX as PREMIUM_TIER_MAX, TIERS as PREMIUM_TIERS
from .preinstanced import (
    ContentFilterLevel, GuildFeature, HubType, MFA, MessageNotificationLevel, NsfwLevel, VerificationLevel
)
from .sticker_counts import StickerCounts


VoiceClient = include('VoiceClient')
Client = include('Client')
Stage = include('Stage')
trigger_voice_client_ghost_event = include('trigger_voice_client_ghost_event')

LARGE_GUILD_LIMIT = 250 # can be between 50 and 250

EMOJI_UPDATE_NONE = 0
EMOJI_UPDATE_CREATE = 1
EMOJI_UPDATE_DELETE = 2
EMOJI_UPDATE_EDIT = 3


STICKER_UPDATE_NONE = 0
STICKER_UPDATE_CREATE = 1
STICKER_UPDATE_DELETE = 2
STICKER_UPDATE_EDIT = 3


VOICE_STATE_NONE = 0
VOICE_STATE_JOIN = 1
VOICE_STATE_LEAVE = 2
VOICE_STATE_UPDATE = 3
VOICE_STATE_MOVE = 4

COMMUNITY_FEATURES = frozenset((
    GuildFeature.community,
    GuildFeature.discoverable,
    GuildFeature.public,
))


if CACHE_USER:
    GUILD_USERS_TYPE = dict
else:
    GUILD_USERS_TYPE = WeakValueDictionary


MAX_PRESENCES_DEFAULT = 0
MAX_USERS_DEFAULT = 250000
MAX_VIDEO_CHANNEL_USERS_DEFAULT = 25


def _user_date_sort_key(item):
    """
    Sort key used inside ``Guild.get_users_like_ordered`` and in ``Guild.boosters`` to sort users by a specified date.
    
    Parameters
    ----------
    item : `tuple` ( ``ClientUserBase``, `datetime`)
        The user and it's specific date.
    
    Returns
    -------
    date : `datetime`
    """
    return item[1]


def _emoji_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_emojis_like`` to sort emojis based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Emoji``, `tuple` (`int`, `int`))
        The emoji and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`int`, `int`)
    """
    return item[1]


def _sticker_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_stickers_like`` to sort stickers based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Sticker``, `tuple` (`bool`, `int`, `int`))
        The sticker and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`bool`, `int`, `int`)
    """
    return item[1]


def _strip_emoji_name(name):
    """
    Strips the given emoji name from colon signs.
    
    Parameters
    ----------
    name : `str`
        The name to strip.
    
    Returns
    -------
    name : `str`
    """
    if name.startswith(':'):
        starts_at = 1
    else:
        starts_at = None
    
    if name.endswith(':'):
        ends_at = -1
    else:
        ends_at = None
    
    if (starts_at is not None) or (ends_at is not None):
        name = name[starts_at : ends_at]
    
    return name


# discord does not send `widget_channel_id`, `widget_enabled`, `max_presences`, `max_users` correctly and that is sad.

@export
class Guild(DiscordEntity, immortal = True):
    """
    Represents a Discord guild (or server).
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the guild.
    _boosters : `None`, `list` of ``ClientUserBase`` objects
        Cached slot for the boosters of the guild.
    _embedded_activity_states : `None`, `set` of ``EmbeddedActivityState``
        Embedded activity states to keep them alive in cache.
    _permission_cache : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    afk_channel_id : `int`
        The afk channel's identifier of the guild if it has.
        
        Defaults to `0`.
    afk_timeout : `int`
        The afk timeout at the `afk_channel`. Can be `60`, `300`, `900`, `1800`, `3600` in seconds.
    approximate_online_count : `int`
        The approximate amount of online users at the respective guild. Set as `0` if not yet requested.
    approximate_user_count : `int`
        The approximate amount of users at the respective guild. Set as `0` if not yet requested.
    available : `bool`
        Whether the guild is available.
    banner_hash : `int`
        The guild's banner's hash in `uint128`.
    banner_type : ``IconType``
        The guild's banner's type.
    boost_progress_bar_enabled : `bool`
        Whether the guild has the boost progress bar enabled.
    boost_count : `int`
        The total number of boosts of the guild.
    channels : `dict` of (`int`, ``Channel``) items
        The channels of the guild stored in `channel_id` - `channel` relation.
    clients : `list` of ``Client``
        The loaded clients, who are the member of the guild. If no clients are member of a guild, it is partial.
    content_filter : ``ContentFilterLevel``
        The explicit content filter level of the guild.
    description : `None`, `str`
        Description of the guild. The guild must be a Community guild.
    discovery_splash_hash : `int`
        The guild's discovery splash's hash in `uint128`. The guild must be a discoverable.
    discovery_splash_type : ``IconType``
        The guild's discovery splash's type.
    emojis : `dict` of (`int`, ``Emoji``) items
        The emojis of the guild stored in `emoji_id` - `emoji` relation.
    features : `None`, `tuple` of ``GuildFeature``
        The guild's features.
    hub_type : ``HubType``
        The guild's hub type. Only applicable for hub guilds.
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
    icon_type : ``IconType``
        The guild's icon's type.
    invite_splash_hash : `int`
        The guild's invite splash's hash in `uint128`. The guild must have `INVITE_SPLASH` feature.
    invite_splash_type : ``IconType``
        The guild's invite splash's type.
    is_large : `bool`
        Whether the guild is considered as a large one.
    max_presences : `int`
        The maximal amount of presences for the guild. If not received defaults to `0`. Only applicable for very large
        guilds.
    max_users : `int`
        The maximal amount of users for the guild.
    max_video_channel_users : `int`
        The maximal amount of users in a video channel(?).
    message_notification : ``MessageNotificationLevel``
        The message notification level of the guild.
    mfa : ``MFA``
        The required Multi-factor authentication level for the guild.
    name : `str`
        The name of the guild.
    nsfw_level : `bool`
        The guild's nsfw level.
    owner_id : `int`
        The guild's owner's id. Defaults to `0`.
    preferred_locale : ``Locale``
        The preferred language of the guild. The guild must be a Community guild, defaults to `'en-US'`.
    premium_tier : `int`
        The premium tier of the guild. More boosters = higher tier.
    public_updates_channel_id : `int`
        The channel's identifier where the guild's public updates should go. The guild must be a `community` guild.
        
        Defaults to `0`.
    roles : `dict` of (`int`, ``Role``) items
        The roles of the guild stored in `role_id` - `role` relation.
    rules_channel_id : `int`
        The channel's identifier where the rules of a public guild's should be.
        
        The guild must be a `community` guild.
    stages : `None`, `dict` of (`int`, ``Stage``) items
        Active stages of the guild. Defaults to `None` if would be empty.
    stickers : `dict` of (`int`, ``Sticker``) items
        Stickers of th guild.
    system_channel_id : `int`
        The channel's identifier where the system messages are sent.
        
        Defaults to `0`.
    scheduled_events : `dict` of (`int`, ``ScheduledEvent``) items
        The scheduled events of the guild.
    system_channel_flags : ``SystemChannelFlag``
        Describe which type of messages are sent automatically to the system channel.
    threads : `dict` of (`int`, ``Channel``)
        Thread channels of the guild.
    user_count : `int`
        The amount of users at the guild.
    users : `dict`, ``WeakValueDictionary`` of (`int`, ``ClientUserBase``) items
        The users at the guild stored within `user_id` - `user` relation.
    vanity_code : `None`, `str`
        The guild's vanity invite's code if it has.
    verification_level : ``VerificationLevel``
        The minimal verification needed to join to guild.
    voice_states : `dict` of (`int`, ``VoiceState``) items
        Each user at a voice channel is represented by a ``VoiceState`` object. Voice state are stored in
        `respective user's id` - `voice state` relation.
    widget_channel_id : `int`
        The channel's identifier for which the guild's widget is for.
        
        Defaults to `0`.
    widget_enabled : `bool`
        Whether the guild's widget is enabled. Linked to ``.widget_channel``.
    
    Notes
    -----
    When a guild is loaded first time, some of it's attributes might not reflect their real value. These are the
    following:
    - ``.max_presences``
    - ``.max_users``
    - ``.widget_channel_id``
    - ``.widget_enabled``
    """
    __slots__ = (
        '_boosters', '_embedded_activity_states', '_permission_cache', 'afk_channel_id', 'afk_timeout',
        'approximate_online_count', 'approximate_user_count', 'available', 'boost_progress_bar_enabled',
        'boost_count', 'channels', 'clients', 'content_filter', 'description', 'emojis', 'features', 'hub_type',
        'is_large', 'max_presences', 'max_users', 'max_video_channel_users', 'message_notification', 'mfa', 'name',
        'nsfw_level', 'owner_id', 'preferred_locale', 'premium_tier', 'public_updates_channel_id', 'roles',
        'rules_channel_id', 'scheduled_events', 'stages', 'stickers', 'system_channel_flags', 'system_channel_id',
        'threads', 'user_count', 'users', 'vanity_code', 'verification_level', 'voice_states', 'widget_channel_id',
        'widget_enabled'
    )
    
    banner = IconSlot(
        'banner',
        'banner',
        module_urls.guild_banner_url,
        module_urls.guild_banner_url_as,
    )
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.guild_icon_url,
        module_urls.guild_icon_url_as,
    )
    invite_splash = IconSlot(
        'invite_splash',
        'splash',
        module_urls.guild_invite_splash_url,
        module_urls.guild_invite_splash_url_as,
    )
    discovery_splash = IconSlot(
        'discovery_splash',
        'discovery_splash',
        module_urls.guild_discovery_splash_url,
        module_urls.guild_discovery_splash_url_as,
    )
    
    
    def __new__(cls, data, client):
        """
        `.__new__` will be repurposed. Please use `.from_data` instead.
        """
        warnings.warn(
            f'`{cls.__name__}.__new__` will be repurposed. Please use `.from_data` instead.',
            FutureWarning,
            stacklevel = 2,
        )
        return cls.from_data(data, client)
    
    
    @classmethod
    def from_data(cls, data, client = None):
        """
        Tries to find the guild from the already existing ones. If it can not find, creates a new one. If the found
        guild is partial (or freshly created), sets it's attributes from the given `data`. If the the guild is not
        added to the client's guild profiles yet, adds it, and the client to the guilds' `.clients` as well.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild data.
        client : `None`, ``Client`` = `None`, Optional
            The client who received the guild's data.
        
        Returns
        -------
        guild : ``Guild``
        """
        guild_id = int(data['id'])
        
        try:
            self = GUILDS[guild_id]
            update = (not self.clients)
        except KeyError:
            self = object.__new__(cls)
            GUILDS[guild_id] = self
            self.id = guild_id
            
            self.clients = []
            self.users = GUILD_USERS_TYPE()
            self.emojis = {}
            self.voice_states = {}
            self.roles = {}
            self.channels = {}
            self.features = []
            self.threads = {}
            self.stickers = {}
            self.scheduled_events = {}
            self._permission_cache = None
            self._boosters = None
            self.user_count = 1
            self.approximate_online_count = 0
            self.approximate_user_count = 0
            self.stages = None
            self._embedded_activity_states = None
            
            update = True
        
        self.available = (not data.get('unavailable', False))
        
        if update:
            try:
                user_count = data['member_count']
            except KeyError:
                pass
            else:
                self.user_count = user_count
            
            self.boost_count = 0
            
            try:
                is_large = data['large']
            except KeyError:
                is_large = (self.user_count >= LARGE_GUILD_LIMIT)
            
            self.is_large = is_large
            
            try:
                role_datas = data['roles']
            except KeyError:
                pass
            else:
                for role_data in role_datas:
                    Role.from_data(role_data, guild_id)
            
            try:
                emoji_datas = data['emojis']
            except KeyError:
                pass
            else:
                emojis = self.emojis
                for emoji_data in emoji_datas:
                    emoji = Emoji(emoji_data, guild_id)
                    emojis[emoji.id] = emoji
            
            try:
                sticker_datas = data['stickers']
            except KeyError:
                pass
            else:
                stickers = self.stickers
                for sticker_data in sticker_datas:
                    sticker = Sticker(sticker_data)
                    stickers[sticker.id] = sticker
            
            try:
                channel_datas = data['channels']
            except KeyError:
                pass
            else:
                for channel_data in channel_datas:
                    Channel.from_data(channel_data, client, guild_id)
            
            self._update_attributes(data)
            
            if CACHE_PRESENCE:
                try:
                    guild_profile_datas = data['members']
                except KeyError:
                    pass
                else:
                    for guild_profile_data in guild_profile_datas:
                        User.from_data(guild_profile_data['user'], guild_profile_data, guild_id)
                
                # If user caching is disabled, then presence caching is too.
                try:
                    presence_data = data['presences']
                except KeyError:
                    pass
                else:
                    self._apply_presences(presence_data)
            
            try:
                voice_state_datas = data['voice_states']
            except KeyError:
                pass
            else:
                for voice_state_data in voice_state_datas:
                    VoiceState(voice_state_data, self.id)
            
            try:
                thread_datas = data['threads']
            except KeyError:
                pass
            else:
                for thread_data in thread_datas:
                    Channel.from_data(thread_data, client, guild_id)
            
            try:
                scheduled_event_datas = data['guild_scheduled_events']
            except KeyError:
                pass
            else:
                for scheduled_event_data in scheduled_event_datas:
                    ScheduledEvent(scheduled_event_data)
            
            stage_datas = data.get('stage_instances', None)
            if (stage_datas is not None):
                for stage_data in stage_datas:
                    Stage(stage_data)
            
            try:
                embedded_activity_state_datas = data['embedded_activities']
            except KeyError:
                pass
            else:
                for embedded_activity_state_data in embedded_activity_state_datas:
                    EmbeddedActivityState(embedded_activity_state_data, guild_id)
            
        
        if (not CACHE_PRESENCE):
            # we get information about the client here
            try:
                user_datas = data['members']
            except KeyError:
                pass
            else:
                for user_data in user_datas:
                    User._bypass_no_cache(user_data, self)
        
        if client not in self.clients:
            try:
                ghost_state = self.voice_states[client.id]
            except KeyError:
                pass
            else:
                trigger_voice_client_ghost_event(client, ghost_state)
            
            self.clients.append(client)
            client.guilds.add(self)
        
        return self
    
    
    @classmethod
    def precreate(cls, guild_id, **kwargs):
        """
        Precreates the guild with the given parameters. Precreated guilds are picked up when a guild's data is received
        with the same id.
        
        First tries to find whether a guild exists with the given id. If it does and it is partial, updates it with the
        given parameters, else it creates a new one.
        
        Parameters
        ----------
        guild_id : `snowflake`
            The guild's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the guild.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The guild's ``.name``.
        
        banner : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's banner.
            
            > Mutually exclusive with `banner_type` and `banner_hash` parameters.
        
        banner_type : ``IconType``, Optional (Keyword only)
            The guild's banner's type.
            
            > Mutually exclusive with the `banner` parameter.
        
        banner_hash : `int`, Optional (Keyword only)
            The guild's banner's hash.
            
            > Mutually exclusive with the `banner` parameter.
        
        boost_progress_bar_enabled : `bool`, Optional (Keyword only)
            Whether the guild has the boost progress bar enabled.
        
        invite_splash : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's invite splash.
            
            > Mutually exclusive with the `invite_splash_type` and `invite_splash_hash` parameters.
        
        invite_splash_type : `IconType``, Optional (Keyword only)
            The guild's invite splash's type.
            
            > Mutually exclusive with the `invite_splash` parameter.
        
        invite_splash_hash : `int`, Optional (Keyword only)
            The guild's invite splash's hash.
            
            > Mutually exclusive with the `invite_splash` parameter.
        
        discovery_splash : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's discovery splash.
            
            Mutually exclusive with the `discovery_splash_type` and  `discovery_splash_hash` parameters.
        
        discovery_splash_type : `IconType``, Optional (Keyword only)
            The guild's discovery splash's type.
            
            > Mutually exclusive with the `discovery_splash` parameter.
        
        discovery_splash_hash : `int`, Optional (Keyword only)
            The guild's discovery splash's hash.
            
            > Mutually exclusive with the `discovery_splash` parameter.
            
        features : `None`, `tuple` of `(`int`, `GuildFeature``), Optional (Keyword only)
            The guild's features.
            
        icon : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's icon.
            
            > Mutually exclusive with `icon_type` and `icon_hash`.
        
        icon_type : ``IconType``, Optional (Keyword only)
            The guild's icon's type.
            
            > Mutually exclusive with `icon`.
        
        icon_hash : `int`, Optional (Keyword only)
            The guild's icon's hash.
            
            > Mutually exclusive with `icon`.
        
        nsfw_level : ``NsfwLevel``, Optional (Keyword only)
            The nsfw level of the guild.
            
        premium_tier : `int`, Optional (Keyword only)
            The premium tier of the guild.
        
        Returns
        -------
        guild : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            - If an parameter's type is good, but it's value is unacceptable.
        """
        guild_id = preconvert_snowflake(guild_id, 'guild_id')
        
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
            cls.banner.preconvert(kwargs, processable)
            cls.invite_splash.preconvert(kwargs, processable)
            cls.discovery_splash.preconvert(kwargs, processable)
            
            for attribute_name, attribute_type in (
                ('nsfw_level', NsfwLevel),
            ):
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    pass
                else:
                    attribute_value = preconvert_preinstanced_type(attribute_value, attribute_name, attribute_type)
                    processable.append((attribute_name, attribute_value))
            
            try:
                boost_progress_bar_enabled = kwargs.pop('boost_progress_bar_enabled')
            except KeyError:
                pass
            else:
                boost_progress_bar_enabled = preconvert_bool(boost_progress_bar_enabled, 'boost_progress_bar_enabled')
                processable.append(('boost_progress_bar_enabled', boost_progress_bar_enabled))
            
            for attribute_name, field_validator in (
                ('features', validate_features),
                ('premium_tier', validate_premium_tier),
            ):
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    continue
                
                attribute_value = field_validator(attribute_value)
                processable.append((attribute_name, attribute_value))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
            
        else:
            processable = None
        
        try:
            self = GUILDS[guild_id]
        except KeyError:
            self = cls._create_empty(guild_id)
            GUILDS[guild_id] = self
        else:
            if self.clients:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, guild_id):
        """
        Creates a guild with default parameters set.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's identifier.
        
        Returns
        -------
        self : ``Guild``
        """
        self = object.__new__(cls)
        self._boosters = None
        self._permission_cache = None
        self.afk_channel_id = 0
        self.afk_timeout = 0
        self.channels = {}
        self.roles = {}
        self.available = False
        self.banner_hash = 0
        self.banner_type = ICON_TYPE_NONE
        self.boost_progress_bar_enabled = False
        self.boost_count = 0
        self.clients = []
        self.content_filter = ContentFilterLevel.disabled
        self.description = None
        self.discovery_splash_hash = 0
        self.discovery_splash_type = ICON_TYPE_NONE
        self.emojis = {}
        self.features = []
        self.hub_type = HubType.none
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        self.id = guild_id
        self.is_large = False
        self.max_presences = MAX_PRESENCES_DEFAULT
        self.max_users = MAX_USERS_DEFAULT
        self.max_video_channel_users = MAX_VIDEO_CHANNEL_USERS_DEFAULT
        self.message_notification = MessageNotificationLevel.only_mentions
        self.mfa = MFA.none
        self.name = ''
        self.owner_id = 0
        self.preferred_locale = DEFAULT_LOCALE
        self.premium_tier = 0
        self.public_updates_channel_id = 0
        self.rules_channel_id = 0
        self.invite_splash_hash = 0
        self.invite_splash_type = ICON_TYPE_NONE
        self.system_channel_id = 0
        self.system_channel_flags = SystemChannelFlag.NONE
        self.approximate_user_count = 1
        self.users = GUILD_USERS_TYPE()
        self.vanity_code = None
        self.verification_level = VerificationLevel.none
        self.voice_states = {}
        self.widget_channel_id = 0
        self.widget_enabled = False
        self.user_count = 0
        self.approximate_online_count = 0
        self.approximate_user_count = 0
        self.threads = {}
        self.stages = None
        self.nsfw_level = NsfwLevel.none
        self.stickers = {}
        self.scheduled_events = {}
        self._embedded_activity_states = None
        return self
    
    
    def __repr__(self):
        """Returns the guild's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id = ', repr(self.id),
        ]
        
        if self.partial:
            repr_parts.append(' (partial)')
        
        name = self.name
        if name:
            repr_parts.append(', name = ')
            repr_parts.append(repr(name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __del__(self):
        """Clears up the guild profile references of the guild."""
        users = self.users
        if users:
            guild_id = self.id
            for user in users.values():
                try:
                    user.guild_profiles[guild_id]
                except KeyError:
                    pass
            
            users.clear()
    
    
    def __format__(self, code):
        """
        Formats the guild in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        guild : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import Guild, now_as_id
        >>> guild = Guild.precreate(now_as_id(), name='GrassGrass')
        >>> guild
        <Guild name='GrassGrass', id=713718885970345984 (partial)>
        >>> # no code stands for `guild.name`
        >>> f'{guild}'
        'GrassGrass'
        >>> # 'c' stands for created at.
        >>> f'{guild:c}'
        '2020-05-23 11:44:02'
        ```
        """
        if not code:
            return self.name
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}.'
        )
    
    
    widget_url = module_urls.guild_widget_url
    
    def _delete(self, client):
        """
        When a client leaves (gets kicked or banned) from a guild, this method is called. If the guild loses it's last
        active client, then the it's references are cleared.
        
        Parameters
        ----------
        client : ``Client``
            The client, who left the guild.
        """
        clients = self.clients
        
        try:
            clients.remove(client)
        except ValueError:
            pass
        
        client.guilds.discard(self)
        
        if clients:
            return
        
        self.threads.clear()
        self.channels.clear()
        self.emojis.clear()
        self.stickers.clear()
        self.voice_states.clear()
        
        users = self.users
        guild_id = self.id
        for user in users.values():
            if isinstance(user, User):
                try:
                    del user.guild_profiles[guild_id]
                except KeyError:
                    pass
        
        users.clear()
        self.scheduled_events.clear()
        
        self.roles.clear()
        self._boosters = None
    
    
    def _update_voice_state(self, data, user):
        """
        Called by dispatch event. Updates the voice state of the represented user by `user_id` with the given `data`.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        user : ``ClientUserBase``
            The respective user.
        
        Yields
        -------
        action : `int`
            The respective action.
            
            Can be one of the following:
            
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | VOICE_STATE_NONE      | 0     |
            +-----------------------+-------+
            | VOICE_STATE_JOIN      | 1     |
            +-----------------------+-------+
            | VOICE_STATE_LEAVE     | 2     |
            +-----------------------+-------+
            | VOICE_STATE_UPDATE    | 3     |
            +-----------------------+-------+
            | VOICE_STATE_MOVE      | 4     |
            +-----------------------+-------+
        
        voice_state : `None`, ``VoiceState``
            The user's respective voice state.
            
            Will be returned as `None` if action is `VOICE_STATE_NONE`.
        
        old_attributes / old_channel_id : `None` or (`dict` of (`str`, `Any`) items / `int`)
            If `action` is `VOICE_STATE_UPDATE`, then `old_attributes` is returned as a `dict` containing the changed
            attributes in `attribute-name` - `old-value` relation. All item at the returned dictionary is optional.
            
            +---------------+-------------------+
            | Keys          | Values            |
            +===============+===================+
            | deaf          | `str`             |
            +---------------+-------------------+
            | mute          | `bool`            |
            +---------------+-------------------+
            | self_deaf     | `bool`            |
            +---------------+-------------------+
            | self_mute     | `bool`            |
            +---------------+-------------------+
            | self_stream   | `bool`            |
            +---------------+-------------------+
            | self_video    | `bool`            |
            +---------------+-------------------+
            
            If `action` is `VOICE_STATE_LEAVE`, `VOICE_STATE_MOVE`, then the old channel's identifier is returned.
        """
        try:
            voice_state = self.voice_states[user.id]
        except KeyError:
            voice_state = VoiceState(data, self.id)
            if (voice_state is not None):
                voice_state._set_cache_user(user)
                yield VOICE_STATE_JOIN, voice_state, None
        
        else:
            voice_state._set_cache_user(user)
            old_attributes = voice_state._difference_update_attributes(data)
            if old_attributes:
                yield VOICE_STATE_UPDATE, voice_state, old_attributes
            
            old_channel_id, new_channel_id = voice_state._update_channel(data)
            if new_channel_id == 0:
                yield VOICE_STATE_LEAVE, voice_state, old_channel_id
            elif old_channel_id != new_channel_id:
                yield VOICE_STATE_MOVE, voice_state, old_channel_id
    
    
    def _update_voice_state_restricted(self, data, user):
        """
        Called by dispatch event. Updates the voice state of the represented user by `user_id` with the given `data`.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        user : ``ClientUserBase``
            The respective user.
        """
        try:
            voice_state = self.voice_states[user.id]
        except KeyError:
            voice_state = VoiceState(data, self.id)
            if (voice_state is not None):
                voice_state._set_cache_user(user)
        else:
            voice_state._set_cache_user(user)
            voice_state._update_channel(data)
            voice_state._update_attributes(data)
    
    
    @property
    def text_channels(self):
        """
        Returns the text channels of the guild. Announcement channels are not included.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_guild_text()]
    
    
    @property
    def voice_channels(self):
        """
        Returns the voice channels of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_guild_voice()]
    
    
    @property
    def category_channels(self):
        """
        Returns the category channels of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_guild_category()]
    
    
    @property
    def announcement_channels(self):
        """
        Returns the announcement channels of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_guild_announcements()]
    
    
    @property
    def store_channels(self):
        """
        Returns the store channels of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_guild_store()]
    
    
    @property
    def thread_channels(self):
        """
        Returns the thread channels of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return list(self.threads.values())
    
    
    @property
    def stage_channels(self):
        """
        Returns the stage channels of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_guild_stage()]
    
    
    @property
    def forum_channels(self):
        """
        Returns the forum channels of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_guild_forum()]
    
    
    @property
    def messageable_channels(self):
        """
        Returns the messageable channels (excluding threads) of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_in_group_guild_textual()]
    
    
    @property
    def connectable_channels(self):
        """
        Returns the connectable channels of the guild.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return [channel for channel in self.channels.values() if channel.is_in_group_guild_connectable()]
    
    
    @property
    def default_role(self):
        """
        Returns the default role of the guild (`@everyone`).
        
        Might return `None` at the case of partial guilds.
        
        Returns
        -------
        default_role : `None`, `Role``
        """
        return self.roles.get(self.id, None)
    
    
    @property
    def partial(self):
        """
        Returns whether the guild is partial.
        
        A guild is partial, if it has no active clients.
        
        Returns
        -------
        partial : `bool`
        """
        return (not self.clients)
    
    
    def _sync(self, data):
        """
        Syncs the guild with the requested guild data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild data.
        """
        try:
            is_large = data['large']
        except KeyError:
            is_large = (self.approximate_user_count >= LARGE_GUILD_LIMIT)
        self.is_large = is_large
        
        self._update_attributes(data)
        
        try:
            role_datas = data['roles']
        except KeyError:
            pass
        else:
            self._sync_roles(role_datas)
        
        try:
            emoji_datas = data['emojis']
        except KeyError:
            pass
        else:
            self._sync_emojis(emoji_datas)

##        # sadly we don't get voice states with guild_get
##        try:
##            voice_state_datas = data['voice_states']
##        except KeyError:
##            self.voice_states.clear()
##        else:
##            old_voice_states = self.voice_states
##            new_voice_states = self.voice_states = {}
##
##            for voice_state_data in voice_state_datas:
##                user=create_partial_user_from_id(int(voice_state_data['user_id']))
##
##                channel_id = voice_state_data.get('channel_id', None)
##                if channel_id is None:
##                    continue
##                channel = self.channels[int(channel_id)]
##
##                try:
##                    voice_state = old_voice_states[user.id]
##                except KeyError:
##                    new_voice_states[user.id] = VoiceState(voice_state_data, channel)
##                    continue
##
##                voice_state._update_attributes(voice_state_data, channel)
##                new_voice_states[user.id] = voice_state
    
    def _apply_presences(self, data):
        """
        Applies the presences to the guild user's. Called when the guild is created or if a user chunk is received if
        presence caching is enabled.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Guild's users' presences' data.
        """
        users = self.users
        for presence_data in data:
            user_id = int(presence_data['user']['id'])
            try:
                user = users[user_id]
            except KeyError:
                pass
            else:
                user._update_presence(presence_data)
    
    
    def _sync_channels(self, data):
        """
        Syncs the guild's channels with the given guild channel datas.
        
        Parameters
        ----------
        data `list` of (`dict` of (`str`, `Any`) items)
            Received guild channel datas.
        """
        channels = self.channels
        old_ids = set(channels)
        
        for channel_data in data:
            channel = Channel.from_data(channel_data, None, self.id)
            channel_id = channel.id
            try:
                old_ids.remove(channel_id)
            except KeyError:
                pass
            else:
                # old channel -> update
                channel._update_attributes(channel_data)
        
        # deleting
        for channel_id in old_ids:
            channels[channel_id]._delete(None)
    
    
    def _sync_roles(self, data):
        """
        Syncs the guild's roles with the given guild role datas.
        
        Parameters
        ----------
        data `list` of (`dict` of (`str`, `Any`) items)
            Received guild role datas.
        """
        roles = self.roles
        old_ids = set(roles)
        # every new role can cause mass switchings at the role orders, can it mess up the order tho?
        for role_data in data:
            role = Role.from_data(role_data, self.id)
            try:
                old_ids.remove(role.id)
                role._update_attributes(role_data)
            except KeyError:
                pass
        
        for role_id in old_ids:
            roles[role_id]._delete()
    
    
    def get_user(self, name, default = None):
        """
        Tries to find the a user with the given name at the guild. Returns the first matched one.
        
        The search order is the following:
        - `full_name`
        - `name`
        - `nick`
        
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
        name_length = len(name)
        if name_length < 1:
            return default
        
        users = self.users
        
        if name_length > 6:
            if name_length > 37:
                return default
            
            if name[-5] == '#':
                try:
                    discriminator = int(name[-4:])
                except ValueError:
                    pass
                else:
                    stripped_name = name[:-5]
                    for user in users.values():
                        if (user.discriminator == discriminator) and (user.name == stripped_name):
                            return user
        
        if name_length > 32:
            return default
        
        for user in users.values():
            if user.name == name:
                return user
        
        guild_id = self.id
        for user in users.values():
            nick = user.guild_profiles[guild_id].nick
            if nick is None:
                continue
            
            if nick == name:
                return user
        
        return default
    
    
    def get_user_like(self, name, default = None):
        """
        Searches a user, who's name or nick starts with the given string and returns the first find. Also matches full
        name.
        
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
        name_length = len(name)
        if name_length < 1:
            return default
        
        users = self.users
        
        if name_length > 6:
            if name_length > 37:
                return default
            
            if name[-5] == '#':
                try:
                    discriminator = int(name[-4:])
                except ValueError:
                    pass
                else:
                    stripped_name = name[:-5]
                    for user in users.values():
                        if (user.discriminator == discriminator) and (user.name == stripped_name):
                            return user
        
        if name_length > 32:
            return default
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        guild_id = self.id
        for user in self.users.values():
            if (pattern.search(user.name) is not None):
                return user
            
            nick = user.guild_profiles[guild_id].nick
            
            if nick is None:
                continue
            
            if pattern.search(nick) is None:
                continue
            
            return user
        
        return default
    
    
    def get_users_like(self, name):
        """
        Searches the users, who's name or nick start with the given string.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        result = []
        
        name_length = len(name)
        if name_length < 0:
            return result
        
        users = self.users
        
        if name_length > 6:
            if name_length > 37:
                return result
            
            if name[-5] == '#':
                try:
                    discriminator = int(name[-4:])
                except ValueError:
                    pass
                else:
                    stripped_name = name[:-5]
                    for user in users.values():
                        if (user.discriminator == discriminator) and (user.name == stripped_name):
                            result.append(user)
                            break
        
        if name_length > 32:
            return result
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        guild_id = self.id
        for user in self.users.values():
            if pattern.search(user.name) is None:
                nick = user.guild_profiles[guild_id].nick
                if nick is None:
                    continue
                
                if pattern.search(nick) is None:
                    continue
            
            result.append(user)
        
        return result
    
    
    def get_users_like_ordered(self, name):
        """
        Searches the users, who's name or nick start with the given string. At the orders them at the same ways, as
        Discord orders them when requesting guild member chunk.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of ``ClientUserBase`` objects
        """
        to_sort = []
        if (not 1 < len(name) < 33):
            return to_sort
        
        now_date_time = None
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        guild_id = self.id
        for user in self.users.values():
            profile = user.guild_profiles[guild_id]
            if pattern.search(user.name) is None:
                nick = profile.nick
                if nick is None:
                    continue
                
                if pattern.search(nick) is None:
                    continue
            
            joined_at = profile.joined_at
            
            if joined_at is None:
                # Instead of defaulting to `user.created_at` use the current date
                if now_date_time is None:
                    now_date_time = datetime.utcnow()
                
                joined_at = now_date_time
            
            
            to_sort.append((user, joined_at))
        
        if not to_sort:
            return to_sort
        
        to_sort.sort(key = _user_date_sort_key)
        return [item[0] for item in to_sort]
    
    
    def get_emoji(self, name, default = None):
        """
        Searches an emoji of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        emoji : ``Emoji``, `default`
        """
        parsed = EMOJI_NAME_RP.fullmatch(name)
        if (parsed is not None):
            name = parsed.group(1)
            for emoji in self.emojis.values():
                if emoji.name == name:
                    return emoji
        
        return default
    
    
    def get_emoji_like(self, name, default = None):
        """
        Searches an emoji of the guild, whats name starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        emoji : ``Emoji``, `default`
        """
        name = _strip_emoji_name(name)
        
        emoji_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        accurate_emoji = default
        accurate_match_key = (100, 100)
        
        for emoji in self.emojis.values():
            emoji_name = emoji.name
            parsed = emoji_name_pattern.search(emoji_name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            match_rate = (match_length, match_length)
            if accurate_match_key < match_rate:
                continue
            
            accurate_emoji = emoji
            accurate_match_key = match_rate
        
        return accurate_emoji
    
    
    def get_emojis_like(self, name):
        """
        Searches the emojis, what's name match the given value.
        
        The returned value is ordered by match rate.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        emojis : `list` of ``Emoji``
        """
        name = _strip_emoji_name(name)
        
        emoji_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        to_sort = []
        
        for emoji in self.emojis.values():
            emoji_name = emoji.name
            parsed = emoji_name_pattern.search(emoji_name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            to_sort.append((emoji, (match_length, match_start)))
        
        if not to_sort:
            return to_sort
        
        to_sort.sort(key = _emoji_match_sort_key)
        return [item[0] for item in to_sort]
    
    
    def get_sticker(self, name, default = None):
        """
        Searches a sticker of the guild, what's name equals to the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        sticker : ``Sticker``, `default`
        """
        for sticker in self.stickers.values():
            if sticker.name == name:
                return sticker
        
        return default
    
    
    def get_sticker_like(self, name, default = None):
        """
        Searches a sticker of the guild, what's name or a tag starts with the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        sticker : ``Sticker``, `default`
        """
        sticker_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        accurate_sticker = default
        matching_names_only = False
        accurate_match_key = (100, 100)
        
        for sticker in self.stickers.values():
            sticker_name = sticker.name
            
            parsed = sticker_name_pattern.search(sticker_name)
            if (parsed is not None):
            
                match_start = parsed.start()
                match_length = parsed.end() - match_start
                
                match_rate = (match_length, match_length)
                if accurate_match_key > match_rate:
                    accurate_sticker = sticker
                    accurate_match_key = match_rate
                    matching_names_only = True
                    continue
            
            if not matching_names_only:
                sticker_tags = sticker.tags
                if (sticker_tags is not None):
                    for sticker_tag in sticker_tags:
                        
                        parsed = sticker_name_pattern.search(sticker_tag)
                        if (parsed is not None):
                            
                            match_start = parsed.start()
                            match_length = parsed.end() - match_start
                            
                            match_rate = (match_length, match_length)
                            if accurate_match_key > match_rate:
                                accurate_sticker = sticker
                                accurate_match_key = match_rate
                                continue
        
        return accurate_sticker
    
    
    def get_stickers_like(self, name):
        """
        Searches the stickers, what's name and tags matches the given value.
        
        The returned value is ordered by match rate.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        stickers : `list` of ``Sticker``
        """
        sticker_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        matches = {}
        
        for sticker in self.stickers.values():
            sticker_name = sticker.name
            
            parsed = sticker_name_pattern.search(sticker_name)
            if (parsed is not None):
            
                match_start = parsed.start()
                match_length = parsed.end() - match_start
                
                match_rate = (False, match_length, match_length)
                
                matches[sticker] = match_rate
                continue
            
            sticker_tags = sticker.tags
            if (sticker_tags is not None):
                for sticker_tag in sticker_tags:
                    
                    parsed = sticker_name_pattern.search(sticker_tag)
                    if (parsed is not None):
                        
                        match_start = parsed.start()
                        match_length = parsed.end() - match_start
                        
                        match_rate = (True, match_length, match_length)
                        
                        try:
                            accurate_match_rate = matches[sticker]
                        except KeyError:
                            pass
                        else:
                            if accurate_match_rate <= match_rate:
                                continue
                                
                        matches[sticker] = match_rate
                        continue
        
        
        if not matches:
            return []
        
        return [item[0] for item in sorted(matches.items(), key = _sticker_match_sort_key)]
    
    
    def get_channel(self, name, default = None):
        """
        Searches a channel of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no channel was found. Defaults to `None`.
        
        Returns
        -------
        channel : ``Channel``, `default`
        """
        if name.startswith('#'):
            name = name[1:]
        
        for channel in self.channels.values():
            if channel.display_name == name:
                return channel
        
        for channel in self.channels.values():
            if channel.name == name:
                return channel
        
        return default
    
    
    def get_channel_like(self, name, default = None, type_checker = None):
        """
        Searches a channel of the guild, whats name starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no channel was found. Defaults to `None`.
        
        Returns
        -------
        channel : ``Channel``, `default`
        """
        if isinstance(type_checker, type):
            type_checker = None
        
        if name.startswith('#'):
            name = name[1:]
        
        target_name_length = len(name)
        if (target_name_length < 2) or (target_name_length > 100):
            return default
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        
        accurate_channel = default
        accurate_name_length = 101
        
        for channel in self.channels.values():
            if (type_checker is not None) and (not type_checker(channel)):
                continue
            
            channel_name = channel.name
            name_length = len(channel_name)
            if name_length > accurate_name_length:
                continue
            
            if pattern.search(channel_name) is None:
                continue

            if name_length < accurate_name_length:
                accurate_channel = channel
                accurate_name_length = name_length
            
            # Compare with display name
            if (name_length == target_name_length) and (name == channel.display_name):
                return channel
            
            continue
        
        return accurate_channel
    
    
    def get_role(self, name, default = None):
        """
        Searches a role of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no role was found. Defaults to `None`.
        
        Returns
        -------
        role : ``Role``, `default`
        """
        for role in self.roles.values():
            if role.name == name:
                return role
        
        return default
    
    
    def get_role_like(self, name, default = None):
        """
        Searches a role of the guild, whats name starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any` = `None`, Optional
            The value what is returned when no role was found. Defaults to `None`.
        
        Returns
        -------
        role : ``Role``, `default`
        """
        target_name_length = len(name)
        if (target_name_length < 2) or (target_name_length > 32):
            return default
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        
        accurate_role = default
        accurate_name_length = 33
        
        for role in self.roles.values():
            role_name = role.name
            name_length = len(role_name)
            if name_length > accurate_name_length:
                continue
            
            if pattern.search(role_name) is None:
                continue
            
            if name_length < accurate_name_length:
                accurate_role = role
                accurate_name_length = name_length
            
            if (name_length == target_name_length) and (name == role_name):
                return role
            
            continue
        
        return accurate_role
    
    
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the guild.
        
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
        guild_id = self.id
        if not isinstance(user, ClientUserBase):
            if user.channel_id in self.channels:
                role_everyone = self.roles.get(guild_id, None)
                if role_everyone is None:
                    permissions = PERMISSION_NONE
                else:
                    permissions = role_everyone.permissions
                
                return permissions
            else:
                return PERMISSION_NONE
        
        if user.id == self.owner_id:
            return PERMISSION_ALL
        
        role_everyone = self.roles.get(guild_id, None)
        if role_everyone is None:
            permissions = 0
        else:
            permissions = role_everyone.permissions
        
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            return PERMISSION_NONE
        
        roles = guild_profile.roles
        if (roles is not None):
            for role in roles:
                permissions |= role.permissions
        
        if permissions & PERMISSION_MASK_ADMINISTRATOR:
            return PERMISSION_ALL
        
        return Permission(permissions)
    
    
    def cached_permissions_for(self, user):
        """
        Returns the permissions for the given user at the guild. If the user's permissions are not cached, calculates
        and stores them first.
        
        Parameters
        ----------
        user : ``UserBase``
            The user to calculate it's permissions of.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
        
        Notes
        -----
        Mainly designed for getting clients' permissions and stores only their as well. Do not caches other user's
        permissions.
        """
        if not isinstance(user, Client):
            return self.permissions_for(user)
        
        permission_cache = self._permission_cache
        if permission_cache is None:
            self._permission_cache = permission_cache = {}
        else:
            try:
                return permission_cache[user.id]
            except KeyError:
                pass
        
        permissions = self.permissions_for(user)
        permission_cache[user.id] = permissions
        return permissions
    
    
    def permissions_for_roles(self, *roles):
        """
        Returns the permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        """
        default_role = self.roles.get(self.id, None)
        if default_role is None:
            permissions = 0
        else:
            permissions = default_role.permissions
        
        roles = sorted(roles)
        
        for role in roles:
            if role.guild is self:
                permissions |= role.permissions
        
        if permissions & PERMISSION_MASK_ADMINISTRATOR:
            return PERMISSION_ALL
        
        return Permission(permissions)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the guild and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-------------------------------+-------------------------------+
        | Keys                          | Values                        |
        +===============================+===============================+
        | afk_channel_id                | `int`                         |
        +-------------------------------+-------------------------------+
        | afk_timeout                   | `int`                         |
        +-------------------------------+-------------------------------+
        | available                     | `bool`                        |
        +-------------------------------+-------------------------------+
        | banner                        | ``Icon``                      |
        +-------------------------------+-------------------------------+
        | boost_progress_bar_enabled    | `bool`                        |
        +-------------------------------+-------------------------------+
        | boost_count                   | `int`                         |
        +-------------------------------+-------------------------------+
        | content_filter                | ``ContentFilterLevel``        |
        +-------------------------------+-------------------------------+
        | description                   | `None`, `str`                 |
        +-------------------------------+-------------------------------+
        | discovery_splash              | ``Icon``                      |
        +-------------------------------+-------------------------------+
        | features                      | `list` of ``GuildFeature``    |
        +-------------------------------+-------------------------------+
        | hub_type                      | ``HubType``                   |
        +-------------------------------+-------------------------------+
        | icon                          | ``Icon``                      |
        +-------------------------------+-------------------------------+
        | invite_splash                 | ``Icon``                      |
        +-------------------------------+-------------------------------+
        | max_presences                 | `int`                         |
        +-------------------------------+-------------------------------+
        | max_users                     | `int`                         |
        +-------------------------------+-------------------------------+
        | max_video_channel_users       | `int`                         |
        +-------------------------------+-------------------------------+
        | message_notification          | ``MessageNotificationLevel``  |
        +-------------------------------+-------------------------------+
        | mfa                           | ``MFA``                       |
        +-------------------------------+-------------------------------+
        | name                          | `str`                         |
        +-------------------------------+-------------------------------+
        | nsfw_level                    | ``NsfwLevel``                 |
        +-------------------------------+-------------------------------+
        | owner_id                      | `int`                         |
        +-------------------------------+-------------------------------+
        | preferred_locale              | ``Locale``                    |
        +-------------------------------+-------------------------------+
        | premium_tier                  | `int`                         |
        +-------------------------------+-------------------------------+
        | public_updates_channel_id     | `int`                         |
        +-------------------------------+-------------------------------+
        | rules_channel_id              | `int`                         |
        +-------------------------------+-------------------------------+
        | system_channel_id             | `int`                         |
        +-------------------------------+-------------------------------+
        | system_channel_flags          | ``SystemChannelFlag``         |
        +-------------------------------+-------------------------------+
        | vanity_code                   | `None`, `str`                 |
        +-------------------------------+-------------------------------+
        | verification_level            | ``VerificationLevel``         |
        +-------------------------------+-------------------------------+
        | widget_channel_id             | `int`                         |
        +-------------------------------+-------------------------------+
        | widget_enabled                | `bool`                        |
        +-------------------------------+-------------------------------+
        """
        old_attributes = {}
        
        # ignoring 'roles'
        # ignoring 'emojis'
        # ignoring 'members'
        # ignoring 'presence'
        # ignoring 'channels'
        # ignoring 'voice_states'
        # ignoring 'user_count'
        # ignoring 'large'
        # ignoring 'stickers'
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        self._update_icon(data, old_attributes)
        self._update_invite_splash(data, old_attributes)
        self._update_discovery_splash(data, old_attributes)
        self._update_banner(data, old_attributes)
        
        afk_timeout = data['afk_timeout']
        if self.afk_timeout != afk_timeout:
            old_attributes['afk_timeout'] = self.afk_timeout
            self.afk_timeout = afk_timeout
        
        verification_level = VerificationLevel.get(data['verification_level'])
        if self.verification_level is not verification_level:
            old_attributes['verification_level'] = self.verification_level
            self.verification_level = verification_level

        message_notification = MessageNotificationLevel.get(data['default_message_notifications'])
        if self.message_notification is not message_notification:
            old_attributes['message_notification'] = self.message_notification
            self.message_notification = message_notification
        
        mfa = MFA.get(data['mfa_level'])
        if self.mfa is not mfa:
            old_attributes['mfa'] = self.mfa
            self.mfa = mfa
        
        hub_type = HubType.get(data.get('hub_type', 0))
        if self.hub_type is not hub_type:
            old_attributes['hub_type'] = self.hub_type
            self.hub_type = hub_type
        
        content_filter = ContentFilterLevel.get(data.get('explicit_content_filter', 0))
        if self.content_filter is not content_filter:
            old_attributes['content_filter'] = self.content_filter
            self.content_filter = content_filter
        
        available = (not data.get('unavailable', False))
        if self.available != available:
            old_attributes['available'] = self.available
            self.available = available
        
        features = parse_features(data)
        if self.features != features:
            old_attributes['features'] = self.features
            self.features = features
        
        system_channel_id = data.get('system_channel_id', None)
        if system_channel_id is None:
            system_channel_id = 0
        else:
            system_channel_id = int(system_channel_id)
        
        if self.system_channel_id != system_channel_id:
            old_attributes['system_channel_id'] = self.system_channel_id
            self.system_channel_id = system_channel_id
        
        try:
            system_channel_flags = SystemChannelFlag(data['system_channel_flags'])
        except KeyError:
            system_channel_flags = SystemChannelFlag.ALL
        
        if self.system_channel_flags != system_channel_flags:
            old_attributes['system_channel_flags'] = self.system_channel_flags
            self.system_channel_flags = system_channel_flags
        
        public_updates_channel_id = data.get('public_updates_channel_id', None)
        if public_updates_channel_id is None:
            public_updates_channel_id = 0
        else:
            public_updates_channel_id = int(public_updates_channel_id)
        
        if self.public_updates_channel_id !=  public_updates_channel_id:
            old_attributes['public_updates_channel_id'] = self.public_updates_channel_id
            self.public_updates_channel_id = public_updates_channel_id
        
        owner_id = data.get('owner_id', None)
        if owner_id is None:
            owner_id = 0
        else:
            owner_id = int(owner_id)
        
        if self.owner_id != owner_id:
            old_attributes['owner_id'] = self.owner_id
            self.owner_id = owner_id
        
        afk_channel_id = data['afk_channel_id']
        if afk_channel_id is None:
            afk_channel_id = 0
        else:
            afk_channel_id = int(afk_channel_id)
        if self.afk_channel_id != afk_channel_id:
            old_attributes['afk_channel_id'] = self.afk_channel_id
            self.afk_channel_id = afk_channel_id
        
        widget_enabled = data.get('widget_enabled', False)
        if self.widget_enabled != widget_enabled:
            old_attributes['widget_enabled'] = self.widget_enabled
            self.widget_enabled = widget_enabled
        
        widget_channel_id = data.get('widget_channel_id', None)
        if widget_channel_id is None:
            widget_channel_id = 0
        else:
            widget_channel_id = int(widget_channel_id)
        
        if self.widget_channel_id != widget_channel_id:
            old_attributes['widget_channel_id'] = self.widget_channel_id
            self.widget_channel_id = widget_channel_id
        
        rules_channel_id = data.get('rules_channel_id', None)
        if rules_channel_id is None:
            rules_channel_id = 0
        else:
            rules_channel_id = int(rules_channel_id)
        
        if self.rules_channel_id != rules_channel_id:
            old_attributes['rules_channel_id'] = self.rules_channel_id
            self.rules_channel_id = rules_channel_id
        
        description = data.get('description', None)
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        vanity_code = data.get('vanity_url_code', None)
        if self.vanity_code != vanity_code:
            old_attributes['vanity_code'] = self.vanity_code
            self.vanity_code = vanity_code
        
        max_users = data.get('max_members', None)
        if max_users is None:
            max_users = MAX_USERS_DEFAULT
        if self.max_users != max_users:
            old_attributes['max_users'] = self.max_users
            self.max_users = max_users
        
        max_presences = data.get('max_presences', None)
        if max_presences is None:
            max_presences = MAX_PRESENCES_DEFAULT
        if self.max_presences != max_presences:
            old_attributes['max_presences'] = self.max_presences
            self.max_presences = max_presences
        
        max_video_channel_users = data.get('max_video_channel_users', None)
        if max_video_channel_users is None:
            max_video_channel_users = MAX_VIDEO_CHANNEL_USERS_DEFAULT
        if self.max_video_channel_users != max_video_channel_users:
            old_attributes['max_video_channel_users'] = self.max_video_channel_users
            self.max_video_channel_users = max_video_channel_users
        
        premium_tier = parse_premium_tier(data)
        if self.premium_tier != premium_tier:
            old_attributes['premium_tier'] = self.premium_tier
            self.premium_tier = premium_tier

        boost_count = data.get('premium_subscription_count', None)
        if boost_count is None:
            boost_count = 0
        
        if self.boost_count != boost_count:
            old_attributes['boost_count'] = self.boost_count
            self.boost_count = boost_count
        
        self._boosters = None
        
        preferred_locale = get_locale(data.get('preferred_locale', None))
        if self.preferred_locale is not preferred_locale:
            old_attributes['preferred_locale'] = self.preferred_locale
            self.preferred_locale = preferred_locale
        
        nsfw_level = NsfwLevel.get(data.get('nsfw_level', 0))
        if self.nsfw_level is not nsfw_level:
            old_attributes['nsfw_level'] = self.nsfw_level
            self.nsfw_level = nsfw_level
        
        boost_progress_bar_enabled = data.get('premium_progress_bar_enabled', False)
        if self.boost_progress_bar_enabled != boost_progress_bar_enabled:
            old_attributes['boost_progress_bar_enabled'] = self.boost_progress_bar_enabled
            self.boost_progress_bar_enabled = boost_progress_bar_enabled
        
        self._update_counts_only(data)
        
        return old_attributes
    
    
    def _update_attributes(self, data):
        """
        Updates the guild and with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild data received from Discord.
        """
        # ignoring 'roles'
        # ignoring 'emojis'
        # ignoring 'members'
        # ignoring 'presence'
        # ignoring 'channels'
        # ignoring 'voice_states'
        # ignoring 'stickers'
        
        self.name = data['name']
        
        self._set_icon(data)
        self._set_invite_splash(data)
        self._set_discovery_splash(data)
        self._set_banner(data)
        
        self.afk_timeout = data['afk_timeout']
        
        self.verification_level = VerificationLevel.get(data['verification_level'])
        
        self.message_notification = MessageNotificationLevel.get(data['default_message_notifications'])
        
        self.mfa = MFA.get(data['mfa_level'])
        
        self.hub_type = HubType.get(data.get('hub_type', 0))
        
        self.content_filter = ContentFilterLevel.get(data.get('explicit_content_filter', 0))

        self.available = (not data.get('unavailable', False))
        
        self.features = parse_features(data)
        
        system_channel_id = data.get('system_channel_id', None)
        if system_channel_id is None:
            system_channel_id = 0
        else:
            system_channel_id = int(system_channel_id)
        self.system_channel_id = system_channel_id
        
        try:
            system_channel_flags = SystemChannelFlag(data['system_channel_flags'])
        except KeyError:
            system_channel_flags = SystemChannelFlag.ALL
        self.system_channel_flags = system_channel_flags
        
        public_updates_channel_id = data.get('public_updates_channel_id', None)
        if public_updates_channel_id is None:
            public_updates_channel_id = 0
        else:
            public_updates_channel_id = int(public_updates_channel_id)
        self.public_updates_channel_id = public_updates_channel_id
        
        owner_id = data.get('owner_id', None)
        if owner_id is None:
            owner_id = 0
        else:
            owner_id = int(owner_id)
        self.owner_id= owner_id
        
        afk_channel_id = data.get('afk_channel_id', None)
        if afk_channel_id is None:
            afk_channel_id = 0
        else:
            afk_channel_id = int(afk_channel_id)
        self.afk_channel_id = afk_channel_id
        
        self.widget_enabled = data.get('widget_enabled', False)

        widget_channel_id = data.get('widget_channel_id', None)
        if widget_channel_id is None:
            widget_channel_id = 0
        else:
            widget_channel_id = int(widget_channel_id)
        self.widget_channel_id = widget_channel_id
        
        rules_channel_id = data.get('rules_channel_id', None)
        if rules_channel_id is None:
            rules_channel_id = 0
        else:
            rules_channel_id = int(rules_channel_id)
        self.rules_channel_id = rules_channel_id
        
        self.description = data.get('description', None)
        
        self.vanity_code = data.get('vanity_url_code', None)
        
        max_users = data.get('max_members', None)
        if max_users is None:
            max_users = MAX_USERS_DEFAULT
        self.max_users = max_users
        
        max_presences = data.get('max_presences', None)
        if max_presences is None:
            max_presences = MAX_PRESENCES_DEFAULT
        self.max_presences = max_presences
        
        max_video_channel_users = data.get('max_video_channel_users', None)
        if max_video_channel_users is None:
            max_video_channel_users = MAX_VIDEO_CHANNEL_USERS_DEFAULT
        self.max_video_channel_users = max_video_channel_users
        
        self.premium_tier = parse_premium_tier(data)
        
        boost_count = data.get('premium_subscription_count', None)
        if boost_count is None:
            boost_count = 0
        
        self.boost_count = boost_count
        self._boosters = None
        
        self.preferred_locale = get_locale(data.get('preferred_locale', None))
        
        self.nsfw_level = NsfwLevel.get(data.get('nsfw_level', 0))
        
        self.boost_progress_bar_enabled = data.get('premium_progress_bar_enabled', False)
        
        self._update_counts_only(data)
    
    
    def _update_counts_only(self, data):
        """
        Updates the guilds' counts if given.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild data.
        """
        try:
            approximate_online_count = data['approximate_presence_count']
        except KeyError:
            pass
        else:
            self.approximate_online_count = approximate_online_count
        
        try:
            approximate_user_count = data['approximate_member_count']
        except KeyError:
            pass
        else:
            self.approximate_user_count = approximate_user_count
    
    
    def _update_emojis(self, data):
        """
        Updates the emojis o the guild and returns all the changes broke down for each changes emoji.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Received emoji datas.
        
        Returns
        -------
        changes : `list` of `tuple` (`int`, ``Emoji``, (`None`, `dict` of (`str`, `Any`) items)))
            The changes broken down for each changed emoji. Each element of the list is a tuple of 3 elements:
            
            +-------+-------------------+-----------------------------------------------+
            | Index | Respective name   | Type                                          |
            +=======+===================+===============================================+
            | 0     | action            | `int`                                         |
            +-------+-------------------+-----------------------------------------------+
            | 1     | emoji             | ``Emoji``                                     |
            +-------+-------------------+-----------------------------------------------+
            | 2     | old_attributes    | `None`, `dict` of (`str`, `Any`) items        |
            +-------+-------------------+-----------------------------------------------+
            
            Possible actions:
            
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | EMOJI_UPDATE_NONE     | `0`   |
            +-----------------------+-------+
            | EMOJI_UPDATE_CREATE   | `1`   |
            +-----------------------+-------+
            | EMOJI_UPDATE_DELETE   | `2`   |
            +-----------------------+-------+
            | EMOJI_UPDATE_EDIT     | `3`   |
            +-----------------------+-------+
            
            If action is `EMOJI_UPDATE_EDIT`, then `old_attributes` is passed as a dictionary containing the changed
            attributes in an `attribute-name` - `old-value` relation. Every item in `old_attributes` is optional.
            
            +-------------------+-------------------------------+
            | Keys              | Values                        |
            +===================+===============================+
            | animated          | `bool`                        |
            +-------------------+-------------------------------+
            | available         | `bool`                        |
            +-------------------+-------------------------------+
            | managed           | `bool`                        |
            +-------------------+-------------------------------+
            | name              | `int`                         |
            +-------------------+-------------------------------+
            | require_colons    | `bool`                        |
            +-------------------+-------------------------------+
            | roles_ids         | `None`, `tuple` of ``Role``   |
            +-------------------+-------------------------------+
        """
        emojis = self.emojis
        changes = []
        old_ids = set(emojis)
        
        for emoji_data in data:
            emoji_id = int(emoji_data['id'])
            try:
                emoji = emojis[emoji_id]
            except KeyError:
                emoji = Emoji(emoji_data, self.id)
                emojis[emoji_id] = emoji
                changes.append((EMOJI_UPDATE_CREATE, emoji, None),)
            else:
                old_attributes = emoji._difference_update_attributes(emoji_data)
                if old_attributes:
                    changes.append((EMOJI_UPDATE_EDIT, emoji, old_attributes),)
                old_ids.remove(emoji_id)
        
        for emoji_id in old_ids:
            try:
                emoji = emojis.pop(emoji_id)
            except KeyError:
                pass
            else:
                changes.append((EMOJI_UPDATE_DELETE, emoji, None),)
        
        return changes
    
    
    def _sync_emojis(self, emoji_datas):
        """
        Syncs the emojis of the guild.
        
        Parameters
        ----------
        emoji_datas : `list` of (`dict` of (`str`, `Any`) items)
            Received emoji datas.
        """
        emojis = self.emojis
        old_ids = set(emojis)
        
        for emoji_data in emoji_datas:
            emoji_id = int(emoji_data['id'])
            try:
                emoji = emojis[emoji_id]
            except KeyError:
                emoji = Emoji(emoji_data, self.id)
                emojis[emoji_id] = emoji
            else:
                emoji._update_attributes(emoji_data)
                old_ids.remove(emoji_id)
        
        for emoji_id in old_ids:
            try:
                del emojis[emoji_id]
            except KeyError:
                pass
    
    
    def _update_stickers(self, data):
        """
        Updates the stickers of the guild and returns the changes broke down for each changed sticker.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Received sticker datas.
        
        Returns
        -------
        changes : `list` of `tuple` (`int`, ``Sticker``, (`None`, `dict` of (`str`, `Any`) items)))
            The changes broken down for each changed sticker. Each element of the list is a tuple of 3 elements:
            
            +-------+-------------------+-----------------------------------------------+
            | Index | Respective name   | Type                                          |
            +=======+===================+===============================================+
            | 0     | action            | `int`                                         |
            +-------+-------------------+-----------------------------------------------+
            | 1     | sticker           | ``Sticker``                                   |
            +-------+-------------------+-----------------------------------------------+
            | 2     | old_attributes    | `None`, `dict` of (`str`, `Any`) items      |
            +-------+-------------------+-----------------------------------------------+
            
            Possible actions:
            
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | STICKER_UPDATE_NONE   | `0`   |
            +-----------------------+-------+
            | STICKER_UPDATE_CREATE | `1`   |
            +-----------------------+-------+
            | STICKER_UPDATE_DELETE | `2`   |
            +-----------------------+-------+
            | STICKER_UPDATE_EDIT   | `3`   |
            +-----------------------+-------+
            
            If action is `STICKER_UPDATE_EDIT`, then `old_attributes` is passed as a dictionary containing the changed
            attributes in an `attribute-name` - `old-value` relation. Every item in `old_attributes` is optional.
            
            +-----------------------+-----------------------------------+
            | Keys                  | Values                            |
            +=======================+===================================+
            | available             | `bool`                            |
            +-----------------------+-----------------------------------+
            | description           | `None`, `str`                   |
            +-----------------------+-----------------------------------+
            | name                  | `str`                             |
            +-----------------------+-----------------------------------+
            | sort_value            | `int`                             |
            +-----------------------+-----------------------------------+
            | tags                  | `None`  or `frozenset` of `str`   |
            +-----------------------+-----------------------------------+
        """
        stickers = self.stickers
        changes = []
        old_ids = set(stickers)
        
        for sticker_data in data:
            sticker_id = int(sticker_data['id'])
            try:
                sticker = stickers[sticker_id]
            except KeyError:
                sticker = Sticker(sticker_data)
                stickers[sticker_id] = sticker
                changes.append((STICKER_UPDATE_CREATE, sticker, None),)
            else:
                old_attributes = sticker._difference_update_attributes(sticker_data)
                if old_attributes:
                    changes.append((STICKER_UPDATE_EDIT, sticker, old_attributes),)
                old_ids.remove(sticker_id)
        
        for sticker_id in old_ids:
            try:
                sticker = stickers.pop(sticker_id)
            except KeyError:
                pass
            else:
                changes.append((STICKER_UPDATE_DELETE, sticker, None),)
        
        return changes
    
    
    def _sync_stickers(self, data):
        """
        Syncs the stickers of the guild.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Received sticker datas.
        """
        stickers = self.stickers
        old_ids = set(stickers)
        
        for sticker_data in data:
            sticker_id = int(sticker_data['id'])
            try:
                sticker = stickers[sticker_id]
            except KeyError:
                sticker = Sticker(sticker_data)
                stickers[sticker_id] = sticker
            else:
                sticker._update_attributes(sticker_data)
                old_ids.remove(sticker_id)
        
        for sticker_id in old_ids:
            try:
                del stickers[sticker_id]
            except KeyError:
                pass
    
    
    def _invalidate_permission_cache(self):
        """
        Invalidates the cached permissions of the guild.
        """
        self._permission_cache = None
        for channel in self.channels.values():
            channel.metadata._invalidate_permission_cache()
    
    
    @property
    def owner(self):
        """
        Returns the guild's owner's.
        
        Returns
        -------
        owner : ``UserClientBase``
            If user the guild has no owner, returns `ZEROUSER`.
        """
        owner_id = self.owner_id
        if owner_id == 0:
            owner = ZEROUSER
        else:
            owner = create_partial_user_from_id(owner_id)
        
        return owner
    
    
    def iter_features(self):
        """
        Iterates over the features of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        feature : ``GuildFeature``
        """
        features = self.features
        if (features is not None):
            yield from features
    
    
    def has_feature(self, feature):
        """
        Returns whether the guild has the give feature.
        
        Parameters
        ----------
        feature : ``GuildFeature``
            The feature to look for.
        
        Returns
        -------
        has_feature : `bool`
        """
        features = self.features
        if features is None:
            return False
        
        return feature in features
    
    
    @property
    def premium_perks(self):
        """
        Returns the guild's premium tier perks for it's current level.
        
        Returns
        -------
        premium_perks : ``GuildPremiumPerks``
        """
        return PREMIUM_TIERS.get(self.premium_tier, PREMIUM_TIER_MAX)
    
    
    @property
    def emoji_limit(self):
        """
        The maximal amount of emojis, what the guild can have.
        
        Returns
        -------
        limit : `int`
        """
        limit = self.premium_perks.emoji_limit
        if limit < 200 and self.has_feature(GuildFeature.more_emoji):
            limit = 200
        
        return limit
    
    
    @property
    def bitrate_limit(self):
        """
        The maximal bitrate for the guild's voice channels.
        
        Returns
        -------
        limit : `int`
        """
        limit = self.premium_perks.bitrate_limit
        if limit < 128000 and self.has_feature(GuildFeature.vip_voice_regions):
            limit = 128000
        
        return limit
    
    
    @property
    def upload_limit(self):
        """
        The maximal size of files, which can be uploaded to the guild's channels.
        
        Returns
        -------
        limit : `int`
        """
        return self.premium_perks.upload_limit
    
    
    @property
    def sticker_limit(self):
        """
        The maximal amount of stickers, what the guild can have.
        
        Returns
        -------
        limit : `int`
        """
        limit = self.premium_perks.sticker_limit
        if limit < 30 and self.has_feature(GuildFeature.more_sticker):
            limit = 30
        
        return limit
    
    
    widget_json_url = property(module_urls.guild_widget_json_url)
    
    
    @property
    def boosters(self):
        """
        The boosters of the guild sorted by their subscription date.
        
        These users are queried from the guild's `.users` dictionary, so make sure that is populated before accessing
        the property.
        
        Returns
        -------
        boosters : `list` of ``ClientUserBase``
        """
        boosters = self._boosters
        if boosters is None:
            if self.boost_count:
                boosters_ordered = []
                guild_id = self.id
                for user in self.users.values():
                    try:
                        guild_profile = user.guild_profiles[guild_id]
                    except KeyError:
                        continue
                    
                    boosts_since = guild_profile.boosts_since
                    if boosts_since is None:
                        continue
                    
                    boosters_ordered.append((user, boosts_since),)
                    
                boosters_ordered.sort(key = _user_date_sort_key)
                boosters = [element[0] for element in boosters_ordered]
            else:
                boosters = []
            
            self._boosters = boosters

        return boosters
    
    
    @property
    def emoji_counts(self):
        """
        Returns the emoji counts of the guild.
        
        Returns
        -------
        emoji_counts : ``EmojiCounts``
        """
        return EmojiCounts.from_emojis(self.emojis.values())
    
    
    @property
    def sticker_counts(self):
        """
        Returns the sticker counts of the guild for each type.
        
        Returns
        -------
        sticker_counts : ``StickerCounts``
        """
        return StickerCounts.from_stickers(self.stickers.values())
    
    
    @property
    def sticker_count(self):
        """
        `.sticker_count` is deprecated and will be removed in 2023 August. Please use `.sticker_counts` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.sticker_count` is deprecated and will be removed in 2023 January. '
                f'Please use `.sticker_counts` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.sticker_counts
    
    
    @property
    def channel_list(self):
        """
        Returns the channels of the guild in a list in their display order. Note, that channels inside of categories are
        excluded.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return sorted(channel for channel in self.channels.values() if channel.parent is None)
    
    
    @property
    def channel_list_flattened(self):
        """
        Returns the channels of the guild in a list in their display order. Note, that channels inside of categories are
        included as well.
        
        channels : `list` of ``Channel``
        """
        channels = []
        for channel in sorted(channel for channel in self.channels.values() if channel.parent is None):
            channels.append(channel)
            if channel.is_guild_category():
                channels.extend(channel.list_channels)
        
        return channels
    
    
    @property
    def role_list(self):
        """
        Returns the roles of the guild in their display order.
        
        Returns
        -------
        roles : `list` of ``Role``
        """
        return sorted(self.roles.values())
    
    
    @property
    def nsfw(self):
        """
        Returns whether the guild is nsfw.
        
        Returns
        -------
        nsfw : `bool`
        """
        return self.nsfw_level.nsfw
    
    
    @property
    def public_updates_channel(self):
        """
        Returns the channel's where the guild's public updates should go.
        
        Returns
        -------
        public_updates_channel : `None`, ``Channel``
        """
        public_updates_channel_id = self.public_updates_channel_id
        if public_updates_channel_id:
            return self.channels.get(public_updates_channel_id, None)
    
    
    @property
    def afk_channel(self):
        """
        Returns the afk channel of the guild if it has.
        
        Returns
        -------
        afk_channel : `None`, ``Channel``
        """
        afk_channel_id = self.afk_channel_id
        if afk_channel_id:
            return self.channels.get(afk_channel_id, None)
    
    
    @property
    def rules_channel(self):
        """
        Returns the channel where the rules of a public guild's should be.

        Returns
        -------
        rules_channel : `None`, ``Channel``
        """
        rules_channel_id = self.rules_channel_id
        if rules_channel_id:
            return self.channels.get(rules_channel_id, None)
    
    
    @property
    def system_channel(self):
        """
        Returns the channel where the system messages are sent.
        
        Returns
        -------
        public_updates_channel : `None`, ``Channel``
        """
        system_channel_id = self.system_channel_id
        if system_channel_id:
            return self.channels.get(system_channel_id, None)
    
    
    @property
    def widget_channel(self):
        """
        Returns the channel for which the guild's widget is for.
        
        Returns
        -------
        public_updates_channel : `None`, ``Channel``
        """
        widget_channel_id = self.widget_channel_id
        if widget_channel_id:
            return self.channels.get(widget_channel_id, None)
    
    
    vanity_url = property(module_urls.guild_vanity_invite_url)
