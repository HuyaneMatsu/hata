__all__ = (
    'create_interaction_guild_data', 'create_partial_guild_data', 'create_partial_guild_from_data',
    'create_partial_guild_from_id', 'create_partial_guild_from_interaction_guild_data'
)

from functools import partial as partial_func

from scarletio import export

from ...core import GUILDS

from .fields import (
    parse_available, parse_description, parse_features, parse_id, parse_locale, parse_name, parse_nsfw_level,
    parse_verification_level, put_afk_channel_id, put_afk_timeout, put_available,
    put_boost_progress_bar_enabled, put_channels_and_channel_datas,
    put_default_message_notification_level, put_description, put_explicit_content_filter_level,
    put_features, put_hub_type, put_id, put_locale, put_mfa_level, put_name,
    put_nsfw_level, put_owner_id, put_public_updates_channel_id, put_roles_and_role_datas,
    put_rules_channel_id, put_safety_alerts_channel_id, put_system_channel_flags,
    put_system_channel_id, put_vanity_code, put_verification_level, put_widget_channel_id,
    put_widget_enabled, validate_afk_channel_id, validate_afk_timeout, validate_boost_progress_bar_enabled,
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
    'afk_channel_id': (validate_afk_channel_id, put_afk_channel_id),
    'afk_timeout': (validate_afk_timeout, put_afk_timeout),
    'banner': (
        partial_func(GUILD_BANNER.validate_icon, allow_data = True),
        partial_func(GUILD_BANNER.put_into, as_data = True),
    ),
    'boost_progress_bar_enabled': (validate_boost_progress_bar_enabled, put_boost_progress_bar_enabled),
    'default_message_notification_level': (
        validate_default_message_notification_level, put_default_message_notification_level)
    ,
    'description': (validate_description, put_description),
    'discovery_splash': (
        partial_func(GUILD_DISCOVERY_SPLASH.validate_icon, allow_data = True),
        partial_func(GUILD_DISCOVERY_SPLASH.put_into, as_data = True),
    ),
    'explicit_content_filter_level': (validate_explicit_content_filter_level, put_explicit_content_filter_level),
    'features': (validate_features, put_features),
    'hub_type': (validate_hub_type, put_hub_type),
    'icon': (
        partial_func(GUILD_ICON.validate_icon, allow_data = True),
        partial_func(GUILD_ICON.put_into, as_data = True),
    ),
    'invite_splash': (
        partial_func(GUILD_INVITE_SPLASH.validate_icon, allow_data = True),
        partial_func(GUILD_INVITE_SPLASH.put_into, as_data = True),
    ),
    'locale': (validate_locale, put_locale),
    'mfa_level': (validate_mfa_level, put_mfa_level),
    'name': (validate_name, put_name),
    'nsfw_level': (validate_nsfw_level, put_nsfw_level),
    'owner_id': (validate_owner_id, put_owner_id),
    'public_updates_channel_id': (validate_public_updates_channel_id, put_public_updates_channel_id),
    'rules_channel_id': (validate_rules_channel_id, put_rules_channel_id),
    'safety_alerts_channel_id': (validate_safety_alerts_channel_id, put_safety_alerts_channel_id),
    'system_channel_flags': (validate_system_channel_flags, put_system_channel_flags),
    'system_channel_id': (validate_system_channel_id, put_system_channel_id),
    'vanity_code': (validate_vanity_code, put_vanity_code),
    'verification_level': (validate_verification_level, put_verification_level),
    'widget_channel_id': (validate_widget_channel_id, put_widget_channel_id),
    'widget_enabled': (validate_widget_enabled, put_widget_enabled),
}


# We need to ignore client adding, because clients count to being not partial.
# If a guild is not partial it wont get update on Guild.__new__

def create_partial_guild_from_data(data):
    """
    Creates a partial guild from partial guild data.
    
    Parameters
    ----------
    data : `dict<str, object>`
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
    
    put_available(guild.available, data, True)
    put_description(guild.description, data, True)
    type(guild).discovery_splash.put_into(guild.discovery_splash, data, True, as_data = False)
    put_features(guild.features, data, True)
    put_id(guild.id, data, True)
    type(guild).icon.put_into(guild.icon, data, True, as_data = False)
    type(guild).invite_splash.put_into(guild.invite_splash, data, True, as_data = False)
    put_name(guild.name, data, True)
    put_nsfw_level(guild.nsfw_level, data, True)
    put_verification_level(guild.verification_level, data, True)
    
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
    afk_channel_id : `None | int`, Optional (Keyword only)
        The id of the guild's afk channel. The id should be one of the channel's id from `channels`.
    
    afk_timeout : `None | int` = `None`, Optional (Keyword only)
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
    
    # default_message_notification_level
    if default_message_notification_level is ...:
        default_message_notification_level = MessageNotificationLevel.all_messages
    else:
        default_message_notification_level = validate_default_message_notification_level(default_message_notification_level)
    
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
    put_name(name, data, True)
    put_afk_channel_id(afk_channel_id, data, True)
    put_afk_timeout(afk_timeout, data, False)
    put_channels_and_channel_datas(channels, data, True)
    put_explicit_content_filter_level(explicit_content_filter_level, data, True)
    GUILD_ICON.put_into(icon, data, defaults = True, as_data = True)
    put_roles_and_role_datas(roles, data,  True)
    put_default_message_notification_level(default_message_notification_level, data, True)
    put_system_channel_id(system_channel_id, data, True)
    put_system_channel_flags(system_channel_flags, data, True)
    put_verification_level(verification_level, data, True)
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
    
    put_id(guild.id, data, True)
    put_locale(guild.locale, data, True)
    put_features(guild.features, data, True)
    
    return data
