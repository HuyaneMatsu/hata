__all__ = ('Guild',)

from datetime import datetime as DateTime, timezone as TimeZone
from re import I as re_ignore_case, compile as re_compile, escape as re_escape
from warnings import warn

from scarletio import WeakValueDictionary, export, include

from ....env import CACHE_USER

from ...bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ...channel import Channel
from ...channel.channel_metadata.constants import (
    NAME_LENGTH_MAX as CHANNEL_NAME_LENGTH_MAX, NAME_LENGTH_MIN as CHANNEL_NAME_LENGTH_MIN
)
from ...core import GUILDS
from ...emoji import Emoji
from ...emoji.emoji.constants import NAME_LENGTH_MAX as EMOJI_NAME_LENGTH_MAX, NAME_LENGTH_MIN as EMOJI_NAME_LENGTH_MIN
from ...emoji.emoji.fields import parse_id as parse_emoji_id
from ...http.urls import (
    build_guild_banner_url, build_guild_banner_url_as, build_guild_discovery_splash_url,
    build_guild_discovery_splash_url_as, build_guild_home_splash_url, build_guild_home_splash_url_as,
    build_guild_icon_url, build_guild_icon_url_as, build_guild_invite_splash_url, build_guild_invite_splash_url_as,
    build_guild_vanity_invite_url, build_guild_widget_json_url, build_guild_widget_url, build_guild_widget_url_as
)
from ...localization.utils import LOCALE_DEFAULT
from ...permission import Permission
from ...permission.permission import PERMISSION_ALL, PERMISSION_MASK_ADMINISTRATOR, PERMISSION_NONE
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...role import Role
from ...role.role.constants import NAME_LENGTH_MAX as ROLE_NAME_LENGTH_MAX, NAME_LENGTH_MIN as ROLE_NAME_LENGTH_MIN
from ...soundboard import SoundboardSound
from ...soundboard.soundboard_sound.constants import (
    NAME_LENGTH_MAX as SOUNDBOARDS_SOUND_NAME_LENGTH_MAX, NAME_LENGTH_MIN as SOUNDBOARDS_SOUND_NAME_LENGTH_MIN
)
from ...soundboard.soundboard_sound.fields import parse_id as parse_soundboard_sound_id
from ...sticker import Sticker
from ...sticker.sticker.constants import (
    NAME_LENGTH_MAX as STICKER_NAME_LENGTH_MAX, NAME_LENGTH_MIN as STICKER_NAME_LENGTH_MIN
)
from ...sticker.sticker.fields import parse_id as parse_sticker_id
from ...user import VoiceState, ZEROUSER, create_partial_user_from_id
from ...user.guild_profile.constants import (
    NICK_LENGTH_MAX as USER_NICK_LENGTH_MAX, NICK_LENGTH_MIN as USER_NICK_LENGTH_MIN
)
from ...user.user.constants import NAME_LENGTH_MAX as USER_NAME_LENGTH_MAX, NAME_LENGTH_MIN as USER_NAME_LENGTH_MIN
from ...user.user.matching import (
    _user_date_sort_key, _user_match_sort_key, USER_MATCH_WEIGHT_DISPLAY_NAME, USER_MATCH_WEIGHT_NAME,
    USER_MATCH_WEIGHT_NICK, _is_user_matching_name_with_discriminator, _parse_name_with_discriminator
)
from ...utils import DATETIME_FORMAT_CODE, EMOJI_NAME_RP
from ...webhook import WebhookBase

from .constants import (
    EMOJI_EVENT_CREATE, EMOJI_EVENT_DELETE, EMOJI_EVENT_UPDATE, GUILD_STATE_MASK_CACHE_ALL,
    GUILD_STATE_MASK_CACHE_BOOSTERS, GUILD_STATE_MASK_SOUNDBOARD_SOUNDS_CACHED, LARGE_GUILD_LIMIT,
    MAX_PRESENCES_DEFAULT, MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT, MAX_USERS_DEFAULT,
    MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT, SOUNDBOARD_SOUND_EVENT_CREATE, SOUNDBOARD_SOUND_EVENT_DELETE,
    SOUNDBOARD_SOUND_EVENT_UPDATE, STICKER_EVENT_CREATE, STICKER_EVENT_DELETE, STICKER_EVENT_UPDATE,
    VOICE_STATE_EVENT_JOIN, VOICE_STATE_EVENT_LEAVE, VOICE_STATE_EVENT_MOVE, VOICE_STATE_EVENT_UPDATE
)
from .emoji_counts import EmojiCounts
from .fields import (
    parse_afk_channel_id, parse_afk_timeout, parse_approximate_online_count, parse_approximate_user_count,
    parse_available, parse_boost_count, parse_boost_level, parse_boost_progress_bar_enabled, parse_channels,
    parse_client_guild_profile, parse_default_message_notification_level, parse_description, parse_embedded_activities,
    parse_emojis, parse_explicit_content_filter_level, parse_features, parse_hub_type, parse_id, parse_incidents,
    parse_inventory_settings, parse_large, parse_locale, parse_max_presences, parse_max_stage_channel_video_users,
    parse_max_users, parse_max_voice_channel_video_users, parse_mfa_level, parse_name, parse_nsfw_level, parse_owner_id,
    parse_public_updates_channel_id, parse_roles, parse_rules_channel_id, parse_safety_alerts_channel_id,
    parse_scheduled_events, parse_soundboard_sounds, parse_stages, parse_stickers, parse_system_channel_flags,
    parse_system_channel_id, parse_threads, parse_user_count, parse_users, parse_vanity_code, parse_verification_level,
    parse_voice_states, parse_widget_channel_id, parse_widget_enabled, put_afk_channel_id, put_afk_timeout,
    put_approximate_online_count, put_approximate_user_count, put_available, put_boost_count, put_boost_level,
    put_boost_progress_bar_enabled, put_channels, put_default_message_notification_level, put_description,
    put_embedded_activities, put_emojis, put_explicit_content_filter_level, put_features, put_hub_type, put_id,
    put_incidents, put_inventory_settings, put_large, put_locale, put_max_presences, put_max_stage_channel_video_users,
    put_max_users, put_max_voice_channel_video_users, put_mfa_level, put_name, put_nsfw_level, put_owner_id,
    put_public_updates_channel_id, put_roles, put_rules_channel_id, put_safety_alerts_channel_id, put_scheduled_events,
    put_soundboard_sounds, put_stages, put_stickers, put_system_channel_flags, put_system_channel_id, put_threads,
    put_user_count, put_users, put_vanity_code, put_verification_level, put_voice_states, put_widget_channel_id,
    put_widget_enabled, validate_afk_channel_id, validate_afk_timeout, validate_approximate_online_count,
    validate_approximate_user_count, validate_available, validate_boost_count, validate_boost_level,
    validate_boost_progress_bar_enabled, validate_channels, validate_default_message_notification_level,
    validate_description, validate_embedded_activities, validate_emojis, validate_explicit_content_filter_level,
    validate_features, validate_hub_type, validate_id, validate_incidents, validate_inventory_settings, validate_large,
    validate_locale, validate_max_presences, validate_max_stage_channel_video_users, validate_max_users,
    validate_max_voice_channel_video_users, validate_mfa_level, validate_name, validate_nsfw_level, validate_owner_id,
    validate_public_updates_channel_id, validate_roles, validate_rules_channel_id, validate_safety_alerts_channel_id,
    validate_scheduled_events, validate_soundboard_sounds, validate_stages, validate_stickers,
    validate_system_channel_flags, validate_system_channel_id, validate_threads, validate_user_count, validate_users,
    validate_vanity_code, validate_verification_level, validate_voice_states, validate_widget_channel_id,
    validate_widget_enabled
)
from .flags import SystemChannelFlag
from .guild_boost_perks import LEVELS as BOOST_LEVELS, LEVEL_MAX as BOOST_LEVEL_MAX
from .preinstanced import (
    ExplicitContentFilterLevel, GuildFeature, HubType, MfaLevel, MessageNotificationLevel, NsfwLevel, VerificationLevel
)
from .sticker_counts import StickerCounts
from .helpers import (
    _channel_match_sort_key, _emoji_match_sort_key, _role_match_sort_key, _soundboard_sound_match_sort_key,
    _sticker_match_sort_key, _strip_emoji_name, STICKER_MATCH_WEIGHT_NAME, STICKER_MATCH_WEIGHT_TAG
)


Client = include('Client')
trigger_voice_client_ghost_event = include('trigger_voice_client_ghost_event')


if CACHE_USER:
    GUILD_USERS_TYPE = dict
else:
    GUILD_USERS_TYPE = WeakValueDictionary


GUILD_BANNER = IconSlot('banner', 'banner')
GUILD_DISCOVERY_SPLASH = IconSlot('discovery_splash', 'discovery_splash')
GUILD_HOME_SPLASH = IconSlot('home_splash', 'home_header')
GUILD_ICON = IconSlot('icon', 'icon')
GUILD_INVITE_SPLASH = IconSlot('invite_splash', 'splash')


PRECREATE_FIELDS = {
    'afk_channel': ('afk_channel_id', validate_afk_channel_id),
    'afk_channel_id': ('afk_channel_id', validate_afk_channel_id),
    'afk_timeout': ('afk_timeout', validate_afk_timeout),
    'approximate_online_count': ('approximate_online_count', validate_approximate_online_count),
    'approximate_user_count': ('approximate_user_count', validate_approximate_user_count),
    'available': ('available', validate_available),
    'banner': ('banner', GUILD_BANNER.validate_icon),
    'boost_count': ('boost_count', validate_boost_count),
    'boost_progress_bar_enabled': ('boost_progress_bar_enabled', validate_boost_progress_bar_enabled),
    'channels': ('channels', validate_channels),
    'default_message_notification_level': (
        'default_message_notification_level', validate_default_message_notification_level,
    ),
    'description': ('description', validate_description),
    'discovery_splash': ('discovery_splash', GUILD_INVITE_SPLASH.validate_icon),
    'embedded_activities': ('embedded_activities', validate_embedded_activities),
    'explicit_content_filter_level': ('explicit_content_filter_level', validate_explicit_content_filter_level),
    'emojis': ('emojis', validate_emojis),
    'features': ('features', validate_features),
    'home_splash': ('home_splash', GUILD_HOME_SPLASH.validate_icon),
    'hub_type': ('hub_type', validate_hub_type),
    'icon': ('icon', GUILD_ICON.validate_icon),
    'incidents': ('incidents', validate_incidents),
    'inventory_settings': ('inventory_settings', validate_inventory_settings),
    'invite_splash': ('invite_splash', GUILD_INVITE_SPLASH.validate_icon),
    'large': ('large', validate_large),
    'max_presences': ('max_presences', validate_max_presences),
    'max_stage_channel_video_users': ('max_stage_channel_video_users', validate_max_stage_channel_video_users),
    'max_users': ('max_users', validate_max_users),
    'max_voice_channel_video_users': ('max_voice_channel_video_users', validate_max_voice_channel_video_users),
    'mfa_level': ('mfa_level', validate_mfa_level),
    'name': ('name', validate_name),
    'nsfw_level': ('nsfw_level', validate_nsfw_level),
    'owner': ('owner_id', validate_owner_id),
    'owner_id': ('owner_id', validate_owner_id),
    'locale': ('locale', validate_locale),
    'boost_level': ('boost_level', validate_boost_level),
    'public_updates_channel': ('public_updates_channel_id', validate_public_updates_channel_id),
    'public_updates_channel_id': ('public_updates_channel_id', validate_public_updates_channel_id),
    'roles': ('roles', validate_roles),
    'rules_channel': ('rules_channel_id', validate_rules_channel_id),
    'rules_channel_id': ('rules_channel_id', validate_rules_channel_id),
    'safety_alerts_channel': ('safety_alerts_channel_id', validate_safety_alerts_channel_id),
    'safety_alerts_channel_id': ('safety_alerts_channel_id', validate_safety_alerts_channel_id),
    'scheduled_events': ('scheduled_events', validate_scheduled_events),
    'soundboard_sounds': ('soundboard_sounds', validate_soundboard_sounds),
    'stages': ('stages', validate_stages),
    'stickers': ('stickers', validate_stickers),
    'system_channel_flags': ('system_channel_flags', validate_system_channel_flags),
    'system_channel': ('system_channel_id', validate_system_channel_id),
    'system_channel_id': ('system_channel_id', validate_system_channel_id),
    'threads': ('threads', validate_threads),
    'user_count': ('user_count', validate_user_count),
    'users': ('users', validate_users),
    'vanity_code': ('vanity_code', validate_vanity_code),
    'verification_level': ('verification_level', validate_verification_level),
    'voice_states': ('voice_states', validate_voice_states),
    'widget_channel': ('widget_channel_id', validate_widget_channel_id),
    'widget_channel_id': ('widget_channel_id', validate_widget_channel_id),
    'widget_enabled': ('widget_enabled', validate_widget_enabled),
}


USER_ALL_NAME_LENGTH_MAX = max(USER_NAME_LENGTH_MAX, USER_NICK_LENGTH_MAX)
USER_ALL_NAME_LENGTH_MIN = max(USER_NAME_LENGTH_MIN, USER_NICK_LENGTH_MIN)
USER_ALL_NAME_LENGTH_MAX_WITH_DISCRIMINATOR = USER_ALL_NAME_LENGTH_MAX + 5


