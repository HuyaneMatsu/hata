__all__ = (
    'create_interaction_guild_data', 'create_partial_guild_data', 'create_partial_guild_from_data',
    'create_partial_guild_from_id', 'create_partial_guild_from_interaction_guild_data'
)

from functools import partial as partial_func
from warnings import warn

from scarletio import export

from ...core import GUILDS

from .fields import (
    parse_available, parse_description, parse_features, parse_id, parse_locale, parse_name, parse_nsfw_level,
    parse_verification_level, put_afk_channel_id_into, put_afk_timeout_into, put_available_into,
    put_boost_progress_bar_enabled_into, put_channels_and_channel_datas_into,
    put_default_message_notification_level_into, put_description_into, put_explicit_content_filter_level_into,
    put_features_into, put_hub_type_into, put_id_into, put_locale_into, put_mfa_level_into, put_name_into,
    put_nsfw_level_into, put_owner_id_into, put_public_updates_channel_id_into, put_roles_and_role_datas_into,
    put_rules_channel_id_into, put_safety_alerts_channel_id_into, put_system_channel_flags_into,
    put_system_channel_id_into, put_vanity_code_into, put_verification_level_into, put_widget_channel_id_into,
    put_widget_enabled_into, validate_afk_channel_id, validate_afk_timeout, validate_boost_progress_bar_enabled,
    validate_channels_and_channel_datas, validate_default_message_notification_level, validate_description,
    validate_explicit_content_filter_level, validate_features, validate_hub_type, validate_locale, validate_mfa_level,
    validate_name, validate_nsfw_level, validate_owner_id, validate_public_updates_channel_id,
    validate_roles_and_role_datas, validate_rules_channel_id, validate_safety_alerts_channel_id,
    validate_system_channel_flags, validate_system_channel_id, validate_vanity_code, validate_verification_level,
    validate_widget_channel_id, validate_widget_enabled
)
from .flags import SystemChannelFlag
from .guild import GUILD_BANNER, GUILD_DISCOVERY_SPLASH, GUILD_ICON, GUILD_INVITE_SPLASH, Guild
from .preinstanced import ExplicitContentFilterLevel, MessageNotificationLevel, NsfwLevel, VerificationLevel


GUILD_FIELD_CONVERTERS = {
    'afk_channel_id': (validate_afk_channel_id, put_afk_channel_id_into),
    'afk_timeout': (validate_afk_timeout, put_afk_timeout_into),
    'banner': (
        partial_func(GUILD_BANNER.validate_icon, allow_data = True),
        partial_func(GUILD_BANNER.put_into, as_data = True),
    ),
    'boost_progress_bar_enabled': (validate_boost_progress_bar_enabled, put_boost_progress_bar_enabled_into),
    'default_message_notification_level': (
        validate_default_message_notification_level, put_default_message_notification_level_into)
    ,
    'description': (validate_description, put_description_into),
    'discovery_splash': (
        partial_func(GUILD_DISCOVERY_SPLASH.validate_icon, allow_data = True),
        partial_func(GUILD_DISCOVERY_SPLASH.put_into, as_data = True),
    ),
    'explicit_content_filter_level': (validate_explicit_content_filter_level, put_explicit_content_filter_level_into),
    'features': (validate_features, put_features_into),
    'hub_type': (validate_hub_type, put_hub_type_into),
    'icon': (
        partial_func(GUILD_ICON.validate_icon, allow_data = True),
        partial_func(GUILD_ICON.put_into, as_data = True),
    ),
    'invite_splash': (
        partial_func(GUILD_INVITE_SPLASH.validate_icon, allow_data = True),
        partial_func(GUILD_INVITE_SPLASH.put_into, as_data = True),
    ),
    'locale': (validate_locale, put_locale_into),
    'mfa_level': (validate_mfa_level, put_mfa_level_into),
    'name': (validate_name, put_name_into),
    'nsfw_level': (validate_nsfw_level, put_nsfw_level_into),
    'owner_id': (validate_owner_id, put_owner_id_into),
    'public_updates_channel_id': (validate_public_updates_channel_id, put_public_updates_channel_id_into),
    'rules_channel_id': (validate_rules_channel_id, put_rules_channel_id_into),
    'safety_alerts_channel_id': (validate_safety_alerts_channel_id, put_safety_alerts_channel_id_into),
    'system_channel_flags': (validate_system_channel_flags, put_system_channel_flags_into),
    'system_channel_id': (validate_system_channel_id, put_system_channel_id_into),
    'vanity_code': (validate_vanity_code, put_vanity_code_into),
    'verification_level': (validate_verification_level, put_verification_level_into),
    'widget_channel_id': (validate_widget_channel_id, put_widget_channel_id_into),
    'widget_enabled': (validate_widget_enabled, put_widget_enabled_into),
}


# We need to ignore client adding, because clients count to being not partial.
# If a guild is not partial it wont get update on Guild.__new__

def create_partial_guild_from_data(data):
    """
    Creates a partial guild from partial guild data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Partial channel data received from Discord.
    
    Returns
    -------
    guild : ``Guild``
    """
    guild_id = parse_id(data)
    try:
        return GUILDS[guild_id]
    except KeyError:
        pass
    
    guild = Guild._create_empty(guild_id)
    
    guild.available = parse_available(data)
    guild.description = parse_description(data)
    guild._set_banner(data)
    guild._set_discovery_splash(data)
    guild._set_icon(data)
    guild._set_invite_splash(data)
    guild.name = parse_name(data)
    
    # Optional
    features = parse_features(data)
    if (features is not None):
        guild.features = features
    
    nsfw_level = parse_nsfw_level(data)
    if nsfw_level is not NsfwLevel.none:
        guild.nsfw_level = nsfw_level
    
    verification_level = parse_verification_level(data)
    if verification_level is not VerificationLevel.none:
        guild.verification_level = verification_level
        
    GUILDS[guild_id] = guild
    
    return guild


def create_partial_guild_data(guild):
    """
    Creates partial guild data. The opposite of ``create_partial_guild_from_data``.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to serialize.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    
    put_available_into(guild.available, data, True)
    put_description_into(guild.description, data, True)
    type(guild).discovery_splash.put_into(guild.discovery_splash, data, True, as_data = False)
    put_features_into(guild.features, data, True)
    put_id_into(guild.id, data, True)
    type(guild).icon.put_into(guild.icon, data, True, as_data = False)
    type(guild).invite_splash.put_into(guild.invite_splash, data, True, as_data = False)
    put_name_into(guild.name, data, True)
    put_nsfw_level_into(guild.nsfw_level, data, True)
    put_verification_level_into(guild.verification_level, data, True)
    
    return data


@export
def create_partial_guild_from_id(guild_id):
    """
    Creates a guild from the given identifier and stores it in the cache as well. If the guild already exists,
    returns that instead.
    
    Parameters
    ----------
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    guild : ``Guild``
        The created guild instance.
    """
    try:
        guild = GUILDS[guild_id]
    except KeyError:
        guild = Guild._create_empty(guild_id)
        GUILDS[guild_id] = guild
    
    return guild


def create_new_guild_data(
    *,
    afk_channel_id = ...,
    afk_timeout = ...,
    channels = ...,
    content_filter = ...,
    message_notification = ...,
    default_message_notification_level = ...,
    explicit_content_filter_level = ...,
    icon = ...,
    name = ...,
    roles = ...,
    system_channel_flags = ...,
    system_channel_id = ...,
    verification_level = ...,
):
    """
    Helper function to create guild create data.
    
    Parameters
    ----------
    afk_channel_id : `None`, `int`, Optional (Keyword only)
        The id of the guild's afk channel. The id should be one of the channel's id from `channels`.
    
    afk_timeout : `None`, `int` = `None`, Optional (Keyword only)
        The afk timeout for the users at the guild's afk channel.
    
    channels : `None`, `list` of `dict`, Optional (Keyword only)
        A list of channels of the new guild. It should contain channel data objects.
    
    default_message_notification_level : ``MessageNotificationLevel``, `int`, Optional (Keyword only)
        The message notification level of the new guild.
    
    explicit_content_filter_level : ``ExplicitContentFilterLevel``, `int`, Optional (Keyword only)
        The content filter level of the guild.
    
    icon : `None`, `bytes-like`, Optional (Keyword only)
        The icon of the new guild.
    
    name : `str`, Optional (Keyword only)
        The name of the new guild.
    
    roles : `None`, `list` of (`dict<str, object>`, ``Role``), Optional (Keyword only)
        A list of roles of the new guild. It should contain role data objects.
    
    system_channel_flags : ``SystemChannelFlag``, `int`, Optional (Keyword only)
        Describe which type of messages are sent automatically to the system channel.
    
    system_channel_id: `int`, Optional (Keyword only)
        The id of the guild's system channel. The id should be one of the channel's id from `channels`.
    
    verification_level : ``VerificationLevel``, `int`, Optional (Keyword only)
        The verification level of the new guild.
    
    Returns
    -------
    data : `dict<str, object>`
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
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
    
    # channels
    if channels is ...:
        channels = None
    else:
        channels = validate_channels_and_channel_datas(channels)
    
    
    if message_notification is not ...:
        warn(
            (
                f'`{create_new_guild_data.__name__}`\'s `message_notification` parameter is deprecated. '
                f'And will be removed in 2024 April. '
                f'Please use `default_message_notification_level` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        default_message_notification_level = message_notification
    
    # default_message_notification_level
    if default_message_notification_level is ...:
        default_message_notification_level = MessageNotificationLevel.all_messages
    else:
        default_message_notification_level = validate_default_message_notification_level(default_message_notification_level)
    
    
    if content_filter is not ...:
        warn(
            (
                f'`{create_new_guild_data.__name__}`\'s `content_filter` parameter is deprecated. '
                f'And will be removed in 2024 April. '
                f'Please use `explicit_content_filter_level` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        explicit_content_filter_level = content_filter
    
    # explicit_content_filter_level
    if explicit_content_filter_level is ...:
        explicit_content_filter_level = ExplicitContentFilterLevel.disabled
    else:
        explicit_content_filter_level = validate_explicit_content_filter_level(explicit_content_filter_level)
    
    if icon is ...:
        icon = None
    else:
        icon = GUILD_ICON.validate_icon(icon, allow_data = True)
    
    # name
    if name is ...:
        name = ''
    else:
        name = validate_name(name)
    
    # roles
    if roles is ...:
        roles = None
    else:
        roles = validate_roles_and_role_datas(roles)
    
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
    
    # verification_level
    if verification_level is ...:
        verification_level = VerificationLevel.none
    else:
        verification_level = validate_verification_level(verification_level)
    
    data = {}
    put_name_into(name, data, True)
    put_afk_channel_id_into(afk_channel_id, data, True)
    put_afk_timeout_into(afk_timeout, data, False)
    put_channels_and_channel_datas_into(channels, data, True)
    put_explicit_content_filter_level_into(explicit_content_filter_level, data, True)
    GUILD_ICON.put_into(icon, data, defaults = True, as_data = True)
    put_roles_and_role_datas_into(roles, data,  True)
    put_default_message_notification_level_into(default_message_notification_level, data, True)
    put_system_channel_id_into(system_channel_id, data, True)
    put_system_channel_flags_into(system_channel_flags, data, True)
    put_verification_level_into(verification_level, data, True)
    return data


def create_partial_guild_from_interaction_guild_data(data):
    """
    Creates a partial guild from the guild data received through an interaction.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Interaction guild data.
    
    Returns
    -------
    guild : ``Guild``
    """
    guild_id = parse_id(data)
    try:
        guild = GUILDS[guild_id]
    except KeyError:
        guild = Guild._create_empty(guild_id)
        GUILDS[guild_id] = guild
    
    guild.locale = parse_locale(data)
    guild.features = parse_features(data)
    
    return guild


def create_interaction_guild_data(guild):
    """
    Creates interaction guild data.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to serialise.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    
    put_id_into(guild.id, data, True)
    put_locale_into(guild.locale, data, True)
    put_features_into(guild.features, data, True)
    
    return data