@export
class Guild(DiscordEntity, immortal = True):
    """
    Represents a Discord guild (or server).
    
    Attributes
    ----------
    _cache_boosters : ``None | list<ClientUserBase>``
        Cached slot for the boosters of the guild.
    
    _cache_permission : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    
    _state : `int`
        Bitwise mask used to track the guild's state.
    
    afk_channel_id : `int`
        The afk channel's identifier of the guild if it has.
        
        Defaults to `0`.
    
    afk_timeout : `int`
        The afk timeout at the `afk_channel`. Can be `0`, `60`, `300`, `900`, `1800`, `3600` in seconds.
        
        Defaults to `0` if not applicable.
    
    approximate_online_count : `int`
        The approximate amount of online users at the guild.
        
        Defaults to `0` if not yet received / requested.
    
    approximate_user_count : `int`
        The approximate amount of users at the guild.
        
        Defaults to `0` if not yet received / requested.
    
    available : `bool`
        Whether the guild is available.
    
    banner_hash : `int`
        The guild's banner's hash in `uint128`.
    
    banner_type : ``IconType``
        The guild's banner's type.
    
    boost_count : `int`
        The total number of boosts of the guild.
    
    boost_level : `int`
        The boost level of the guild. More boosters = higher level.
        
        Defaults to `0`.
    
    boost_progress_bar_enabled : `bool`
        Whether the guild has the boost progress bar enabled.
    
    channels : `dict` of (`int`, ``Channel``) items
        The channels of the guild stored in `channel_id` - `channel` relation.
    
    clients : `list` of ``Client``
        The loaded clients, who are the member of the guild. If no clients are member of a guild, it is partial.
    
    default_message_notification_level : ``MessageNotificationLevel``
        The default message notification level of the guild.
    
    description : `None`, `str`
        Description of the guild. The guild must be a Community guild.
    
    discovery_splash_hash : `int`
        The guild's discovery splash's hash in `uint128`.
    
    discovery_splash_type : ``IconType``
        The guild's discovery splash's type.
    
    embedded_activities : `None`, `set` of ``EmbeddedActivity``
        Embedded activity states to keep them alive in cache.
    
    emojis : `dict` of (`int`, ``Emoji``) items
        The emojis of the guild stored in `emoji_id` - `emoji` relation.
    
    explicit_content_filter_level : ``ExplicitContentFilterLevel``
        The explicit content filter level of the guild.
    
    features : `None`, `tuple` of ``GuildFeature``
        The guild's features.
    
    home_splash_hash : `int`
        The guild's home splash's hash in `uint128`.
    
    home_splash_type : ``IconType``
        The guild's home splash's type.
    
    hub_type : ``HubType``
        The guild's hub type. Only applicable for hub guilds.
    
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
    
    icon_type : ``IconType``
        The guild's icon's type.
    
    incidents : `None`, ``GuildIncidents``
        The guild's incidents (if any).
    
    inventory_settings : `None`, ``GuildInventorySettings``
        The guild's inventory settings (if any).
    
    id : `int`
        The unique identifier number of the guild.
    
    invite_splash_hash : `int`
        The guild's invite splash's hash in `uint128`. The guild must have `INVITE_SPLASH` feature.
    
    invite_splash_type : ``IconType``
        The guild's invite splash's type.
    
    large : `bool`
        Whether the guild is considered as a large one.
    
    locale : ``Locale``
        The preferred language of the guild.
        
        The guild must be a Community guild, defaults to `'en-US'`.
    
    max_presences : `int`
        The maximal amount of presences for the guild.
        
        Defaults to `0`. Only applicable for very large guilds.
    
    max_stage_channel_video_users : `int`
        The maximal amount of users watching a video in a stage channel.
        
        Defaults to `50`.
    
    max_users : `int`
        The maximal allowed users in the guild.
        
        Defaults to `250000`.
    
    max_voice_channel_video_users : `int`
        The maximal amount of users watching a video in a stage channel.
        
        Defaults to `25`.
    
    mfa_level : ``MfaLevel``
        The required multi-factor authentication level for the guild.
    
    name : `str`
        The name of the guild.
    
    nsfw_level : ``NsfwLevel``
        The guild's nsfw level.
    
    owner_id : `int`
        The guild's owner's id.
        
        Defaults to `0`.
    
    public_updates_channel_id : `int`
        The channel's identifier where the guild's public updates should go.
        
        Defaults to `0`. The guild must be a `community` guild.
    
    roles : `dict` of (`int`, ``Role``) items
        The roles of the guild stored in `role_id` - `role` relation.
    
    rules_channel_id : `int`
        The channel's identifier where the rules of a public guild's should be.
        
        Defaults to `0`. The guild must be a `community` guild.
    
    safety_alerts_channel_id : `int`
        The channel's identifier where safety alerts are sent by Discord.
        
        Defaults to `0`.
    
    scheduled_events : `dict` of (`int`, ``ScheduledEvent``) items
        The scheduled events of the guild.
    
    soundboard_sounds : `None`, `dict` of (`int`, ``SoundboardSound``) items
        The soundboard sounds of the guild.
        
        Defaults to `None` if would be empty.
    
    stages : `None`, `dict` of (`int`, ``Stage``) items
        Active stages of the guild.
        
        Defaults to `None` if would be empty.
    
    stickers : ``dict<int, Sticker>``
        Stickers of the guild.
    
    system_channel_flags : ``SystemChannelFlag``
        Describe which type of messages are sent automatically to the system channel.
    
    system_channel_id : `int`
        The channel's identifier where the system messages are sent.
        
        Defaults to `0`.
    
    threads : `dict` of (`int`, ``Channel``)
        Thread channels of the guild.
    
    user_count : `int`
        The amount of users at the guild.
        
        Defaults to `0`.
    
    users : `dict`, ``WeakValueDictionary`` of (`int`, ``ClientUserBase``) items
        The users at the guild stored within `user_id` - `user` relation.
    
    vanity_code : `None`, `str`
        The guild's vanity invite's code if it has.
    
    verification_level : ``VerificationLevel``
        The minimal verification needed to join or to interact with guild.
    
    voice_states : `None`, `dict` of (`int`, ``VoiceState``) items
        Each user at a voice channel is represented by a their voice state. Voice state are stored in
        `respective user's id` - `voice state` relation.
    
    widget_channel_id : `int`
        The channel's identifier for which the guild's widget is for.
        
        Defaults to `0`.
    
    widget_enabled : `bool`
        Whether the guild's widget is enabled. Linked to ``.widget_channel``.
    
    Notes
    -----
    When a guild is loaded first time, some of it's attributes might not reflect their real value.
    These are the following:
    
    - ``.max_presences``
    - ``.max_users``
    - ``.widget_channel_id``
    - ``.widget_enabled``
    - ``.inventory_settings``.
    """
    __slots__ = (
        '_cache_boosters', '_cache_permission', '_state', 'afk_channel_id', 'afk_timeout', 'approximate_online_count',
        'approximate_user_count', 'available', 'boost_count', 'boost_level', 'boost_progress_bar_enabled', 'channels',
        'clients', 'default_message_notification_level', 'description', 'embedded_activities', 'emojis',
        'explicit_content_filter_level', 'features', 'hub_type', 'incidents', 'inventory_settings', 'large', 'locale',
        'max_presences', 'max_stage_channel_video_users', 'max_users', 'max_voice_channel_video_users', 'mfa_level',
        'name', 'nsfw_level', 'owner_id', 'public_updates_channel_id', 'roles', 'rules_channel_id',
        'safety_alerts_channel_id', 'scheduled_events', 'soundboard_sounds', 'stages', 'stickers',
        'system_channel_flags', 'system_channel_id', 'threads', 'user_count', 'users', 'vanity_code',
        'verification_level', 'voice_states', 'widget_channel_id', 'widget_enabled'
    )
    
    banner = GUILD_BANNER
    discovery_splash = GUILD_DISCOVERY_SPLASH
    home_splash = GUILD_HOME_SPLASH
    icon = GUILD_ICON
    invite_splash = GUILD_INVITE_SPLASH
    
    
    def __new__(
        cls,
        afk_channel_id = ...,
        afk_timeout = ...,
        banner = ...,
        boost_progress_bar_enabled = ...,
        default_message_notification_level = ...,
        description = ...,
        discovery_splash = ...,
        explicit_content_filter_level = ...,
        features = ...,
        home_splash = ...,
        hub_type = ...,
        icon = ...,
        invite_splash = ...,
        locale = ...,
        mfa_level = ...,
        name = ...,
        nsfw_level = ...,
        owner_id = ...,
        public_updates_channel_id = ...,
        safety_alerts_channel_id = ...,
        rules_channel_id = ...,
        system_channel_id = ...,
        system_channel_flags = ...,
        vanity_code = ...,
        verification_level = ...,
        widget_channel_id = ...,
        widget_enabled = ...,
    ):
        """
        Creates a new partial guild with the given fields.
        
        Parameters
        ----------
        afk_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The afk channel or its identifier.
        
        afk_timeout : `int`, Optional (Keyword only)
            The afk timeout at the `afk_channel`.
        
        banner : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's banner.
        
        boost_progress_bar_enabled : `bool`, Optional (Keyword only)
            Whether the guild has the boost progress bar enabled.
        
        default_message_notification_level : ``MessageNotificationLevel``, `int`, Optional (Keyword only)
            The default message notification level of the guild.
        
        description : `None`, `str`
            Description of the guild. The guild must be a Community guild.
        
        discovery_splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's discovery splash.
        
        explicit_content_filter_level : ``ExplicitContentFilterLevel``, `int`, Optional (Keyword only)
            The explicit content filter level of the guild.
        
        features : `None`, `iterable` of `(`int`, `GuildFeature``), Optional (Keyword only)
            The guild's features.
        
        home_splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's home splash.
        
        hub_type : ``HubType``, `int`, Optional (Keyword only)
            The guild's hub type.
        
        icon : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's icon.
        
        invite_splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's invite splash.
        
        locale : ``Locale``, `int`, Optional (Keyword only)
            The preferred language of the guild.
        
        mfa_level : ``MfaLevel``, `int`, Optional (Keyword only)
            The required multi-factor authentication level for the guild.
        
        name : `str`, Optional (Keyword only)
            The guild's name.
        
        nsfw_level : ``NsfwLevel``, `int`, Optional (Keyword only)
            The nsfw level of the guild.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The guild's owner or their id.
        
        public_updates_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's identifier where the guild's public updates should go.
        
        rules_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the rules of a public guild's should be.
        
        safety_alerts_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where safety alerts are sent by Discord.
        
        system_channel_flags : ``SystemChannelFlag``, `int`, Optional (Keyword only)
            Describe which type of messages are sent automatically to the system channel.
        
        system_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the system messages are sent.
        
        vanity_code : `None`, `str`, Optional (Keyword only)
            The guild's vanity invite's code if it has.
        
        verification_level : ``VerificationLevel``, `int`, Optional (Keyword only)
            The minimal verification needed to join or to interact with guild.
        
        widget_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier for which the guild's widget is for.
        
        widget_enabled : `bool`, Optional (Keyword only)
            Whether the guild's widget is enabled.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If any parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # afk_channel_id
        if afk_channel_id is ...:
            afk_channel_id = 0
        else:
            afk_channel_id = validate_afk_channel_id(afk_channel_id)
        
        # afk_timeout
        if afk_timeout is ...:
            afk_timeout = 0
        else:
            afk_timeout = validate_afk_timeout(afk_timeout)
        
        # banner
        if banner is ...:
            banner = None
        else:
            banner = cls.banner.validate_icon(banner, allow_data = True)
        
        # boost_progress_bar_enabled
        if boost_progress_bar_enabled is ...:
            boost_progress_bar_enabled = False
        else:
            boost_progress_bar_enabled = validate_boost_progress_bar_enabled(boost_progress_bar_enabled)
        
        # discovery_splash
        if discovery_splash is ...:
            discovery_splash = None
        else:
            discovery_splash = cls.discovery_splash.validate_icon(discovery_splash, allow_data = True)
        
        # default_message_notification_level
        if default_message_notification_level is ...:
            default_message_notification_level = MessageNotificationLevel.all_messages
        else:
            default_message_notification_level = validate_default_message_notification_level(default_message_notification_level)
        
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # explicit_content_filter_level
        if explicit_content_filter_level is ...:
            explicit_content_filter_level = ExplicitContentFilterLevel.disabled
        else:
            explicit_content_filter_level = validate_explicit_content_filter_level(explicit_content_filter_level)
        
        # features
        if features is ...:
            features = None
        else:
            features = validate_features(features)
        
        # home_splash
        if home_splash is ...:
            home_splash = None
        else:
            home_splash = cls.home_splash.validate_icon(home_splash, allow_data = True)
        
        # hub_type
        if hub_type is ...:
            hub_type = HubType.none
        else:
            hub_type = validate_hub_type(hub_type)
        
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon, allow_data = True)
        
        # invite_splash
        if invite_splash is ...:
            invite_splash = None
        else:
            invite_splash = cls.invite_splash.validate_icon(invite_splash, allow_data = True)
        
        # locale
        if locale is ...:
            locale = LOCALE_DEFAULT
        else:
            locale = validate_locale(locale)
        
        # mfa_level
        if mfa_level is ...:
            mfa_level = MfaLevel.none
        else:
            mfa_level = validate_mfa_level(mfa_level)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # nsfw_level
        if nsfw_level is ...:
            nsfw_level = NsfwLevel.none
        else:
            nsfw_level = validate_nsfw_level(nsfw_level)
        
        # owner_id
        if owner_id is ...:
            owner_id = 0
        else:
            owner_id = validate_owner_id(owner_id)
        
        # public_updates_channel_id
        if public_updates_channel_id is ...:
            public_updates_channel_id = 0
        else:
            public_updates_channel_id = validate_public_updates_channel_id(public_updates_channel_id)
        
        # safety_alerts_channel_id
        if safety_alerts_channel_id is ...:
            safety_alerts_channel_id = 0
        else:
            safety_alerts_channel_id = validate_safety_alerts_channel_id(safety_alerts_channel_id)
        
        # rules_channel_id
        if rules_channel_id is ...:
            rules_channel_id = 0
        else:
            rules_channel_id = validate_rules_channel_id(rules_channel_id)
        
        # system_channel_id
        if system_channel_id is ...:
            system_channel_id = 0
        else:
            system_channel_id = validate_system_channel_id(system_channel_id)
        
        # system_channel_flags
        if system_channel_flags is ...:
            system_channel_flags = SystemChannelFlag.NONE
        else:
            system_channel_flags = validate_system_channel_flags(system_channel_flags)
        
        # vanity_code
        if vanity_code is ...:
            vanity_code = None
        else:
            vanity_code = validate_vanity_code(vanity_code)
        
        # verification_level
        if verification_level is ...:
            verification_level = VerificationLevel.none
        else:
            verification_level = validate_verification_level(verification_level)
        
        # widget_channel_id
        if widget_channel_id is ...:
            widget_channel_id = 0
        else:
            widget_channel_id = validate_widget_channel_id(widget_channel_id)
        
        # widget_enabled
        if widget_enabled is ...:
            widget_enabled = False
        else:
            widget_enabled = validate_widget_enabled(widget_enabled)
        
        # Construct
        self = object.__new__(cls)
        self._cache_boosters = None
        self._cache_permission = None
        self._state = 0
        self.afk_channel_id = afk_channel_id
        self.afk_timeout = afk_timeout
        self.approximate_online_count = 0
        self.approximate_user_count = 0
        self.available = True
        self.banner = banner
        self.boost_count = 0
        self.boost_level = 0
        self.boost_progress_bar_enabled = boost_progress_bar_enabled
        self.channels = {}
        self.clients = []
        self.discovery_splash = discovery_splash
        self.default_message_notification_level = default_message_notification_level
        self.description = description
        self.embedded_activities = None
        self.emojis = {}
        self.explicit_content_filter_level = explicit_content_filter_level
        self.features = features
        self.home_splash = home_splash
        self.hub_type = hub_type
        self.icon = icon
        self.id = 0
        self.incidents = None
        self.inventory_settings = None
        self.invite_splash = invite_splash
        self.large = False
        self.locale = locale
        self.max_presences = MAX_PRESENCES_DEFAULT
        self.max_stage_channel_video_users = MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
        self.max_users = MAX_USERS_DEFAULT
        self.max_voice_channel_video_users = MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
        self.mfa_level = mfa_level
        self.name = name
        self.nsfw_level = nsfw_level
        self.owner_id = owner_id
        self.public_updates_channel_id = public_updates_channel_id
        self.safety_alerts_channel_id = safety_alerts_channel_id
        self.roles = {}
        self.rules_channel_id = rules_channel_id
        self.scheduled_events = None
        self.soundboard_sounds = None
        self.stages = None
        self.stickers = {}
        self.system_channel_id = system_channel_id
        self.system_channel_flags = system_channel_flags
        self.threads = None
        self.user_count = 0
        self.users = GUILD_USERS_TYPE()
        self.vanity_code = vanity_code
        self.verification_level = verification_level
        self.voice_states = None
        self.widget_channel_id = widget_channel_id
        self.widget_enabled = widget_enabled
        
        return self
    
    
    @classmethod
    def precreate(cls, guild_id, **keyword_parameters):
        """
        Precreates the guild with the given parameters. Precreated guilds are picked up when a guild's data is received
        with the same id.
        
        First tries to find whether a guild exists with the given id. If it does and it is partial, updates it with the
        given parameters, else it creates a new one.
        
        Parameters
        ----------
        guild_id : `snowflake`
            The guild's id.
        
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the guild.
        
        Other Parameters
        ----------------
        afk_channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `afk_channel_id`.
        
        afk_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The afk channel or its identifier.
        
        afk_timeout : `int`, Optional (Keyword only)
            The afk timeout at the `afk_channel`.
        
        approximate_online_count : `int`, Optional (Keyword only)
            The approximate amount of online users at the guild
        
        approximate_user_count : `int`, Optional (Keyword only)
            The approximate amount of users at the guild.
        
        available : `bool`, Optional (Keyword only)
            Whether the guild is available.
        
        banner : ``None | str | Icon``, Optional (Keyword only)
            The guild's banner.
        
        boost_count : `int`, Optional (Keyword only)
            The total number of boosts of the guild.
        
        boost_level : `int`, Optional (Keyword only)
            The boost level of the guild.
        
        boost_progress_bar_enabled : `bool`, Optional (Keyword only)
            Whether the guild has the boost progress bar enabled.
        
        channels : `None`, `iterable` of ``Channel``, `dict` of (`int`, ``Channel``) items, Optional (Keyword only)
            The channels of the guild.
        
        default_message_notification_level : ``MessageNotificationLevel``, `int`, Optional (Keyword only)
            The message notification level of the guild.
        
        description : `None`, `str`
            Description of the guild. The guild must be a Community guild.
        
        discovery_splash : ``None | str | Icon``, Optional (Keyword only)
            The guild's discovery splash.
        
        embedded_activities : `None`, `iterable` of ``EmbeddedActivity``, Optional (Keyword only)
            Embedded activity states to keep them alive in cache.
        
        emojis : `None`, `iterable` of ``Emoji``, `dict` of (`int`, ``Emoji``) items, Optional (Keyword only)
            The emojis of the guild.
        
        explicit_content_filter_level : ``ExplicitContentFilterLevel``, `int`, Optional (Keyword only)
            The explicit content filter level of the guild.
        
        features : `None`, `features` of `(`int`, `GuildFeature``), Optional (Keyword only)
            The guild's features.
        
        home_splash : ``None | str | Icon``, Optional (Keyword only)
            The guild's home splash.
        
        hub_type : ``HubType``, `int`, Optional (Keyword only)
            The guild's hub type.
        
        icon : ``None | str | Icon``, Optional (Keyword only)
            The guild's icon.
        
        incidents : `None`, ``GuildIncidents``, Optional (Keyword only)
            The guild's incidents.
        
        inventory_settings : `None`, ``GuildInventorySettings``, Optional (Keyword only)
            The guild's inventory settings.
        
        invite_splash : ``None | str | Icon``, Optional (Keyword only)
            The guild's invite splash.
        
        large : `bool`, Optional (Keyword only)
            Whether the guild is considered as a large one.
        
        locale : ``Locale``, `int`, Optional (Keyword only)
            The preferred language of the guild.
        
        max_presences : `int`, Optional (Keyword only)
            The maximal amount of presences for the guild.
        
        max_stage_channel_video_users : `int`, Optional (Keyword only)
            The maximal amount of users watching a video in a stage channel.
        
        max_users : `int`, Optional (Keyword only)
            The maximal allowed users in the guild.
        
        max_voice_channel_video_users : `int`, Optional (Keyword only)
            The maximal amount of users watching a video in a stage channel.
        
        mfa_level : ``MfaLevel``, `int`, Optional (Keyword only)
            The required multi-factor authentication level for the guild.
        
        name : `str`, Optional (Keyword only)
            The guild's name.
        
        nsfw_level : ``NsfwLevel``, `int`, Optional (Keyword only)
            The nsfw level of the guild.
        
        owner : `int`, ``ClientUserBase``, Optional (Keyword only)
            Alternative for `owner`.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The guild's owner or their id.
        
        public_updates_channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `public_updates_channel_id`.
        
        public_updates_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's identifier where the guild's public updates should go.
        
        roles : `None`, `iterable` of ``Role``, `dict` of (`int`, ``Role``) items, Optional (Keyword only)
            The roles of the guild.
        
        rules_channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `rules_channel_id`.
        
        rules_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the rules of a public guild's should be.
        
        safety_alerts_channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `safety_alerts_channel_id`.
        
        safety_alerts_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where safety alerts are sent by Discord.
        
        scheduled_events : `None`, `iterable` of ``ScheduledEvent``, `dict` of (`int`, ``ScheduledEvent``) items \
                , Optional (Keyword only)
            The scheduled events of the guild.
        
        soundboard_sounds : `None`, `iterable` of ``SoundboardSound``, `dict` of (`int`, ``SoundboardSound``) items \
                , Optional (Keyword only)
            The soundboard sounds of the guild.
        
        stages : `None`, `iterable` of ``Stage``, `dict` of (`int`, ``Stage``) items, Optional (Keyword only)
            Active stages of the guild.
            
            Defaults to `None` if would be empty.
        
        stickers : `None`, `iterable` of ``Sticker``, ``dict<int, Sticker>``, Optional (Keyword only)
            The stickers of the guild.
        
        system_channel_flags : ``SystemChannelFlag``, `int`, Optional (Keyword only)
            Describe which type of messages are sent automatically to the system channel.
        
        system_channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `system_channel_id`.
        
        system_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the system messages are sent.
        
        threads : `None`, `iterable` of ``Channel``, `dict` of (`int`, ``Channel``) items, Optional (Keyword only)
            The threads of the guild.
        
        user_count : `int`, Optional (Keyword only)
            The amount of users at the guild.
        
        users : `None`, `iterable` of ``ClientUserBase``, `dict` of (`int`, ``ClientUserBase``) items \
                , Optional (Keyword only)
            The users of the guild.
        
        vanity_code : `None`, `str`, Optional (Keyword only)
            The guild's vanity invite's code if it has.
        
        verification_level : ``VerificationLevel``, `int`, Optional (Keyword only)
            The minimal verification needed to join or to interact with guild.
        
        voice_states : `None`, `iterable` of ``VoiceState``, `dict` of (`int`, ``VoiceState``) items \
                , Optional (Keyword only)
            The users represented in the guild's voice channels.
        
        widget_channel : `int`, ``Channel``, Optional (Keyword only)
            Alternative for `widget_channel_id`.
        
        widget_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier for which the guild's widget is for.
        
        widget_enabled : `bool`, Optional (Keyword only)
            Whether the guild's widget is enabled.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If any parameter's type is incorrect.
            - Extra parameters given.
        ValueError
            - If a parameter's value is incorrect.
        """
        guild_id = validate_id(guild_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = GUILDS[guild_id]
        except KeyError:
            self = cls._create_empty(guild_id)
            GUILDS[guild_id] = self
        else:
            if self.clients:
                return self
        
        if (processed is not None):
            for item in processed:
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
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._cache_boosters = None
        self._cache_permission = None
        self._state = 0
        self.afk_channel_id = 0
        self.afk_timeout = 0
        self.approximate_online_count = 0
        self.approximate_user_count = 0
        self.available = True
        self.banner_hash = 0
        self.banner_type = ICON_TYPE_NONE
        self.boost_count = 0
        self.boost_progress_bar_enabled = False
        self.channels = {}
        self.clients = []
        self.default_message_notification_level = MessageNotificationLevel.all_messages
        self.description = None
        self.discovery_splash_hash = 0
        self.discovery_splash_type = ICON_TYPE_NONE
        self.embedded_activities = None
        self.emojis = {}
        self.explicit_content_filter_level = ExplicitContentFilterLevel.disabled
        self.features = None
        self.home_splash_hash = 0
        self.home_splash_type = ICON_TYPE_NONE
        self.hub_type = HubType.none
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        self.incidents = None
        self.inventory_settings = None
        self.id = guild_id
        self.invite_splash_hash = 0
        self.invite_splash_type = ICON_TYPE_NONE
        self.large = False
        self.locale = LOCALE_DEFAULT
        self.max_presences = MAX_PRESENCES_DEFAULT
        self.max_stage_channel_video_users = MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
        self.max_users = MAX_USERS_DEFAULT
        self.max_voice_channel_video_users = MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
        self.mfa_level = MfaLevel.none
        self.name = ''
        self.nsfw_level = NsfwLevel.none
        self.owner_id = 0
        self.boost_level = 0
        self.public_updates_channel_id = 0
        self.safety_alerts_channel_id = 0
        self.roles = {}
        self.rules_channel_id = 0
        self.scheduled_events = None
        self.soundboard_sounds = None
        self.stages = None
        self.stickers = {}
        self.system_channel_id = 0
        self.system_channel_flags = SystemChannelFlag.NONE
        self.threads = None
        self.user_count = 0
        self.users = GUILD_USERS_TYPE()
        self.vanity_code = None
        self.verification_level = VerificationLevel.none
        self.voice_states = None
        self.widget_channel_id = 0
        self.widget_enabled = False
        return self
    
    
    @classmethod
    def from_data(cls, data, client = None):
        """
        Tries to find the guild from the already existing ones. If it can not find, creates a new one. If the found
        guild is partial (or freshly created), sets it's attributes from the given `data`. If the the guild is not
        added to the client's guild profiles yet, adds it, and the client to the guilds' `.clients` as well.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received guild data.
        client : `None`, ``Client`` = `None`, Optional
            The client who received the guild's data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        guild_id = parse_id(data)
        
        try:
            self = GUILDS[guild_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = guild_id
            self._set_attributes(data, True)
            GUILDS[guild_id] = self
        else:
            if self.clients:
                # Update just available
                self.available = parse_available(data)
            else:
                self._set_attributes(data, False)
        
        self.users = parse_client_guild_profile(data, self.users, guild_id)
        
        if (client is not None) and (client not in self.clients):
            ghost_state = self.get_voice_state(client.id)
            if (ghost_state is not None):
                trigger_voice_client_ghost_event(client, ghost_state)
            
            self.clients.append(client)
            client.guilds.add(self)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the guild to its json representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, str>`
        """
        data = {}
        
        put_afk_channel_id(self.afk_channel_id, data, defaults)
        put_afk_timeout(self.afk_timeout, data, defaults)
        put_boost_progress_bar_enabled(self.boost_progress_bar_enabled, data, defaults)
        put_default_message_notification_level(self.default_message_notification_level, data, defaults)
        put_description(self.description, data, defaults)
        put_explicit_content_filter_level(self.explicit_content_filter_level, data, defaults)
        put_features(self.features, data, defaults)
        put_hub_type(self.hub_type, data, defaults)
        put_mfa_level(self.mfa_level, data, defaults)
        put_name(self.name, data, defaults)
        put_nsfw_level(self.nsfw_level, data, defaults)
        put_owner_id(self.owner_id, data, defaults)
        put_locale(self.locale, data, defaults)
        put_public_updates_channel_id(self.public_updates_channel_id, data, defaults)
        put_rules_channel_id(self.rules_channel_id, data, defaults)
        put_safety_alerts_channel_id(self.safety_alerts_channel_id, data, defaults)
        put_system_channel_flags(self.system_channel_flags, data, defaults)
        put_system_channel_id(self.system_channel_id, data, defaults)
        put_vanity_code(self.vanity_code, data, defaults)
        put_verification_level(self.verification_level, data, defaults)
        put_widget_channel_id(self.widget_channel_id, data, defaults)
        put_widget_enabled(self.widget_enabled, data, defaults)
        
        type(self).banner.put_into(self.banner, data, defaults, as_data = not include_internals)
        type(self).discovery_splash.put_into(self.discovery_splash, data, defaults, as_data = not include_internals)
        type(self).home_splash.put_into(self.home_splash, data, defaults, as_data = not include_internals)
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        type(self).invite_splash.put_into(self.invite_splash, data, defaults, as_data = not include_internals)
        
        if include_internals:
            put_approximate_online_count(self.approximate_online_count, data, defaults)
            put_approximate_user_count(self.approximate_user_count, data, defaults)
            put_available(self.available, data, defaults)
            put_boost_count(self.boost_count, data, defaults)
            put_boost_level(self.boost_level, data, defaults)
            put_channels(self.channels, data, defaults)
            put_embedded_activities(self.embedded_activities, data, defaults)
            put_emojis(self.emojis, data, defaults)
            put_incidents(self.incidents, data, defaults)
            put_inventory_settings(self.inventory_settings, data, defaults)
            put_id(self.id, data, defaults)
            put_large(self.large, data, defaults)
            put_max_presences(self.max_presences, data, defaults)
            put_max_stage_channel_video_users(self.max_stage_channel_video_users, data, defaults)
            put_max_users(self.max_users, data, defaults)
            put_max_voice_channel_video_users(self.max_voice_channel_video_users, data, defaults)
            put_roles(self.roles, data, defaults)
            put_scheduled_events(self.scheduled_events, data, defaults)
            put_soundboard_sounds(self.soundboard_sounds, data, defaults)
            put_stages(self.stages, data, defaults)
            put_stickers(self.stickers, data, defaults)
            put_threads(self.threads, data, defaults)
            put_user_count(self.user_count, data, defaults)
            put_users(self.users, data, defaults, guild_id = self.id)
            put_voice_states(self.voice_states, data, defaults)
        
        return data
    
    
    def _set_attributes(self, data, creation):
        """
        Finishes the guild's initialization process by setting it's attributes.
         
        > This method required `.id` to be set already.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild data.
        creation : `bool`
            Whether the entity was just created.
        """
        guild_id = self.id
        
        self.available = parse_available(data)
        
        user_count = parse_user_count(data)
        self.user_count = user_count or 1
        
        if creation:
            # Set cache
            self._cache_boosters = None
            self._cache_permission = None
            self._state = 0
            
            # Set fields
            self.approximate_online_count = 0
            self.approximate_user_count = 0
            self.clients = []
            
            # Set entity fields
            self.channels = parse_channels(data, {}, guild_id)
            self.embedded_activities = parse_embedded_activities(data, None, guild_id)
            self.emojis = parse_emojis(data, {}, guild_id)
            self.large = parse_large(data) or (user_count >= LARGE_GUILD_LIMIT)
            self.roles = parse_roles(data, {}, guild_id)
            self.scheduled_events = parse_scheduled_events(data, None)
            self.soundboard_sounds = parse_soundboard_sounds(data, None)
            self.stages = parse_stages(data, None)
            self.stickers = parse_stickers(data, {})
            self.threads = parse_threads(data, None, guild_id)
            self.users = parse_users(data, GUILD_USERS_TYPE(), guild_id)
            self.voice_states = parse_voice_states(data, None, guild_id)
            
        else:
            # Clear permission cache
            self._cache_permission = None
            
            # Update fields.
            self.channels = parse_channels(data, self.channels, guild_id)
            self.embedded_activities = parse_embedded_activities(
                data, self.embedded_activities, guild_id
            )
            self.emojis = parse_emojis(data, self.emojis, guild_id)
            self.large = parse_large(data) or (user_count >= LARGE_GUILD_LIMIT)
            self.roles = parse_roles(data, self.roles, guild_id)
            self.scheduled_events = parse_scheduled_events(data, self.scheduled_events)
            self.soundboard_sounds = parse_soundboard_sounds(data, self.soundboard_sounds)
            self.stages = parse_stages(data, self.stages)
            self.stickers = parse_stickers(data, self.stickers)
            self.threads = parse_threads(data, self.threads, guild_id)
            self.users = parse_users(data, self.users, guild_id)
            self.voice_states = parse_voice_states(data, self.voice_states, guild_id)
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the guild and with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild data received from Discord.
        """
        # Clear generic cache.
        self._clear_cache()
        
        self.afk_channel_id = parse_afk_channel_id(data)
        self.afk_timeout = parse_afk_timeout(data)
        self.available = parse_available(data)
        self._set_banner(data)
        self.boost_count = parse_boost_count(data)
        self.boost_level = parse_boost_level(data)
        self.boost_progress_bar_enabled = parse_boost_progress_bar_enabled(data)
        self.default_message_notification_level = parse_default_message_notification_level(data)
        self.description = parse_description(data)
        self._set_discovery_splash(data)
        self.explicit_content_filter_level = parse_explicit_content_filter_level(data)
        self.features = parse_features(data)
        self._set_home_splash(data)
        self.hub_type = parse_hub_type(data)
        self._set_icon(data)
        self.incidents = parse_incidents(data)
        self.inventory_settings = parse_inventory_settings(data)
        self._set_invite_splash(data)
        self.max_presences = parse_max_presences(data)
        self.max_stage_channel_video_users = parse_max_stage_channel_video_users(data)
        self.max_users = parse_max_users(data)
        self.max_voice_channel_video_users = parse_max_voice_channel_video_users(data)
        self.mfa_level = parse_mfa_level(data)
        self.name = parse_name(data)
        self.nsfw_level = parse_nsfw_level(data)
        self.owner_id = parse_owner_id(data)
        self.locale = parse_locale(data)
        self.public_updates_channel_id = parse_public_updates_channel_id(data)
        self.rules_channel_id = parse_rules_channel_id(data)
        self.safety_alerts_channel_id = parse_safety_alerts_channel_id(data)
        self.system_channel_flags = parse_system_channel_flags(data)
        self.system_channel_id = parse_system_channel_id(data)
        self.vanity_code = parse_vanity_code(data)
        self.verification_level = parse_verification_level(data)
        self.widget_channel_id = parse_widget_channel_id(data)
        self.widget_enabled = parse_widget_enabled(data)
        
        self._update_counts_only(data)
    
    
    def _update_counts_only(self, data):
        """
        Updates the guilds' counts if given.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received guild data.
        """
        approximate_online_count = parse_approximate_online_count(data)
        if approximate_online_count:
            self.approximate_online_count = approximate_online_count
        
        approximate_user_count = parse_approximate_user_count(data)
        if approximate_user_count:
            self.approximate_user_count = approximate_user_count
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the guild and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild data received from Discord.
        
        Returns
        -------
        old_attributes : `dict<str, object>`
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +---------------------------------------+---------------------------------------+
        | Keys                                  | Values                                |
        +========================================+=======================================+
        | afk_channel_id                        | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | afk_timeout                           | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | available                             | `bool`                                |
        +---------------------------------------+---------------------------------------+
        | banner                                | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | boost_count                           | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | boost_level                           | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | boost_progress_bar_enabled            | `bool`                                |
        +---------------------------------------+---------------------------------------+
        | explicit_content_filter_level         | ``ExplicitContentFilterLevel``        |
        +---------------------------------------+---------------------------------------+
        | default_message_notification_level    | ``MessageNotificationLevel``          |
        +---------------------------------------+---------------------------------------+
        | description                           | `None`, `str`                         |
        +---------------------------------------+---------------------------------------+
        | discovery_splash                      | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | features                              | `None`, `tuple` of ``GuildFeature``   |
        +---------------------------------------+---------------------------------------+
        | home_splash                           | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | hub_type                              | ``HubType``                           |
        +---------------------------------------+---------------------------------------+
        | icon                                  | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | incidents                             | `None`, ``GuildIncidents``            |
        +---------------------------------------+---------------------------------------+
        | inventory_settings                    | `None`, ``GuildInventorySettings``    |
        +---------------------------------------+---------------------------------------+
        | invite_splash                         | ``Icon``                              |
        +---------------------------------------+---------------------------------------+
        | max_presences                         | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | max_stage_channel_video_users         | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | max_users                             | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | max_voice_channel_video_users         | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | mfa_level                             | ``MfaLevel``                          |
        +---------------------------------------+---------------------------------------+
        | name                                  | `str`                                 |
        +---------------------------------------+---------------------------------------+
        | nsfw_level                            | ``NsfwLevel``                         |
        +---------------------------------------+---------------------------------------+
        | owner_id                              | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | locale                                | ``Locale``                            |
        +---------------------------------------+---------------------------------------+
        | public_updates_channel_id             | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | rules_channel_id                      | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | safety_alerts_channel_id              | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | system_channel_id                     | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | system_channel_flags                  | ``SystemChannelFlag``                 |
        +---------------------------------------+---------------------------------------+
        | vanity_code                           | `None`, `str`                         |
        +---------------------------------------+---------------------------------------+
        | verification_level                    | ``VerificationLevel``                 |
        +---------------------------------------+---------------------------------------+
        | widget_channel_id                     | `int`                                 |
        +---------------------------------------+---------------------------------------+
        | widget_enabled                        | `bool`                                |
        +---------------------------------------+---------------------------------------+
        """
        # Clear generic cache.
        self._clear_cache()
        
        old_attributes = {}
        
        # afk_channel_id
        afk_channel_id = parse_afk_channel_id(data)
        if self.afk_channel_id != afk_channel_id:
            old_attributes['afk_channel_id'] = self.afk_channel_id
            self.afk_channel_id = afk_channel_id
        
        # afk_timeout
        afk_timeout = parse_afk_timeout(data)
        if self.afk_timeout != afk_timeout:
            old_attributes['afk_timeout'] = self.afk_timeout
            self.afk_timeout = afk_timeout
        
        # available
        available = parse_available(data)
        if self.available != available:
            old_attributes['available'] = self.available
            self.available = available
        
        # banner
        self._update_banner(data, old_attributes)
        
        # boost_count
        boost_count = parse_boost_count(data)
        if self.boost_count != boost_count:
            old_attributes['boost_count'] = self.boost_count
            self.boost_count = boost_count
        
        # boost_level
        boost_level = parse_boost_level(data)
        if self.boost_level != boost_level:
            old_attributes['boost_level'] = self.boost_level
            self.boost_level = boost_level
        
        # boost_progress_bar_enabled
        boost_progress_bar_enabled = parse_boost_progress_bar_enabled(data)
        if self.boost_progress_bar_enabled != boost_progress_bar_enabled:
            old_attributes['boost_progress_bar_enabled'] = self.boost_progress_bar_enabled
            self.boost_progress_bar_enabled = boost_progress_bar_enabled
        
        # default_message_notification_level
        default_message_notification_level = parse_default_message_notification_level(data)
        if self.default_message_notification_level is not default_message_notification_level:
            old_attributes['default_message_notification_level'] = self.default_message_notification_level
            self.default_message_notification_level = default_message_notification_level
        
        # description
        description = parse_description(data)
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        # discovery_splash
        self._update_discovery_splash(data, old_attributes)
        
        # explicit_content_filter_level
        explicit_content_filter_level = parse_explicit_content_filter_level(data)
        if self.explicit_content_filter_level is not explicit_content_filter_level:
            old_attributes['explicit_content_filter_level'] = self.explicit_content_filter_level
            self.explicit_content_filter_level = explicit_content_filter_level
        
        # features
        features = parse_features(data)
        if self.features != features:
            old_attributes['features'] = self.features
            self.features = features
        
        # home_splash
        self._update_home_splash(data, old_attributes)
        
        # hub_type
        hub_type = parse_hub_type(data)
        if self.hub_type is not hub_type:
            old_attributes['hub_type'] = self.hub_type
            self.hub_type = hub_type
        
        # icon
        self._update_icon(data, old_attributes)
        
        # incidents
        incidents = parse_incidents(data)
        if self.incidents != incidents:
            old_attributes['incidents'] = self.incidents
            self.incidents = incidents
        
        # inventory_settings
        inventory_settings = parse_inventory_settings(data)
        if self.inventory_settings != inventory_settings:
            old_attributes['inventory_settings'] = self.inventory_settings
            self.inventory_settings = inventory_settings
        
        # invite_splash
        self._update_invite_splash(data, old_attributes)
        
        # max_presences
        max_presences = parse_max_presences(data)
        if self.max_presences != max_presences:
            old_attributes['max_presences'] = self.max_presences
            self.max_presences = max_presences
        
        # max_stage_channel_video_users
        max_stage_channel_video_users = parse_max_stage_channel_video_users(data)
        if self.max_stage_channel_video_users != max_stage_channel_video_users:
            old_attributes['max_stage_channel_video_users'] = self.max_stage_channel_video_users
            self.max_stage_channel_video_users = max_stage_channel_video_users
        
        # max_users
        max_users = parse_max_users(data)
        if self.max_users != max_users:
            old_attributes['max_users'] = self.max_users
            self.max_users = max_users
        
        # max_voice_channel_video_users
        max_voice_channel_video_users = parse_max_voice_channel_video_users(data)
        if self.max_voice_channel_video_users != max_voice_channel_video_users:
            old_attributes['max_voice_channel_video_users'] = self.max_voice_channel_video_users
            self.max_voice_channel_video_users = max_voice_channel_video_users
        
        # mfa_level
        mfa_level = parse_mfa_level(data)
        if self.mfa_level is not mfa_level:
            old_attributes['mfa_level'] = self.mfa_level
            self.mfa_level = mfa_level
        
        # name
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # nsfw_level
        nsfw_level = parse_nsfw_level(data)
        if self.nsfw_level is not nsfw_level:
            old_attributes['nsfw_level'] = self.nsfw_level
            self.nsfw_level = nsfw_level
        
        # owner_id
        owner_id = parse_owner_id(data)
        if self.owner_id != owner_id:
            old_attributes['owner_id'] = self.owner_id
            self.owner_id = owner_id
        
        # locale
        locale = parse_locale(data)
        if self.locale is not locale:
            old_attributes['locale'] = self.locale
            self.locale = locale
        
        # public_updates_channel_id
        public_updates_channel_id = parse_public_updates_channel_id(data)
        if self.public_updates_channel_id !=  public_updates_channel_id:
            old_attributes['public_updates_channel_id'] = self.public_updates_channel_id
            self.public_updates_channel_id = public_updates_channel_id
        
        # rules_channel_id
        rules_channel_id = parse_rules_channel_id(data)
        if self.rules_channel_id != rules_channel_id:
            old_attributes['rules_channel_id'] = self.rules_channel_id
            self.rules_channel_id = rules_channel_id
        
        # safety_alerts_channel_id
        safety_alerts_channel_id = parse_safety_alerts_channel_id(data)
        if self.safety_alerts_channel_id != safety_alerts_channel_id:
            old_attributes['safety_alerts_channel_id'] = self.safety_alerts_channel_id
            self.safety_alerts_channel_id = safety_alerts_channel_id
        
        # system_channel_flags
        system_channel_flags = parse_system_channel_flags(data)
        if self.system_channel_flags != system_channel_flags:
            old_attributes['system_channel_flags'] = self.system_channel_flags
            self.system_channel_flags = system_channel_flags
        
        # system_channel_id
        system_channel_id = parse_system_channel_id(data)
        if self.system_channel_id != system_channel_id:
            old_attributes['system_channel_id'] = self.system_channel_id
            self.system_channel_id = system_channel_id
        
        # vanity_code
        vanity_code = parse_vanity_code(data)
        if self.vanity_code != vanity_code:
            old_attributes['vanity_code'] = self.vanity_code
            self.vanity_code = vanity_code
        
        # verification_level
        verification_level = parse_verification_level(data)
        if self.verification_level is not verification_level:
            old_attributes['verification_level'] = self.verification_level
            self.verification_level = verification_level
        
        # widget_channel_id
        widget_channel_id = parse_widget_channel_id(data)
        if self.widget_channel_id != widget_channel_id:
            old_attributes['widget_channel_id'] = self.widget_channel_id
            self.widget_channel_id = widget_channel_id
        
        # widget_enabled
        widget_enabled = parse_widget_enabled(data)
        if self.widget_enabled != widget_enabled:
            old_attributes['widget_enabled'] = self.widget_enabled
            self.widget_enabled = widget_enabled
        
        self._update_counts_only(data)
        
        return old_attributes
    
    
    def __repr__(self):
        """Returns the guild's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
        ]
        
        guild_id = self.id
        if guild_id:
            repr_parts.append(' id = ')
            repr_parts.append(str(guild_id))
            
            field_added = True
        else:
            field_added = False
        
        if self.partial:
            if field_added:
                repr_parts.append(' (partial)')
            else:
                repr_parts.append(' partial')
                field_added = True
        
        name = self.name
        if name:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' name = ')
            repr_parts.append(repr(name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
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
        >>> guild = Guild.precreate(now_as_id(), name = 'GrassGrass')
        >>> guild
        <Guild id = 713718885970345984 (partial), name = 'GrassGrass'>
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
    
    
    def __eq__(self, other):
        """Returns whether the two guilds are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id == other_id
        
        return self._is_equal_partial(other)
    
    
    def __ne__(self, other):
        """Returns whether the two guilds are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id != other_id
        
        return not self._is_equal_partial(other)
    

    def _is_equal_partial(self, other):
        """
        Returns whether the guild is equal to the given one.
        This function is called when one or both the guilds are templates.
        
        Parameters
        ----------
        other : ``instance<type<self>>``
            The other guild to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        # afk_channel_id
        if self.afk_channel_id != other.afk_channel_id:
            return False
        
        # afk_timeout
        if self.afk_timeout != other.afk_timeout:
            return False
        
        # banner
        if self.banner != other.banner:
            return False
        
        # boost_progress_bar_enabled
        if self.boost_progress_bar_enabled != other.boost_progress_bar_enabled:
            return False
        
        # discovery_splash
        if self.discovery_splash != other.discovery_splash:
            return False
        
        # default_message_notification_level
        if self.default_message_notification_level is not other.default_message_notification_level:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # explicit_content_filter_level
        if self.explicit_content_filter_level is not other.explicit_content_filter_level:
            return False
        
        # features
        if self.features != other.features:
            return False
        
        # home_splash
        if self.home_splash != other.home_splash:
            return False
        
        # hub_type
        if self.hub_type is not other.hub_type:
            return False
        
        # icon
        if self.icon != other.icon:
            return False
        
        # invite_splash
        if self.invite_splash != other.invite_splash:
            return False
        
        # mfa_level
        if self.mfa_level != other.mfa_level:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # nsfw_level
        if self.nsfw_level is not other.nsfw_level:
            return False
        
        # owner_id
        if self.owner_id != other.owner_id:
            return False
        
        # locale
        if self.locale is not other.locale:
            return False
        
        # public_updates_channel_id
        if self.public_updates_channel_id != other.public_updates_channel_id:
            return False
        
        # safety_alerts_channel_id
        if self.safety_alerts_channel_id != other.safety_alerts_channel_id:
            return False
        
        # rules_channel_id
        if self.rules_channel_id != other.rules_channel_id:
            return False
        
        # system_channel_id
        if self.system_channel_id != other.system_channel_id:
            return False
        
        # system_channel_flags
        if self.system_channel_flags != other.system_channel_flags:
            return False
        
        # vanity_code
        if self.vanity_code != other.vanity_code:
            return False
        
        # verification_level
        if self.verification_level is not other.verification_level:
            return False
        
        # widget_channel_id
        if self.widget_channel_id != other.widget_channel_id:
            return False
        
        # widget_enabled
        if self.widget_enabled != other.widget_enabled:
            return False
        
        return True
    
    
    def __hash__(self):
        guild_id = self.id
        if guild_id:
            return guild_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Hashes the fields of the guild.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # afk_channel_id
        afk_channel_id = self.afk_channel_id
        if afk_channel_id:
            hash_value ^= 1 << 0
            hash_value ^= afk_channel_id
        
        # afk_timeout
        hash_value ^= self.afk_timeout
        
        # banner
        banner = self.banner
        if banner:
            hash_value ^= 1 << 1
            hash_value ^= hash(banner)
        
        # boost_progress_bar_enabled
        hash_value ^= self.boost_progress_bar_enabled << 2
        
        # discovery_splash
        discovery_splash = self.discovery_splash
        if discovery_splash:
            hash_value ^= 1 << 3
            hash_value ^= hash(discovery_splash)
        
        # default_message_notification_level
        hash_value ^= self.default_message_notification_level.value << 16
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # explicit_content_filter_level
        hash_value ^= self.explicit_content_filter_level.value << 10
        
        # features
        features = self.features
        if (features is not None):
            hash_value ^= len(features) << 12
            
            for feature in features:
                hash_value^= hash(feature)
        
        # home_splash
        home_splash = self.home_splash
        if home_splash:
            hash_value ^= 1 << 25
            hash_value ^= hash(home_splash)
        
        # hub_type
        hash_value ^= self.hub_type.value << 14
        
        # icon
        icon = self.icon
        if icon:
            hash_value ^= 1 << 4
            hash_value ^= hash(icon)
        
        # invite_splash
        invite_splash = self.invite_splash
        if invite_splash:
            hash_value ^= 1 << 5
            hash_value ^= hash(invite_splash)
        
        # mfa_level
        hash_value ^= self.mfa_level.value << 18
        
        # name
        name = self.name
        if (description is None) or (description != name):
            hash_value ^= hash(name)
        
        # nsfw_level
        hash_value ^= self.nsfw_level.value << 20
        
        # owner_id
        owner_id = self.owner_id
        if owner_id:
            hash_value ^= 1 << 6
            hash_value ^= owner_id
        
        # locale
        hash_value ^= hash(self.locale)
        
        # public_updates_channel_id
        public_updates_channel_id = self.public_updates_channel_id
        if public_updates_channel_id:
            hash_value ^= 1 << 7
            hash_value ^= public_updates_channel_id
        
        # safety_alerts_channel_id
        safety_alerts_channel_id = self.safety_alerts_channel_id
        if safety_alerts_channel_id:
            hash_value ^= 1 << 8
            hash_value ^= safety_alerts_channel_id
        
        # rules_channel_id
        rules_channel_id = self.rules_channel_id
        if rules_channel_id:
            hash_value ^= 1 << 9
            hash_value ^= rules_channel_id
        
        # system_channel_id
        system_channel_id = self.system_channel_id
        if system_channel_id:
            hash_value ^= 1 << 10
            hash_value ^= system_channel_id
        
        # system_channel_flags
        hash_value ^= self.system_channel_flags << 22
        
        # vanity_code
        vanity_code = self.vanity_code
        if (vanity_code is not None):
            hash_value ^= hash(vanity_code)
        
        # verification_level
        hash_value ^= self.verification_level.value << 24
        
        # widget_channel_id
        widget_channel_id = self.widget_channel_id
        if widget_channel_id:
            hash_value ^= 1 << 11
            hash_value ^= widget_channel_id
        
        # widget_enabled
        hash_value ^= self.widget_enabled << 12
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the guild.
        
        Returns
        -------
        new : `instance<type<cls>>`
        """
        new = object.__new__(type(self))
        new._cache_boosters = None
        new._cache_permission = None
        new._state = 0
        new.afk_channel_id = self.afk_channel_id
        new.afk_timeout = self.afk_timeout
        new.approximate_online_count = 0
        new.approximate_user_count = 0
        new.available = True
        new.banner = self.banner
        new.boost_count = 0
        new.boost_progress_bar_enabled = self.boost_progress_bar_enabled
        new.channels = {}
        new.clients = []
        new.default_message_notification_level = self.default_message_notification_level
        new.description = self.description
        new.discovery_splash = self.discovery_splash
        new.embedded_activities = None
        new.emojis = {}
        new.explicit_content_filter_level = self.explicit_content_filter_level
        features = self.features
        if (features is not None):
            features = (*features,)
        new.features = features
        new.home_splash = self.home_splash
        new.hub_type = self.hub_type
        new.icon = self.icon
        new.id = 0
        new.incidents = None
        new.inventory_settings = None
        new.invite_splash = self.invite_splash
        new.large = False
        new.max_presences = MAX_PRESENCES_DEFAULT
        new.max_stage_channel_video_users = MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
        new.max_users = MAX_USERS_DEFAULT
        new.max_voice_channel_video_users = MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
        new.mfa_level = self.mfa_level
        new.name = self.name
        new.nsfw_level = self.nsfw_level
        new.owner_id = self.owner_id
        new.locale = self.locale
        new.boost_level = 0
        new.public_updates_channel_id = self.public_updates_channel_id
        new.safety_alerts_channel_id = self.safety_alerts_channel_id
        new.roles = {}
        new.rules_channel_id = self.rules_channel_id
        new.scheduled_events = None
        new.soundboard_sounds = None
        new.stages = None
        new.stickers = {}
        new.system_channel_id = self.system_channel_id
        new.system_channel_flags = self.system_channel_flags
        new.threads = None
        new.user_count = 0
        new.users = GUILD_USERS_TYPE()
        new.vanity_code = self.vanity_code
        new.verification_level = self.verification_level
        new.voice_states = None
        new.widget_channel_id = self.widget_channel_id
        new.widget_enabled = self.widget_enabled
        
        return new
    
    
    def copy_with(
        self,
        afk_channel_id = ...,
        afk_timeout = ...,
        banner = ...,
        boost_progress_bar_enabled = ...,
        default_message_notification_level = ...,
        description = ...,
        discovery_splash = ...,
        explicit_content_filter_level = ...,
        features = ...,
        home_splash = ...,
        hub_type = ...,
        icon = ...,
        invite_splash = ...,
        locale = ...,
        mfa_level = ...,
        name = ...,
        nsfw_level = ...,
        owner_id = ...,
        public_updates_channel_id = ...,
        safety_alerts_channel_id = ...,
        rules_channel_id = ...,
        system_channel_id = ...,
        system_channel_flags = ...,
        vanity_code = ...,
        verification_level = ...,
        widget_channel_id = ...,
        widget_enabled = ...,
    ):
        """
        Copies the guild with the given fields.
        
        Parameters
        ----------
        afk_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The afk channel or its identifier.
        
        afk_timeout : `int`, Optional (Keyword only)
            The afk timeout at the `afk_channel`.
        
        banner : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's banner.
        
        boost_progress_bar_enabled : `bool`, Optional (Keyword only)
            Whether the guild has the boost progress bar enabled.
        
        default_message_notification_level : ``MessageNotificationLevel``, `int`, Optional (Keyword only)
            The message notification level of the guild.
        
        description : `None`, `str`
            Description of the guild. The guild must be a Community guild.
        
        discovery_splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's discovery splash.
        
        explicit_content_filter_level : ``ExplicitContentFilterLevel``, `int`, Optional (Keyword only)
            The explicit content filter level of the guild.
        
        features : `None`, `iterable` of `(`int`, `GuildFeature``), Optional (Keyword only)
            The guild's features.
        
        home_splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's home splash.
        
        hub_type : ``HubType``, `int`, Optional (Keyword only)
            The guild's hub type.
        
        icon : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's icon.
        
        invite_splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The guild's invite splash.
        
        locale : ``Locale``, `int`, Optional (Keyword only)
            The preferred language of the guild.
        
        mfa_level : ``MfaLevel``, `int`, Optional (Keyword only)
            The required multi-factor authentication level for the guild.
        
        name : `str`, Optional (Keyword only)
            The guild's name.
        
        nsfw_level : ``NsfwLevel``, `int`, Optional (Keyword only)
            The nsfw level of the guild.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The guild's owner or their id.
        
        public_updates_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's identifier where the guild's public updates should go.
        
        rules_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the rules of a public guild's should be.
        
        safety_alerts_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where safety alerts are sent by Discord.
        
        system_channel_flags : ``SystemChannelFlag``, `int`, Optional (Keyword only)
            Describe which type of messages are sent automatically to the system channel.
        
        system_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the system messages are sent.
        
        vanity_code : `None`, `str`, Optional (Keyword only)
            The guild's vanity invite's code if it has.
        
        verification_level : ``VerificationLevel``, `int`, Optional (Keyword only)
            The minimal verification needed to join or to interact with guild.
        
        widget_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier for which the guild's widget is for.
        
        widget_enabled : `bool`, Optional (Keyword only)
            Whether the guild's widget is enabled.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If any parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # afk_channel_id
        if afk_channel_id is ...:
            afk_channel_id = self.afk_channel_id
        else:
            afk_channel_id = validate_afk_channel_id(afk_channel_id)
        
        # afk_timeout
        if afk_timeout is ...:
            afk_timeout = self.afk_timeout
        else:
            afk_timeout = validate_afk_timeout(afk_timeout)
        
        # banner
        if banner is ...:
            banner = self.banner
        else:
            banner = type(self).banner.validate_icon(banner, allow_data = True)
        
        # boost_progress_bar_enabled
        if boost_progress_bar_enabled is ...:
            boost_progress_bar_enabled = self.boost_progress_bar_enabled
        else:
            boost_progress_bar_enabled = validate_boost_progress_bar_enabled(boost_progress_bar_enabled)
        
        # discovery_splash
        if discovery_splash is ...:
            discovery_splash = self.discovery_splash
        else:
            discovery_splash = type(self).discovery_splash.validate_icon(discovery_splash, allow_data = True)
        
        # default_message_notification_level
        if default_message_notification_level is ...:
            default_message_notification_level = self.default_message_notification_level
        else:
            default_message_notification_level = validate_default_message_notification_level(default_message_notification_level)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # explicit_content_filter_level
        if explicit_content_filter_level is ...:
            explicit_content_filter_level = self.explicit_content_filter_level
        else:
            explicit_content_filter_level = validate_explicit_content_filter_level(explicit_content_filter_level)
        
        # features
        if features is ...:
            features = self.features
            if (features is not None):
                features = (*(feature for feature in features),)
        else:
            features = validate_features(features)
        
        # home_splash
        if home_splash is ...:
            home_splash = self.home_splash
        else:
            home_splash = type(self).home_splash.validate_icon(home_splash, allow_data = True)
        
        # hub_type
        if hub_type is ...:
            hub_type = self.hub_type
        else:
            hub_type = validate_hub_type(hub_type)
        
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon, allow_data = True)
        
        # invite_splash
        if invite_splash is ...:
            invite_splash = self.invite_splash
        else:
            invite_splash = type(self).invite_splash.validate_icon(invite_splash, allow_data = True)
        
        # locale
        if locale is ...:
            locale = self.locale
        else:
            locale = validate_locale(locale)
        
        # mfa_level
        if mfa_level is ...:
            mfa_level = self.mfa_level
        else:
            mfa_level = validate_mfa_level(mfa_level)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # nsfw_level
        if nsfw_level is ...:
            nsfw_level = self.nsfw_level
        else:
            nsfw_level = validate_nsfw_level(nsfw_level)
        
        # owner_id
        if owner_id is ...:
            owner_id = self.owner_id
        else:
            owner_id = validate_owner_id(owner_id)
        
        # public_updates_channel_id
        if public_updates_channel_id is ...:
            public_updates_channel_id = self.public_updates_channel_id
        else:
            public_updates_channel_id = validate_public_updates_channel_id(public_updates_channel_id)
        
        # safety_alerts_channel_id
        if safety_alerts_channel_id is ...:
            safety_alerts_channel_id = self.safety_alerts_channel_id
        else:
            safety_alerts_channel_id = validate_safety_alerts_channel_id(safety_alerts_channel_id)
        
        # rules_channel_id
        if rules_channel_id is ...:
            rules_channel_id = self.rules_channel_id
        else:
            rules_channel_id = validate_rules_channel_id(rules_channel_id)
        
        # system_channel_id
        if system_channel_id is ...:
            system_channel_id = self.system_channel_id
        else:
            system_channel_id = validate_system_channel_id(system_channel_id)
        
        # system_channel_flags
        if system_channel_flags is ...:
            system_channel_flags = self.system_channel_flags
        else:
            system_channel_flags = validate_system_channel_flags(system_channel_flags)
        
        # vanity_code
        if vanity_code is ...:
            vanity_code = self.vanity_code
        else:
            vanity_code = validate_vanity_code(vanity_code)
        
        # verification_level
        if verification_level is ...:
            verification_level = self.verification_level
        else:
            verification_level = validate_verification_level(verification_level)
        
        # widget_channel_id
        if widget_channel_id is ...:
            widget_channel_id = self.widget_channel_id
        else:
            widget_channel_id = validate_widget_channel_id(widget_channel_id)
        
        # widget_enabled
        if widget_enabled is ...:
            widget_enabled = self.widget_enabled
        else:
            widget_enabled = validate_widget_enabled(widget_enabled)
        
        # Construct
        new = object.__new__(type(self))
        new._cache_boosters = None
        new._cache_permission = None
        new._state = 0
        new.afk_channel_id = afk_channel_id
        new.afk_timeout = afk_timeout
        new.approximate_online_count = 0
        new.approximate_user_count = 0
        new.available = True
        new.banner = banner
        new.boost_count = 0
        new.boost_progress_bar_enabled = boost_progress_bar_enabled
        new.channels = {}
        new.clients = []
        new.default_message_notification_level = default_message_notification_level
        new.description = description
        new.discovery_splash = discovery_splash
        new.embedded_activities = None
        new.emojis = {}
        new.explicit_content_filter_level = explicit_content_filter_level
        new.features = features
        new.home_splash = home_splash
        new.hub_type = hub_type
        new.icon = icon
        new.id = 0
        new.incidents = None
        new.inventory_settings = None
        new.invite_splash = invite_splash
        new.large = False
        new.locale = locale
        new.max_presences = MAX_PRESENCES_DEFAULT
        new.max_stage_channel_video_users = MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
        new.max_users = MAX_USERS_DEFAULT
        new.max_voice_channel_video_users = MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
        new.mfa_level = mfa_level
        new.name = name
        new.nsfw_level = nsfw_level
        new.owner_id = owner_id
        new.boost_level = 0
        new.public_updates_channel_id = public_updates_channel_id
        new.safety_alerts_channel_id = safety_alerts_channel_id
        new.roles = {}
        new.rules_channel_id = rules_channel_id
        new.scheduled_events = None
        new.soundboard_sounds = None
        new.stages = None
        new.stickers = {}
        new.system_channel_id = system_channel_id
        new.system_channel_flags = system_channel_flags
        new.threads = None
        new.user_count = 0
        new.users = GUILD_USERS_TYPE()
        new.vanity_code = vanity_code
        new.verification_level = verification_level
        new.voice_states = None
        new.widget_channel_id = widget_channel_id
        new.widget_enabled = widget_enabled
        
        return new
    
    
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
        
        client.guilds.discard(self)
        
        try:
            clients.remove(client)
        except ValueError:
            return
        
        self._invalidate_cache_permission()
        
        guild_id = self.id
        
        if clients:
            # Clean up client guild profile.
            try:
                del client.guild_profiles[guild_id]
            except KeyError:
                pass
        
        else:
            # Clean up all guild profile.
            for user in self.users.values():
                try:
                    del user.guild_profiles[guild_id]
                except KeyError:
                    pass
    
    # ---- Extra Updaters ----
    
    def _update_voice_state(self, data, user):
        """
        Called by dispatch event. Updates the voice state of the represented user with the given `data`.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data received from Discord.
        user : ``ClientUserBase``
            The respective user.
        
        Yields
        -------
        action : `int`
            The respective action.
            
            Can be one of the following:
            
            +-----------------------------+-------+
            | Respective name             | Value |
            +=============================+=======+
            | VOICE_STATE_EVENT_NONE      | 0     |
            +-----------------------------+-------+
            | VOICE_STATE_EVENT_JOIN      | 1     |
            +-----------------------------+-------+
            | VOICE_STATE_EVENT_LEAVE     | 2     |
            +-----------------------------+-------+
            | VOICE_STATE_EVENT_UPDATE    | 3     |
            +-----------------------------+-------+
            | VOICE_STATE_EVENT_MOVE      | 4     |
            +-----------------------------+-------+
        
        voice_state : `None`, ``VoiceState``
            The user's respective voice state.
            
            Will be returned as `None` if action is `VOICE_STATE_EVENT_NONE`.
        
        old_attributes / old_channel_id : `None` or (`dict<str, object>` / `int`)
            If `action` is `VOICE_STATE_EVENT_UPDATE`, then `old_attributes` is returned as a `dict` containing the changed
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
            
            If `action` is `VOICE_STATE_EVENT_LEAVE`, `VOICE_STATE_EVENT_MOVE`, then the old channel's identifier is returned.
        """
        voice_state = self.get_voice_state(user.id)
        if voice_state is None:
            voice_state = VoiceState.from_data(data, self.id)
            if (voice_state is not None):
                voice_state._set_cache_user(user)
                yield VOICE_STATE_EVENT_JOIN, voice_state, None
        
        else:
            voice_state._set_cache_user(user)
            old_attributes = voice_state._difference_update_attributes(data)
            if old_attributes:
                yield VOICE_STATE_EVENT_UPDATE, voice_state, old_attributes
            
            old_channel_id, new_channel_id = voice_state._update_channel(data)
            if new_channel_id == 0:
                yield VOICE_STATE_EVENT_LEAVE, voice_state, old_channel_id
            elif old_channel_id != new_channel_id:
                yield VOICE_STATE_EVENT_MOVE, voice_state, old_channel_id
    
    
    def _update_voice_state_restricted(self, data, user):
        """
        Called by dispatch event. Updates the voice state of the represented user by `user_id` with the given `data`.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data received from Discord.
        user : ``ClientUserBase``
            The respective user.
        
        Returns
        -------
        voice_state : ``VoiceState``
            The created or updated voice state.
        """
        voice_state = self.get_voice_state(user.id)
        if voice_state is None:
            voice_state = VoiceState.from_data(data, self.id)
            if (voice_state is not None):
                voice_state._set_cache_user(user)
        else:
            voice_state._set_cache_user(user)
            voice_state._update_channel(data)
            voice_state._update_attributes(data)
        
        return voice_state
    
    
    def _difference_update_emojis(self, data):
        """
        Updates the emojis o the guild and returns all the changes broke down for each changes emoji.
        
        Parameters
        ----------
        data : `list` of (`dict<str, object>`)
            Received emoji datas.
        
        Returns
        -------
        changes : `list` of `tuple` (`int`, ``Emoji``, (`None`, `dict<str, object>`)))
            The changes broken down for each changed emoji. Each element of the list is a tuple of 3 elements:
            
            +-------+-------------------+-----------------------------------------------+
            | Index | Respective name   | Type                                          |
            +=======+===================+===============================================+
            | 0     | action            | `int`                                         |
            +-------+-------------------+-----------------------------------------------+
            | 1     | emoji             | ``Emoji``                                     |
            +-------+-------------------+-----------------------------------------------+
            | 2     | old_attributes    | `None`, `dict<str, object>`     |
            +-------+-------------------+-----------------------------------------------+
            
            Possible actions:
            
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | EMOJI_EVENT_NONE      | `0`   |
            +-----------------------+-------+
            | EMOJI_EVENT_CREATE    | `1`   |
            +-----------------------+-------+
            | EMOJI_EVENT_DELETE    | `2`   |
            +-----------------------+-------+
            | EMOJI_EVENT_UPDATE    | `3`   |
            +-----------------------+-------+
            
            If action is `EMOJI_EVENT_UPDATE`, then `old_attributes` is passed as a dictionary containing the changed
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
            | roles_ids         | `None | tuple<int>`           |
            +-------------------+-------------------------------+
        """
        emojis = self.emojis
        changes = []
        old_ids = set(emojis)
        
        for emoji_data in data:
            emoji_id = parse_emoji_id(emoji_data)
            try:
                emoji = emojis[emoji_id]
            except KeyError:
                emoji = Emoji.from_data(emoji_data, self.id)
                emojis[emoji.id] = emoji
                changes.append((EMOJI_EVENT_CREATE, emoji, None),)
            else:
                old_attributes = emoji._difference_update_attributes(emoji_data)
                if old_attributes:
                    changes.append((EMOJI_EVENT_UPDATE, emoji, old_attributes),)
                old_ids.remove(emoji_id)
        
        for emoji_id in old_ids:
            try:
                emoji = emojis.pop(emoji_id)
            except KeyError:
                pass
            else:
                changes.append((EMOJI_EVENT_DELETE, emoji, None),)
        
        return changes
    
    
    def _difference_update_soundboard_sounds(self, data):
        """
        Updates the soundboard_sounds of the guild and returns the changes broke down for each changed soundboard sound.
        
        Parameters
        ----------
        data : `list` of (`dict<str, object>`)
            Received soundboard sound datas.
        
        Returns
        -------
        changes : `list` of `tuple` (`int`, ``SoundboardSound``, (`None`, `dict<str, object>`)))
            The changes broken down for each changed soundboard sound.
            Each element of the list is a tuple of 3 elements:
            
            +-------+-------------------+-----------------------------------------------+
            | Index | Respective name   | Type                                          |
            +=======+===================+===============================================+
            | 0     | action            | `int`                                         |
            +-------+-------------------+-----------------------------------------------+
            | 1     | soundboard_sound  | ``SoundboardSound``                           |
            +-------+-------------------+-----------------------------------------------+
            | 2     | old_attributes    | `None`, `dict<str, object>`     |
            +-------+-------------------+-----------------------------------------------+
            
            Possible actions:
            
            +-------------------------------+-------+
            | Respective name               | Value |
            +===============================+=======+
            | SOUNDBOARD_SOUND_EVENT_NONE   | `0`   |
            +-------------------------------+-------+
            | SOUNDBOARD_SOUND_EVENT_CREATE | `1`   |
            +-------------------------------+-------+
            | SOUNDBOARD_SOUND_EVENT_DELETE | `2`   |
            +-------------------------------+-------+
            | SOUNDBOARD_SOUND_EVENT_UPDATE | `3`   |
            +-------------------------------+-------+
            
            If action is `SOUNDBOARD_SOUND_EVENT_UPDATE`, then `old_attributes` is passed as a dictionary containing
            the changed attributes in an `attribute-name` - `old-value` relation. Every item in `old_attributes` is
            optional.
            
            +-----------+-------------------+
            | Keys      | Values            |
            +===========+===================+
            | available | `bool`            |
            +-----------+-------------------+
            | emoji     | `None`, ``Emoji`` |
            +-----------+-------------------+
            | name      | `str`             |
            +-----------+-------------------+
            | volume    | `float`           |
            +-----------+-------------------+
        """
        soundboard_sounds = self.soundboard_sounds
        changes = []
        
        if soundboard_sounds is None:
            old_ids = None
        else:
            old_ids = set(soundboard_sounds)
        
        if data:
            if soundboard_sounds is None:
                soundboard_sounds = {}
                self.soundboard_sounds = soundboard_sounds
            
            for soundboard_sound_data in data:
                soundboard_sound_id = parse_soundboard_sound_id(soundboard_sound_data)
                
                try:
                    soundboard_sound = soundboard_sounds[soundboard_sound_id]
                except KeyError:
                    soundboard_sound = SoundboardSound.from_data(soundboard_sound_data)
                    soundboard_sounds[soundboard_sound.id] = soundboard_sound
                    changes.append((SOUNDBOARD_SOUND_EVENT_CREATE, soundboard_sound, None),)
                
                else:
                    old_attributes = soundboard_sound._difference_update_attributes(soundboard_sound_data)
                    if old_attributes:
                        changes.append((SOUNDBOARD_SOUND_EVENT_UPDATE, soundboard_sound, old_attributes),)
                    
                    if (old_ids is not None):
                        old_ids.remove(soundboard_sound_id)
        
        else:
            self.soundboard_sounds = None
        
        if (old_ids is not None):
            for soundboard_sound_id in old_ids:
                try:
                    soundboard_sound = soundboard_sounds.pop(soundboard_sound_id)
                except KeyError:
                    pass
                else:
                    changes.append((SOUNDBOARD_SOUND_EVENT_DELETE, soundboard_sound, None),)
        
        self.soundboard_sounds_cached = True
        
        return changes
    
    
    def _difference_update_stickers(self, data):
        """
        Updates the stickers of the guild and returns the changes broke down for each changed sticker.
        
        Parameters
        ----------
        data : `list` of (`dict<str, object>`)
            Received sticker datas.
        
        Returns
        -------
        changes : `list` of `tuple` (`int`, ``Sticker``, (`None`, `dict<str, object>`)))
            The changes broken down for each changed sticker. Each element of the list is a tuple of 3 elements:
            
            +-------+-------------------+-----------------------------------------------+
            | Index | Respective name   | Type                                          |
            +=======+===================+===============================================+
            | 0     | action            | `int`                                         |
            +-------+-------------------+-----------------------------------------------+
            | 1     | sticker           | ``Sticker``                                   |
            +-------+-------------------+-----------------------------------------------+
            | 2     | old_attributes    | `None`, `dict<str, object>`     |
            +-------+-------------------+-----------------------------------------------+
            
            Possible actions:
            
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | STICKER_EVENT_NONE    | `0`   |
            +-----------------------+-------+
            | STICKER_EVENT_CREATE  | `1`   |
            +-----------------------+-------+
            | STICKER_EVENT_DELETE  | `2`   |
            +-----------------------+-------+
            | STICKER_EVENT_UPDATE  | `3`   |
            +-----------------------+-------+
            
            If action is `STICKER_EVENT_UPDATE`, then `old_attributes` is passed as a dictionary containing the changed
            attributes in an `attribute-name` - `old-value` relation. Every item in `old_attributes` is optional.
            
            +-----------------------+-----------------------------------+
            | Keys                  | Values                            |
            +=======================+===================================+
            | available             | `bool`                            |
            +-----------------------+-----------------------------------+
            | description           | `None`, `str`                     |
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
            sticker_id = parse_sticker_id(sticker_data)
            try:
                sticker = stickers[sticker_id]
            except KeyError:
                sticker = Sticker.from_data(sticker_data)
                stickers[sticker.id] = sticker
                changes.append((STICKER_EVENT_CREATE, sticker, None),)
            else:
                old_attributes = sticker._difference_update_attributes(sticker_data)
                if old_attributes:
                    changes.append((STICKER_EVENT_UPDATE, sticker, old_attributes),)
                old_ids.remove(sticker_id)
        
        for sticker_id in old_ids:
            try:
                sticker = stickers.pop(sticker_id)
            except KeyError:
                pass
            else:
                changes.append((STICKER_EVENT_DELETE, sticker, None),)
        
        return changes
    
    
    def _update_generic(self, data):
        """
        Syncs the guild with the requested guild data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received guild data.
        """
        self.emojis = parse_emojis(data, self.emojis, self.id)
        self.roles = parse_roles(data, self.roles, self.id)
        self.stickers = parse_stickers(data, self.stickers)
        
        self._update_attributes(data)
        
        # We do not receive large, but we still want to update it
        self.large = self.large or (self.approximate_user_count >= LARGE_GUILD_LIMIT)
        
        # No other data received.
    
    
    def _update_channels(self, data):
        """
        Syncs the guild's channels with the given guild channel datas.
        
        Parameters
        ----------
        data `list` of `dict<str, object>`
            Received guild channel datas.
        """
        channels = self.channels
        if channels:
            old_channels = [*channels.values()]
            channels.clear()
        
        guild_id = self.id
        
        for channel_data in data:
            channel = Channel.from_data(channel_data, None, guild_id, strong_cache = False)
            channels[channel.id] = channel
    
    
    def _update_emojis(self, emoji_datas):
        """
        Syncs the emojis of the guild.
        
        Parameters
        ----------
        emoji_datas : `list` of (`dict<str, object>`)
            Received emoji datas.
        """
        emojis = self.emojis
        if emojis:
            emoji_cache = [*emojis.values()]
            emojis.clear()
        
        guild_id = self.id
        
        for emoji_data in emoji_datas:
            emoji = Emoji.from_data(emoji_data, guild_id)
            emojis[emoji.id] = emoji
    
    
    def _update_roles(self, data):
        """
        Syncs the guild's roles with the given guild role datas.
        
        Parameters
        ----------
        data `list` of `dict<str, object>`
            Received guild role datas.
        """
        roles = self.roles
        if roles:
            old_roles = [*roles.values()]
            roles.clear()
        
        guild_id = self.id
        
        for role_data in data:
            role = Role.from_data(role_data, guild_id, strong_cache = False)
            roles[role.id] = role
    
    
    def _update_soundboard_sounds(self, data):
        """
        Syncs the guild's soundboard_sounds with the given guild soundboard_sound datas.
        
        Parameters
        ----------
        data `list` of `dict<str, object>`
            Received guild soundboard sound datas.
        """
        if data:
            soundboard_sounds = self.soundboard_sounds
            if (soundboard_sounds is None):
                soundboard_sounds = {}
                self.soundboard_sounds = soundboard_sounds
            else:
                old_soundboard_sounds = [*soundboard_sounds.values()]
                soundboard_sounds.clear()
            
            for soundboard_sound_data in data:
                soundboard_sound = SoundboardSound.from_data(soundboard_sound_data, strong_cache = False)
                soundboard_sounds[soundboard_sound.id] = soundboard_sound
        
        else:
            self.soundboard_sounds = None
        
        self.soundboard_sounds_cached = True
    
    
    def _update_stickers(self, sticker_datas):
        """
        Syncs the stickers of the guild.
        
        Parameters
        ----------
        sticker_datas : `list` of (`dict<str, object>`)
            Received sticker datas.
        """
        stickers = self.stickers
        if stickers:
            sticker_cache = [*stickers.values()]
            stickers.clear()
        
        for sticker_data in sticker_datas:
            sticker = Sticker.from_data(sticker_data)
            stickers[sticker.id] = sticker
    
    
    # ---- properties ----
    
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
    
    
    @property
    def boost_perks(self):
        """
        Returns the boost perks of the guild.
        
        Returns
        -------
        boost_perks : ``GuildBoostPerks``
        """
        return BOOST_LEVELS.get(self.boost_level, BOOST_LEVEL_MAX)
    
    
    @property
    def premium_tier(self):
        """
        Deprecated and will be removed n 2025 November. Please use `.boost_level` instead.
        """
        warn(
            (
                f'`{type(self).__name__}.premium_tier` is deprecated and will be removed in 2025 November. '
                f'Please use `.boost_level` instead.'
            ),
            FutureWarning
        )
        return self.boost_level
    
    
    @property
    def premium_perks(self):
        """
        Deprecated and will be removed in 2025 November. Please use `boost_perks` instead.
        """
        warn(
            (
                f'`{type(self).__name__}.premium_perks` is deprecated and will be removed in 2025 November. '
                f'Please use `.boost_perks` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return BOOST_LEVELS.get(self.boost_level, BOOST_LEVEL_MAX)
    
    
    @property
    def emoji_limit(self):
        """
        The maximal amount of emojis, what the guild can have.
        
        Returns
        -------
        limit : `int`
        """
        limit = self.boost_perks.emoji_limit
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
        limit = self.boost_perks.bitrate_limit
        if limit < 128000 and self.has_feature(GuildFeature.vip_voice_regions):
            limit = 128000
        
        return limit
    
    
    @property
    def attachment_size_limit(self):
        """
        The maximal size in bytes of each attachment that can be uploaded to the guild's channels.
        
        Returns
        -------
        limit : `int`
        """
        return self.boost_perks.attachment_size_limit
    
    
    @property
    def upload_limit(self):
        """
        Deprecated and will be removed in 2025 November. Please use `.attachment_size_limit` instead.
        """
        warn(
            (
                f'`{type(self).__name__}.upload_limit` is deprecated and will be removed in 2025 November. '
                f'Please use `.attachment_size_limit` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.boost_perks.attachment_size_limit
    
    
    @property
    def sticker_limit(self):
        """
        The maximal amount of stickers, what the guild can have.
        
        Returns
        -------
        limit : `int`
        """
        limit = self.boost_perks.sticker_limit
        if limit < 30 and self.has_feature(GuildFeature.more_sticker):
            limit = 30
        
        return limit
    
    
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
        public_updates_channel : ``None | Channel``
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
        afk_channel : ``None | Channel``
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
        rules_channel : ``None | Channel``
        """
        rules_channel_id = self.rules_channel_id
        if rules_channel_id:
            return self.channels.get(rules_channel_id, None)
    
    
    @property
    def safety_alerts_channel(self):
        """
        Returns the channel where safety alerts are sent by Discord.
        
        Returns
        -------
        safety_alerts_channel : ``None | Channel``
        """
        safety_alerts_channel_id = self.safety_alerts_channel_id
        if safety_alerts_channel_id:
            return self.channels.get(safety_alerts_channel_id, None)
    
    
    @property
    def system_channel(self):
        """
        Returns the channel where the system messages are sent.
        
        Returns
        -------
        public_updates_channel : ``None | Channel``
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
        public_updates_channel : ``None | Channel``
        """
        widget_channel_id = self.widget_channel_id
        if widget_channel_id:
            return self.channels.get(widget_channel_id, None)
    
    
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
    def channel_list(self):
        """
        Returns the channels of the guild in a list in their display order. Note, that channels inside of categories are
        excluded.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        return sorted(channel for channel in self.channels.values() if channel.parent_id == 0)
    
    
    @property
    def channel_list_flattened(self):
        """
        Returns the channels of the guild in a list in their display order. Note, that channels inside of categories are
        included as well.
        
        channels : `list` of ``Channel``
        """
        channels = []
        for channel in sorted(channel for channel in self.channels.values() if channel.parent_id == 0):
            channels.append(channel)
            if channel.is_guild_category():
                channels.extend(channel.channels)
        
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
    
    
    # ---- cache ----
    
    @property
    def soundboard_sounds_cached(self):
        """
        Returns whether the guild has its soundboard sounds cached.
        """
        return True if self._state & GUILD_STATE_MASK_SOUNDBOARD_SOUNDS_CACHED else False
    
    
    @soundboard_sounds_cached.setter
    def soundboard_sounds_cached(self, value):
        state = self._state
        if value:
            state |= GUILD_STATE_MASK_SOUNDBOARD_SOUNDS_CACHED
        else:
            state &= ~GUILD_STATE_MASK_SOUNDBOARD_SOUNDS_CACHED
        self._state = state
    

    def _invalidate_cache_permission(self):
        """
        Invalidates the cached permissions of the guild.
        """
        self._cache_permission = None
        for channel in self.channels.values():
            channel.metadata._invalidate_cache_permission()
    
    
    def _clear_cache(self):
        """
        Clears the guild's cache fields.
        """
        self._state &= ~ GUILD_STATE_MASK_CACHE_ALL
        self._cache_boosters = None
    
    
    def _get_boosters(self):
        """
        Iterates over the users of the guild and selects the ones boosting. The output is sorted.
        
        Returns
        -------
        boosters : `None`, `tuple` of ``ClientUserBase``
        """
        if not self.boost_count:
            return None
        
        boosters = []
        guild_id = self.id
        
        for user in self.users.values():
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            boosts_since = guild_profile.boosts_since
            if boosts_since is None:
                continue
            
            boosters.append((user, boosts_since),)
        
        boosters.sort(key = _user_date_sort_key)
        return tuple(element[0] for element in boosters)
    
    
    @property
    def boosters(self):
        """
        The boosters of the guild sorted by their subscription date.
        
        These users are queried from the guild's `.users` dictionary, so make sure that is populated before accessing
        the property.
        
        Returns
        -------
        boosters : `None`, `tuple` of ``ClientUserBase``
        """
        state = self._state
        if state & GUILD_STATE_MASK_CACHE_BOOSTERS:
            boosters = self._cache_boosters
        else:
            boosters = self._get_boosters()
            self._cache_boosters = boosters
            self._state = state | GUILD_STATE_MASK_CACHE_BOOSTERS
        
        return boosters
    
    # ---- getters -----
    
    def get_channel(self, name, default = None, type_checker = None):
        """
        Searches a channel of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no channel was found.
        type_checker : `None`, `FunctionType` = `None`, Optional
            Function specifically to check the channel's type.
        
        Returns
        -------
        channel : ``Channel``, `default`
        """
        if name.startswith('#'):
            name = name[1:]
        
        name_length = len(name)
        if (name_length < CHANNEL_NAME_LENGTH_MIN) or (name_length > CHANNEL_NAME_LENGTH_MAX):
            return default
        
        for channel in self.channels.values():
            if (type_checker is not None) and (not type_checker(channel)):
                continue
            
            if channel.display_name == name:
                return channel
        
        for channel in self.channels.values():
            if (type_checker is not None) and (not type_checker(channel)):
                continue
            
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
        default : `object` = `None`, Optional
            The value what is returned when no channel was found.
        type_checker : `None`, `FunctionType` = `None`, Optional
            Function specifically to check the channel's type.
        
        Returns
        -------
        channel : ``Channel``, `default`
        """
        if name.startswith('#'):
            name = name[1:]
        
        name_length = len(name)
        if name_length > CHANNEL_NAME_LENGTH_MAX:
            return default
        
        channel_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        accurate_channel = default
        accurate_match_key = None
        
        for channel in self.channels.values():
            if (type_checker is not None) and (not type_checker(channel)):
                continue
            
            channel_name = channel.name
            parsed = channel_name_pattern.search(channel_name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            match_rate = (match_length, match_start)
            if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                continue
            
            accurate_channel = channel
            accurate_match_key = match_rate
            continue
        
        return accurate_channel
    
    
    def get_channels_like(self, name, type_checker = None):
        """
        Searches the channels, what's name match the given value.
        
        The returned value is ordered by match rate.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        type_checker : `None`, `FunctionType` = `None`, Optional
            Function specifically to check the channel's type.
        
        Returns
        -------
        channels : `list` of ``Channel``
        """
        if name.startswith('#'):
            name = name[1:]
        
        name_length = len(name)
        if name_length > CHANNEL_NAME_LENGTH_MAX:
            return []
        
        channel_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        matches = []
        
        for channel in self.channels.values():
            if (type_checker is not None) and (not type_checker(channel)):
                continue
            
            channel_name = channel.name
            parsed = channel_name_pattern.search(channel_name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            matches.append((channel, (match_length, match_start)))
        
        if not matches:
            return matches
        
        matches.sort(key = _channel_match_sort_key)
        return [item[0] for item in matches]
    
    
    def get_emoji(self, name, default = None):
        """
        Searches an emoji of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        emoji : ``Emoji``, `default`
        """
        parsed = EMOJI_NAME_RP.fullmatch(name)
        if (parsed is None):
            return default
        
        name = parsed.group(1)
        
        name_length = len(name)
        if (name_length < EMOJI_NAME_LENGTH_MIN) or (name_length > EMOJI_NAME_LENGTH_MAX):
            return default
        
        for emoji in self.emojis.values():
            if emoji.name == name:
                return emoji
    
        return default
    
    
    def get_emoji_like(self, name, default = None):
        """
        Searches an emoji of the guild that matches the given `name` the most.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        emoji : ``Emoji``, `default`
        """
        name = _strip_emoji_name(name)
        
        name_length = len(name)
        if name_length > EMOJI_NAME_LENGTH_MAX:
            return default
        
        emoji_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        accurate_emoji = default
        accurate_match_key = None
        
        for emoji in self.emojis.values():
            emoji_name = emoji.name
            parsed = emoji_name_pattern.search(emoji_name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            match_rate = (match_length, match_start)
            if (accurate_match_key is not None) and (accurate_match_key < match_rate):
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
        name_length = len(name)
        if name_length > EMOJI_NAME_LENGTH_MAX:
            return []
        
        emoji_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        matches = []
        
        for emoji in self.emojis.values():
            emoji_name = emoji.name
            parsed = emoji_name_pattern.search(emoji_name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            matches.append((emoji, (match_length, match_start)))
        
        if not matches:
            return []
        
        matches.sort(key = _emoji_match_sort_key)
        return [item[0] for item in matches]
    

    def get_role(self, name, default = None):
        """
        Searches a role of the guild, what's name equals the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no role was found. Defaults to `None`.
        
        Returns
        -------
        role : ``Role``, `default`
        """
        name_length = len(name)
        if (name_length < ROLE_NAME_LENGTH_MIN) or (name_length > ROLE_NAME_LENGTH_MAX):
            return default
        
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
        default : `object` = `None`, Optional
            The value what is returned when no role was found. Defaults to `None`.
        
        Returns
        -------
        role : ``Role``, `default`
        """
        name_length = len(name)
        if (name_length > ROLE_NAME_LENGTH_MAX):
            return default
        
        role_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        accurate_role = default
        accurate_match_key = None
        
        for role in self.roles.values():
            parsed = role_name_pattern.search(role.name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            match_rate = (match_length, match_start)
            if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                continue
            
            accurate_role = role
            accurate_match_key = match_rate
            continue
        
        return accurate_role
    
    
    def get_roles_like(self, name):
        """
        Searches the roles, what's name match the given value.
        
        The returned value is ordered by match rate.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        roles : `list` of ``Role``
        """
        name_length = len(name)
        if (name_length > ROLE_NAME_LENGTH_MAX):
            return []
        
        role_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        matches = []
        
        for role in self.roles.values():
            parsed = role_name_pattern.search(role.name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            matches.append((role, (match_length, match_start)))
        
        if not matches:
            return []
        
        matches.sort(key = _role_match_sort_key)
        return [item[0] for item in matches]
    
    
    def get_soundboard_sound(self, name, default = None):
        """
        Searches an soundboard sound of the guild that has it name set to same value as the given `name`.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no soundboard sound was found. Defaults to `None`.
        
        Returns
        -------
        soundboard_sound : ``SoundboardSound``, `default`
        """
        name_length = len(name)
        if (name_length < SOUNDBOARDS_SOUND_NAME_LENGTH_MIN) or (name_length > SOUNDBOARDS_SOUND_NAME_LENGTH_MAX):
            return default
        
        for soundboard_sound in self.iter_soundboard_sounds():
            if soundboard_sound.name == name:
                return soundboard_sound
        
        return default
    
    
    def get_soundboard_sound_like(self, name, default = None):
        """
        Searches the soundboard sound of the guild that have its name matching the given `name` value the most.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no soundboard sound was found. Defaults to `None`.
        
        Returns
        -------
        soundboard_sound : ``SoundboardSound``, `default`
        """
        name_length = len(name)
        if name_length > SOUNDBOARDS_SOUND_NAME_LENGTH_MAX:
            return default
        
        soundboard_sound_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        accurate_soundboard_sound = default
        accurate_match_key = None
        
        for soundboard_sound in self.iter_soundboard_sounds():
            parsed = soundboard_sound_name_pattern.search(soundboard_sound.name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            match_rate = (match_length, match_start)
            if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                continue
            
            accurate_soundboard_sound = soundboard_sound
            accurate_match_key = match_rate
            continue
        
        return accurate_soundboard_sound
    
    
    def get_soundboard_sounds_like(self, name):
        """
        Searches the soundboard sounds that have their name matching the given value.
        
        The returned value is ordered by match rate.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        soundboard_sounds : `list` of ``SoundboardSound``
        """
        name_length = len(name)
        if name_length > SOUNDBOARDS_SOUND_NAME_LENGTH_MAX:
            return []
        
        soundboard_sound_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        matches = []
        
        for soundboard_sound in self.iter_soundboard_sounds():
            parsed = soundboard_sound_name_pattern.search(soundboard_sound.name)
            if parsed is None:
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            matches.append((soundboard_sound, (match_length, match_start)))
        
        if not matches:
            return []
        
        matches.sort(key = _soundboard_sound_match_sort_key)
        return [item[0] for item in matches]
    
    
    def get_sticker(self, name, default = None):
        """
        Searches a sticker of the guild, what's name equals to the given name.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        sticker : ``Sticker``, `default`
        """
        name_length = len(name)
        if (name_length < STICKER_NAME_LENGTH_MIN) or (name_length > STICKER_NAME_LENGTH_MAX):
            return default
        
        for sticker in self.stickers.values():
            if sticker.name == name:
                return sticker
        
        return default
    
    
    def get_sticker_like(self, name, default = None):
        """
        Searches a sticker of the guild that's name or tag matches the given `name` the most.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `object` = `None`, Optional
            The value what is returned when no emoji was found. Defaults to `None`.
        
        Returns
        -------
        sticker : ``Sticker``, `default`
        """
        name_length = len(name)
        if name_length > STICKER_NAME_LENGTH_MAX:
            return default
        
        sticker_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        accurate_sticker = default
        accurate_match_key = None
        
        for sticker in self.stickers.values():
            parsed = sticker_name_pattern.search(sticker.name)
            if (parsed is None):
                continue
            
            match_start = parsed.start()
            match_length = parsed.end() - match_start
            
            match_rate = (STICKER_MATCH_WEIGHT_NAME, match_length, match_start)
            if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                continue
            
            accurate_sticker = sticker
            accurate_match_key = match_rate
            continue
        
        if (accurate_match_key is not None):
            return accurate_sticker
        
        for sticker in self.stickers.values():
            sticker_tags = sticker.tags
            if (sticker_tags is not None):
                for sticker_tag in sticker_tags:
                    
                    parsed = sticker_name_pattern.search(sticker_tag)
                    if (parsed is None):
                        continue
                    
                    match_start = parsed.start()
                    match_length = parsed.end() - match_start
                    
                    match_rate = (STICKER_MATCH_WEIGHT_TAG, match_length, match_start)
                    if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                        continue
                    
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
        name_length = len(name)
        if name_length > STICKER_NAME_LENGTH_MAX:
            return []
        
        sticker_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        matches = []
        
        for sticker in self.stickers.values():
            # name
            
            parsed = sticker_name_pattern.search(sticker.name)
            if (parsed is not None):
                
                match_start = parsed.start()
                match_length = parsed.end() - match_start
                
                match_rate = (STICKER_MATCH_WEIGHT_NAME, match_length, match_start)
                
                matches.append((sticker, match_rate))
                continue
            
            # tags
            
            sticker_tags = sticker.tags
            if (sticker_tags is not None):
                accurate_match_key = None
                
                for sticker_tag in sticker_tags:
                    
                    parsed = sticker_name_pattern.search(sticker_tag)
                    if (parsed is not None):
                        
                        match_start = parsed.start()
                        match_length = parsed.end() - match_start
                        
                        match_rate = (STICKER_MATCH_WEIGHT_TAG, match_length, match_start)
                        
                        if (accurate_match_key is not None) and (accurate_match_key < match_rate):
                            continue
                        
                        accurate_match_key = match_rate
                        continue
                
                if (accurate_match_key is not None):
                    matches.append((sticker, accurate_match_key))
        
        if not matches:
            return []
        
        return [item[0] for item in sorted(matches, key = _sticker_match_sort_key)]
    
    
    def get_user(self, name, default = None):
        """
        Tries to find the a user with the given name at the guild. Returns the first matched one.
        
        The search order is the following:
        - name with discriminator
        - name
        - global name
        - nick
        
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
        
        users = self.users
        
        # name with discriminator
        
        name_with_discriminator = _parse_name_with_discriminator(name)
        if (name_with_discriminator is not None):
            for user in users.values():
                if _is_user_matching_name_with_discriminator(user, name_with_discriminator):
                    return user
        
        if name_length > USER_ALL_NAME_LENGTH_MAX:
            return default
        
        # name
        for user in users.values():
            if user.name == name:
                return user
        
        # global_name
        for user in users.values():
            user_display_name = user.display_name
            if (user_display_name is not None) and (user_display_name == name):
                return user
        
        # nick
        guild_id = self.id
        for user in users.values():
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
        Searches a user, who's name or nick starts with the given string and returns the first find. Also matches full
        name.
        
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
        
        users = self.users
        
        # name with discriminator
        
        name_with_discriminator = _parse_name_with_discriminator(name)
        if (name_with_discriminator is not None):
            for user in users.values():
                if _is_user_matching_name_with_discriminator(user, name_with_discriminator):
                    return user
        
        if name_length > USER_ALL_NAME_LENGTH_MAX:
            return default
        
        user_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        
        
        accurate_user = default
        accurate_match_key = None
        
        # name
        
        for user in self.users.values():
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

        for user in self.users.values():
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
        for user in self.users.values():
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
        Searches the users, who's name or nick start with the given string.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : ``list<ClientUserBase>``
        """
        name_length = len(name)
        if name_length > USER_ALL_NAME_LENGTH_MAX_WITH_DISCRIMINATOR:
            return []
        
        users = self.users
        
        # name with discriminator
        
        name_with_discriminator = _parse_name_with_discriminator(name)
        if (name_with_discriminator is not None):
            for user in users.values():
                if _is_user_matching_name_with_discriminator(user, name_with_discriminator):
                    return [user]
        
        if name_length > USER_ALL_NAME_LENGTH_MAX:
            return []
        
        user_name_pattern = re_compile('.*?'.join(re_escape(char) for char in name), re_ignore_case)
        matches = []
        guild_id = self.id
        
        for user in users.values():
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
    
    
    def get_users_like_ordered(self, name):
        """
        Searches the users, who's name or nick start with the given string. At the orders them at the same ways, as
        Discord orders them when requesting guild users chunk.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : ``list<ClientUserBase>``
        """
        name_length = len(name)
        
        if (name_length > USER_ALL_NAME_LENGTH_MAX):
            return []
        
        matches = []
        now_date_time = None
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        guild_id = self.id
        for user in self.users.values():
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            # Use goto
            while True:
                if (pattern.search(user.name) is not None):
                    matched = True
                    break
                
                user_display_name = user.display_name
                if (user_display_name is not None) and (pattern.search(user_display_name) is not None):
                    matched = True
                    break
                
                user_nick = guild_profile.nick
                if (user_nick is not None) and (pattern.search(user_nick) is not None):
                    matched = True
                    break
                
                matched = False
                break
            
            if not matched:
                continue
            
            joined_at = guild_profile.joined_at
            
            if joined_at is None:
                # Instead of defaulting to `user.created_at` use the current date
                if now_date_time is None:
                    now_date_time = DateTime.now(TimeZone.utc)
                
                joined_at = now_date_time
            
            
            matches.append((user, joined_at))
        
        if not matches:
            return []
        
        matches.sort(key = _user_date_sort_key)
        return [item[0] for item in matches]
    
    
    def get_voice_state(self, user_id):
        """
        Returns the guild's voice state for the given user identifier.
        
        Parameters
        ----------
        user_id : `int`
            User identifier.
        
        Returns
        -------
        voice_state : `None`, ``VoiceState``
        """
        voice_states = self.voice_states
        if voice_states is not None:
            return voice_states.get(user_id, None)
    
    
    # ---- iterators ----
    
    def iter_channels(self, type_checker = None):
        """
        Iterates over the channels of the guild.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        type_checker : `None`, `FunctionType` = `None`, Optional
            Function specifically to check the channel's type.
        
        Yields
        -------
        channel : ``Channel``
        """
        if type_checker is None:
            yield from self.channels.values()
            return
        
        for channel in self.channels.values():
            if type_checker(channel):
                yield channel
    
    
    def iter_embedded_activities(self):
        """
        Iterates over the embedded activities of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        embedded_activity : ``EmbeddedActivity``
        """
        embedded_activities = self.embedded_activities
        if (embedded_activities is not None):
            yield from embedded_activities
    
    
    def iter_emojis(self):
        """
        Iterates over the emojis of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        emoji : ``Emoji``
        """
        yield from self.emojis.values()
    
    
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
    
    
    def iter_roles(self):
        """
        Iterates over the roles of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        role : ``Role``
        """
        yield from self.roles.values()
    
    
    def iter_scheduled_events(self):
        """
        Iterates overt he scheduled events of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        scheduled_event : ``ScheduledEvent``
        """
        scheduled_events = self.scheduled_events
        if (scheduled_events is not None):
            yield from scheduled_events.values()
    
    
    def iter_soundboard_sounds(self):
        """
        Iterates over the guild's soundboard sounds.
        
        This method is an iterable generator.
        
        Yields
        ------
        soundboard_sound : ``SoundboardSound``
        """
        soundboard_sounds = self.soundboard_sounds
        if (soundboard_sounds is not None):
            yield from soundboard_sounds.values()
    
    
    def iter_stages(self):
        """
        Iterates over the stages of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        stage : ``Stage``
        """
        stages = self.stages
        if (stages is not None):
            yield from stages.values()
    
    
    def iter_stickers(self):
        """
        Iterates over the stickers of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        sticker : ``Sticker``
        """
        yield from self.stickers.values()
    
    
    def iter_threads(self):
        """
        Iterates over the threads of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        thread : ``Channel``
        """
        threads = self.threads
        if (threads is not None):
            yield from threads.values()
    
    
    def iter_users(self):
        """
        Iterates over the users of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        yield from self.users.values()
    
    
    def iter_voice_states(self):
        """
        Iterates over the voice state of the guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        voice_state : ``VoiceState``
        """
        voice_states = self.voice_states
        if (voice_states is not None):
            yield from self.voice_states.values()
    
    # ---- has ----

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
    
    
    # ---- permissions ----
    
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
        roles = self.roles
        
        if isinstance(user, WebhookBase):
            if user.channel_id not in self.channels:
                return PERMISSION_NONE
            
            role_everyone = roles.get(guild_id, None)
            if role_everyone is None:
                permissions = PERMISSION_NONE
            else:
                permissions = role_everyone.permissions
                if permissions & PERMISSION_MASK_ADMINISTRATOR:
                    permissions = PERMISSION_ALL
            
            return permissions
        
        if user.id == self.owner_id:
            return PERMISSION_ALL
        
        role_everyone = roles.get(guild_id, None)
        if role_everyone is None:
            permissions = 0
        else:
            permissions = role_everyone.permissions
        
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            return PERMISSION_NONE
        
        role_ids = guild_profile.role_ids
        if (role_ids is not None):
            for role_id in role_ids:
                try:
                    role = roles[role_id]
                except KeyError:
                    continue
                
                permissions |= role.permissions
                continue
        
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
        
        cache_permission = self._cache_permission
        if cache_permission is None:
            self._cache_permission = cache_permission = {}
        else:
            try:
                return cache_permission[user.id]
            except KeyError:
                pass
        
        permissions = self.permissions_for(user)
        cache_permission[user.id] = permissions
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
        self_roles = self.roles
        
        default_role = self_roles.get(self.id, None)
        if default_role is None:
            permissions = 0
        else:
            permissions = default_role.permissions
        
        for role in roles:
            if role.id in self_roles:
                permissions |= role.permissions
        
        if permissions & PERMISSION_MASK_ADMINISTRATOR:
            return PERMISSION_ALL
        
        return Permission(permissions)
    
    
    @property
    def banner_url(self):
        """
        Returns the guild's banner's url. If the guild has no banner, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_banner_url(self.id, self.banner_type, self.banner_hash)
    
    
    def banner_url_as(self, ext = None, size = None):
        """
        Returns the guild's banner's url. If the guild has no banner, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated banner, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_banner_url_as(self.id, self.banner_type, self.banner_hash, ext, size)
    
    
    @property
    def discovery_splash_url(self):
        """
        Returns the guild's discovery splash's url. If the guild has no discovery_splash, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_discovery_splash_url(self.id, self.discovery_splash_type, self.discovery_splash_hash)
    
    
    def discovery_splash_url_as(self, ext = None, size = None):
        """
        Returns the guild's discovery splash's url. If the guild has no discovery splash, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated discovery splash, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_discovery_splash_url_as(
            self.id, self.discovery_splash_type, self.discovery_splash_hash, ext, size
        )
    
    
    @property
    def home_splash_url(self):
        """
        Returns the guild's home splash's url. If the guild has no home_splash, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_home_splash_url(self.id, self.home_splash_type, self.home_splash_hash)
    
    
    def home_splash_url_as(self, ext = None, size = None):
        """
        Returns the guild's home splash's url. If the guild has no home splash, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated home splash, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_home_splash_url_as(self.id, self.home_splash_type, self.home_splash_hash, ext, size)
    
    
    @property
    def icon_url(self):
        """
        Returns the guild's icon's url. If the guild has no icon, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_icon_url(self.id, self.icon_type, self.icon_hash)
    
    
    def icon_url_as(self, ext = None, size = None):
        """
        Returns the guild's icon's url. If the guild has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated icon, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_icon_url_as(self.id, self.icon_type, self.icon_hash, ext, size)
    
    
    @property
    def invite_splash_url(self):
        """
        Returns the guild's invite splash's url. If the guild has no invite splash, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_invite_splash_url(self.id, self.invite_splash_type, self.invite_splash_hash)
    
    
    def invite_splash_url_as(self, ext = None, size = None):
        """
        Returns the guild's invite splash's url. If the guild has no invite splash, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the guild has animated invite splash, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_invite_splash_url_as(self.id, self.invite_splash_type, self.invite_splash_hash, ext, size)
    
    
    @property
    def vanity_url(self):
        """
        Returns the guild's vanity invite's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_guild_vanity_invite_url(self.vanity_code)
        
    
    @property
    def widget_json_url(self):
        """
        Returns an url to request the guild's widget data.
        
        Returns
        -------
        url : `str`
        """
        return build_guild_widget_json_url(self.id)
    
    
    @property
    def widget_url(self):
        """
        Returns the guild's widget image's url in `.png` format.
        
        Returns
        -------
        url : `str`
        """
        return build_guild_widget_url(self.id)
    
    
    def widget_url_as(self, style = 'shield'):
        """
        Returns the guild's widget image's url in `.png` format.
        
        Parameters
        ----------
        style : `str` = `'shield'`, Optional
            The widget image's style. Can be any of: `'shield'`, `'banner1'`, `'banner2'`, `'banner3'`, `'banner4'`.
        
        Returns
        -------
        url : `str`
    
        Raises
        ------
        ValueError
            - If `style` was not passed as any of the expected values.
        """
        return build_guild_widget_url_as(self.id, style)
