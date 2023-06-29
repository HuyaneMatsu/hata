__all__ = ()

from scarletio import set_docs

from ....env import CACHE_PRESENCE

from ...channel import Channel
from ...emoji import Emoji
from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, flag_parser_factory, force_string_parser_factory, int_parser_factory,
    negated_bool_parser_factory, nullable_string_parser_factory, preinstanced_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_dictionary_putter_factory, entity_id_optional_putter_factory,
    entity_id_putter_factory, flag_putter_factory, force_string_putter_factory, int_optional_putter_factory,
    int_putter_factory, negated_bool_optional_putter_factory, nullable_string_optional_putter_factory,
    preinstanced_array_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_dictionary_validator_factory, entity_id_validator_factory, flag_validator_factory,
    force_string_validator_factory, int_conditional_validator_factory, int_options_validator_factory,
    nullable_entity_dictionary_validator_factory, nullable_entity_set_validator_factory,
    nullable_string_validator_factory, preinstanced_array_validator_factory, preinstanced_validator_factory
)
from ...localization import Locale
from ...localization.utils import LOCALE_DEFAULT
from ...role import Role
from ...scheduled_event import ScheduledEvent
from ...soundboard import SoundboardSound
from ...stage import Stage
from ...sticker import Sticker
from ...user import ClientUserBase, User, VoiceState

from ..embedded_activity_state import EmbeddedActivityState

from .constants import (
    AFK_TIMEOUT_DEFAULT, AFK_TIMEOUT_OPTIONS, DESCRIPTION_LENGTH_MAX, MAX_PRESENCES_DEFAULT,
    MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT, MAX_USERS_DEFAULT, MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT, NAME_LENGTH_MAX,
    NAME_LENGTH_MIN
)
from .flags import SystemChannelFlag
from .preinstanced import (
    ContentFilterLevel, GuildFeature, HubType, MFA, MessageNotificationLevel, NsfwLevel, VerificationLevel
)

# afk_channel_id

parse_afk_channel_id = entity_id_parser_factory('afk_channel_id')
put_afk_channel_id_into = entity_id_optional_putter_factory('afk_channel_id')
validate_afk_channel_id = entity_id_validator_factory('afk_channel_id', Channel)

# afk_timeout

parse_afk_timeout = int_parser_factory('afk_timeout', AFK_TIMEOUT_DEFAULT)
put_afk_timeout_into = int_putter_factory('afk_timeout')
validate_afk_timeout = int_options_validator_factory('afk_timeout', AFK_TIMEOUT_OPTIONS)

# approximate_online_count

parse_approximate_online_count = int_parser_factory('approximate_presence_count', 0)
put_approximate_online_count_into = int_putter_factory('approximate_presence_count')
validate_approximate_online_count = int_conditional_validator_factory(
    'approximate_online_count',
    0,
    lambda approximate_online_count : approximate_online_count >= 0,
    '>= 0',
)

# approximate_user_count

parse_approximate_user_count = int_parser_factory('approximate_member_count', 0)
put_approximate_user_count_into = int_putter_factory('approximate_member_count')
validate_approximate_user_count = int_conditional_validator_factory(
    'approximate_user_count',
    0,
    lambda approximate_user_count : approximate_user_count >= 0,
    '>= 0',
)

# available

parse_available = negated_bool_parser_factory('unavailable', True)
put_available_into = negated_bool_optional_putter_factory('unavailable', True)
validate_available = bool_validator_factory('unavailable', True)

# boost_progress_bar_enabled

parse_boost_progress_bar_enabled = bool_parser_factory('premium_progress_bar_enabled', False)
put_boost_progress_bar_enabled_into = bool_optional_putter_factory('premium_progress_bar_enabled', False)
validate_boost_progress_bar_enabled = bool_validator_factory('boost_progress_bar_enabled', False)

# boost_count

parse_boost_count = int_parser_factory('premium_subscription_count', 0)
put_boost_count_into = int_optional_putter_factory('premium_subscription_count', 0)
validate_boost_count = int_conditional_validator_factory(
    'boost_count',
    0,
    lambda boost_count : boost_count >= 0,
    '>= 0',
)

# channels

def parse_channels(data, channels, guild_id = 0):
    """
    Parses the guild's channels from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    channels : `dict<int, Channel>`
        The guild's channels.
    guild_id : `int` = `0`, Optional
        The guild's identifier.
        
    Returns
    -------
    channels : `dict<int, Channel>`
        Returns `channels` parameter.
    """
    if channels:
        old_channels = [*channels.values()]
        channels.clear()
    
    channel_datas = data.get('channels', None)
    if (channel_datas is not None):
        for channel_data in channel_datas:
            channel = Channel.from_data(channel_data, None, guild_id, strong_cache = False)
            channels[channel.id] = channel
    
    return channels


put_channels_into = entity_dictionary_putter_factory('channels', Channel, force_include_internals = True)
validate_channels = entity_dictionary_validator_factory('channels', Channel)

# client_guild_profile

def parse_client_guild_profile__cache_presence(data, users, guild_id):
    return users


def parse_client_guild_profile__no_cache_presence(data, users, guild_id):
    guild_profile_datas = data.get('members', None)
    if (guild_profile_datas is not None):
        for guild_profile_data in guild_profile_datas:
            user = User._bypass_no_cache(guild_profile_data['user'], guild_profile_data, guild_id)
            if (user is not None):
                users[user.id] = user
    
    return users


if CACHE_PRESENCE:
    parse_client_guild_profile = parse_client_guild_profile__cache_presence
else:
    parse_client_guild_profile = parse_client_guild_profile__no_cache_presence

set_docs(
    parse_client_guild_profile,
    """
    Parses the guild's client's guild profile data.
    
    > Used when presence caching is disabled.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    users : `dict<int, ClientUserBase>`
        The guild's users.
    guild_id : `int` = `0`
        The guild's identifier.
        
    Returns
    -------
    users : `dict<int, ClientUserBase>`
        Returns `users` parameter.
    """
)

# content_filter

parse_content_filter = preinstanced_parser_factory(
    'explicit_content_filter', ContentFilterLevel, ContentFilterLevel.disabled
)
put_content_filter_into = preinstanced_putter_factory('explicit_content_filter')
validate_content_filter = preinstanced_validator_factory('content_filter', ContentFilterLevel)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_optional_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# embedded_activity_states

def parse_embedded_activity_states(data, embedded_activity_states, guild_id = 0):
    """
    Parses the guild's embedded_activity_states from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    embedded_activity_states : `None | set<EmbeddedActivityState>`
        The guild's embedded activity states.
    guild_id : `int` = `0`, Optional
        The guild's identifier.
        
    Returns
    -------
    embedded_activity_states : `None | set<EmbeddedActivityState>`
        Returns the `embedded_activity_states` parameter.
    """
    if (embedded_activity_states is not None):
        old_embedded_activity_states = [*embedded_activity_states]
        embedded_activity_states.clear()
    
    embedded_activity_state_datas = data.get('embedded_activities', None)
    if (embedded_activity_state_datas is not None):
        for embedded_activity_state_data in embedded_activity_state_datas:
            embedded_activity_state = EmbeddedActivityState.from_data(
                embedded_activity_state_data, guild_id, strong_cache = False
            )
            
            if embedded_activity_states is None:
                embedded_activity_states = set()
                
            embedded_activity_states.add(embedded_activity_state)
    
    if (embedded_activity_states is not None) and (not embedded_activity_states):
        embedded_activity_states = None
    
    return embedded_activity_states


def put_embedded_activity_states_into(embedded_activity_states, data, defaults):
    """
    Puts the given embedded activity states into the given `data` json serializable object.
    
    Parameters
    ----------
    embedded_activity_states : `None | set<EmbeddedActivityState>`
        Entity array.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if embedded_activity_states is None:
        embedded_activity_state_datas = []
    else:
        embedded_activity_state_datas = [
            embedded_activity_state.to_data(defaults = defaults) for embedded_activity_state in embedded_activity_states
        ]
    
    data['embedded_activities'] = embedded_activity_state_datas
    
    return data

validate_embedded_activity_states = nullable_entity_set_validator_factory(
    'embedded_activity_states', EmbeddedActivityState
)

# emojis

def parse_emojis(data, emojis, guild_id = 0):
    """
    Parses the guild's emojis from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    emojis : `dict<int, Emoji>`
        The guild's emojis.
    guild_id : `int` = `0`, Optional
        The guild's identifier.
        
    Returns
    -------
    emojis : `dict<int, Emoji>`
        Returns `emojis` parameter.
    """
    if emojis:
        old_emojis = [*emojis.values()]
        emojis.clear()
    
    emoji_datas = data.get('emojis', None)
    if (emoji_datas is not None):
        for emoji_data in emoji_datas:
            emoji = Emoji.from_data(emoji_data, guild_id)
            emojis[emoji.id] = emoji
    
    return emojis

put_emojis_into = entity_dictionary_putter_factory('emojis', Emoji, force_include_internals = True)
validate_emojis = entity_dictionary_validator_factory('emojis', Emoji)

# features

parse_features = preinstanced_array_parser_factory('features', GuildFeature)
put_features_into = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', GuildFeature)

# hub_type

parse_hub_type = preinstanced_parser_factory('hub_type', HubType, HubType.none)
put_hub_type_into = preinstanced_putter_factory('hub_type')
validate_hub_type = preinstanced_validator_factory('hub_type', HubType)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('guild_id')

# large

parse_large = bool_parser_factory('large', False)
put_large_into = bool_optional_putter_factory('large', False)
validate_large = bool_validator_factory('large', False)

# max_presences

parse_max_presences = int_parser_factory('max_presences', MAX_PRESENCES_DEFAULT)
put_max_presences_into = int_putter_factory('max_presences')
validate_max_presences = int_conditional_validator_factory(
    'max_presences',
    MAX_PRESENCES_DEFAULT,
    (lambda max_presences : max_presences >= 0),
    '>= 0',
)

# max_stage_channel_video_users

parse_max_stage_channel_video_users = int_parser_factory(
    'max_stage_video_channel_users', MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT
)
put_max_stage_channel_video_users_into = int_putter_factory('max_stage_video_channel_users')
validate_max_stage_channel_video_users = int_conditional_validator_factory(
    'max_stage_channel_video_users',
    MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT,
    (lambda max_stage_channel_video_users : max_stage_channel_video_users >= 0),
    '>= 0',
)

# max_users

parse_max_users = int_parser_factory('max_members', MAX_USERS_DEFAULT)
put_max_users_into = int_putter_factory('max_members')
validate_max_users = int_conditional_validator_factory(
    'max_users',
    MAX_USERS_DEFAULT,
    (lambda max_users : max_users >= 0),
    '>= 0',
)

# max_voice_channel_video_users

parse_max_voice_channel_video_users = int_parser_factory(
    'max_video_channel_users', MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
)
put_max_voice_channel_video_users_into = int_putter_factory('max_video_channel_users')
validate_max_voice_channel_video_users = int_conditional_validator_factory(
    'max_voice_channel_video_users',
    MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT,
    (lambda max_voice_channel_video_users : max_voice_channel_video_users >= 0),
    '>= 0',
)

# message_notification

parse_message_notification = preinstanced_parser_factory(
    'default_message_notifications', MessageNotificationLevel, MessageNotificationLevel.all_messages
)
put_message_notification_into = preinstanced_putter_factory('default_message_notifications')
validate_message_notification = preinstanced_validator_factory('message_notification', MessageNotificationLevel)

# mfa

parse_mfa = preinstanced_parser_factory('mfa_level', MFA, MFA.none)
put_mfa_into = preinstanced_putter_factory('mfa_level')
validate_mfa = preinstanced_validator_factory('mfa', MFA)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# nsfw_level

parse_nsfw_level = preinstanced_parser_factory('nsfw_level', NsfwLevel, NsfwLevel.none)
put_nsfw_level_into = preinstanced_putter_factory('nsfw_level')
validate_nsfw_level = preinstanced_validator_factory('nsfw_level', NsfwLevel)

# owner_id

parse_owner_id = entity_id_parser_factory('owner_id')
put_owner_id_into = entity_id_putter_factory('owner_id')
validate_owner_id = entity_id_validator_factory('owner_id', ClientUserBase)

# preferred_locale

parse_preferred_locale = preinstanced_parser_factory('preferred_locale', Locale, LOCALE_DEFAULT)
put_preferred_locale_into = preinstanced_putter_factory('preferred_locale')
validate_preferred_locale = preinstanced_validator_factory('preferred_locale', Locale)

# premium_tier

parse_premium_tier = int_parser_factory('premium_tier', 0)
put_premium_tier_into = int_putter_factory('premium_tier')
validate_premium_tier = int_options_validator_factory('premium_tier', frozenset((range(4))))

# public_updates_channel_id

parse_public_updates_channel_id = entity_id_parser_factory('public_updates_channel_id')
put_public_updates_channel_id_into = entity_id_optional_putter_factory('public_updates_channel_id')
validate_public_updates_channel_id = entity_id_validator_factory('public_updates_channel_id', Channel)

# roles

def parse_roles(data, roles, guild_id = 0):
    """
    Parses the guild's roles from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    roles : `dict<int, Role>`
        The guild's roles.
    guild_id : `int` = `0`, Optional
        The guild's identifier.
        
    Returns
    -------
    roles : `dict<int, Role>`
        Returns `roles` parameter.
    """
    if roles:
        old_roles = [*roles.values()]
        roles.clear()
    
    role_datas = data.get('roles', None)
    if (role_datas is not None):
        for role_data in role_datas:
            role = Role.from_data(role_data, guild_id, strong_cache = False)
            roles[role.id] = role
    
    return roles

put_roles_into = entity_dictionary_putter_factory('roles', Role, force_include_internals = True)
validate_roles = entity_dictionary_validator_factory('roles', Role)

# rules_channel_id

parse_rules_channel_id = entity_id_parser_factory('rules_channel_id')
put_rules_channel_id_into = entity_id_optional_putter_factory('rules_channel_id')
validate_rules_channel_id = entity_id_validator_factory('rules_channel_id', Channel)

# safety_alerts_channel_id

parse_safety_alerts_channel_id = entity_id_parser_factory('safety_alerts_channel_id')
put_safety_alerts_channel_id_into = entity_id_optional_putter_factory('safety_alerts_channel_id')
validate_safety_alerts_channel_id = entity_id_validator_factory('safety_alerts_channel_id', Channel)

# soundboard_sounds

validate_soundboard_sounds = nullable_entity_dictionary_validator_factory('soundboard_sounds', SoundboardSound)

# scheduled_events

def parse_scheduled_events(data, scheduled_events):
    """
    Parses the guild's scheduled_events from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    scheduled_events : `dict<int, ScheduledEvent>`
        The guild's scheduled_events.
        
    Returns
    -------
    scheduled_events : `dict<int, ScheduledEvent>`
        Returns `scheduled_events` parameter.
    """
    if scheduled_events:
        old_scheduled_events = [*scheduled_events.values()]
        scheduled_events.clear()
    
    scheduled_event_datas = data.get('guild_scheduled_events', None)
    if (scheduled_event_datas is not None):
        for scheduled_event_data in scheduled_event_datas:
            scheduled_event = ScheduledEvent.from_data(scheduled_event_data, strong_cache = False)
            scheduled_events[scheduled_event.id] = scheduled_event
    
    return scheduled_events

put_scheduled_events_into = entity_dictionary_putter_factory(
    'guild_scheduled_events', ScheduledEvent, force_include_internals = True
)
validate_scheduled_events = entity_dictionary_validator_factory('scheduled_events', ScheduledEvent)

# stages

def parse_stages(data, stages):
    """
    Parses the guild's stages from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    stages : `None`, `dict<int, Stage>`
        The guild's stages.
        
    Returns
    -------
    stages : `None`, `dict<int, Stage>`
        Returns `stages` parameter.
    """
    if (stages is not None):
        old_stages = [*stages.values()]
        stages.clear()
    
    stage_datas = data.get('stage_instances', None)
    if (stage_datas is not None):
        for stage_data in stage_datas:
            stage = Stage.from_data(stage_data, strong_cache = False)
            
            if stages is None:
                stages = {}
            
            stages[stage.id] = stage
    
    if (stages is not None) and (not stages):
        stages = None
    
    return stages


put_stages_into = entity_dictionary_putter_factory(
    'stage_instances', Stage, force_include_internals = True
)
validate_stages = nullable_entity_dictionary_validator_factory('stages', Stage)

# stickers

def parse_stickers(data, stickers):
    """
    Parses the guild's stickers from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    stickers : `dict<int, Sticker>`
        The guild's stickers.
        
    Returns
    -------
    stickers : `dict<int, Sticker>`
        Returns `stickers` parameter.
    """
    if stickers:
        old_stickers = [*stickers.values()]
        stickers.clear()
    
    sticker_datas = data.get('stickers', None)
    if (sticker_datas is not None):
        for sticker_data in sticker_datas:
            sticker = Sticker.from_data(sticker_data)
            stickers[sticker.id] = sticker
    
    return stickers

put_stickers_into = entity_dictionary_putter_factory('stickers', Sticker, force_include_internals = True)
validate_stickers = entity_dictionary_validator_factory('stickers', Sticker)

# system_channel_flags

parse_system_channel_flags = flag_parser_factory(
    'system_channel_flags', SystemChannelFlag, default_value = SystemChannelFlag.NONE
)
put_system_channel_flags_into = flag_putter_factory('system_channel_flags')
validate_system_channel_flags = flag_validator_factory(
    'system_channel_flags', SystemChannelFlag, default_value = SystemChannelFlag.NONE
)

# system_channel_id

parse_system_channel_id = entity_id_parser_factory('system_channel_id')
put_system_channel_id_into = entity_id_optional_putter_factory('system_channel_id')
validate_system_channel_id = entity_id_validator_factory('system_channel_id', Channel)

# threads

def parse_threads(data, threads, guild_id = 0):
    """
    Parses the guild's threads from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    threads : `dict<int, Channel>`
        The guild's threads.
    guild_id : `int` = `0`, Optional
        The guild's identifier.
        
    Returns
    -------
    threads : `dict<int, Channel>`
        Returns `threads` parameter.
    """
    if threads:
        old_threads = [*threads.values()]
        threads.clear()
    
    thread_datas = data.get('threads', None)
    if (thread_datas is not None):
        for thread_data in thread_datas:
            thread = Channel.from_data(thread_data, None, guild_id, strong_cache = False)
            threads[thread.id] = thread
    
    return threads


put_threads_into = entity_dictionary_putter_factory('threads', Channel, force_include_internals = True)
validate_threads = entity_dictionary_validator_factory('threads', Channel)

# user_count

parse_user_count = int_parser_factory('member_count', 0)
put_user_count_into = int_putter_factory('member_count')
validate_user_count = int_conditional_validator_factory(
    'user_count',
    0,
    lambda user_count : user_count >= 0,
    '>= 0',
)

# users

def parse_users__cache_presence(data, users, guild_id = 0):
    if users:
        old_users = [*users.values()]
        users.clear()
    
    guild_profile_datas = data.get('members', None)
    if (guild_profile_datas is not None):
        for guild_profile_data in guild_profile_datas:
            user = User.from_data(guild_profile_data['user'], guild_profile_data, guild_id, strong_cache = False)
            users[user.id] = user
    
    presence_datas = data.get('presences', None)
    if (presence_datas is not None):
        for presence_data in presence_datas:
            user_id = int(presence_data['user']['id'])
            try:
                user = users[user_id]
            except KeyError:
                pass
            else:
                user._update_presence(presence_data)
    
    return users


def parse_users__no_cache_presence(data, users, guild_id = 0):
    users.clear()
    return users


if CACHE_PRESENCE:
    parse_users = parse_users__cache_presence
else:
    parse_users = parse_users__no_cache_presence


set_docs(
    parse_users,
    """
    Parses the guild's users from the given data.
    
    > Used when presence caching is enabled.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    users : `dict<int, ClientUserBase>`
        The guild's users.
    guild_id : `int` = `0`, Optional
        The guild's identifier.
        
    Returns
    -------
    users : `dict<int, ClientUserBase>`
        Returns `users` parameter.
    """
)


def put_users_into(users, data, defaults, *, guild_id = 0):
    """
    Puts the given `users` into the given `data` json serializable object.
    
    Parameters
    ----------
    users : `dict`, ``WeakValueDictionary``  of (`int`, ``ClientUserBase``) items
        Resolved users.
    data : `dict` of (`str`, `object`) items
        Interaction resolved data.
    defaults : `bool`
        Whether default fields values should be included as well.
    guild_id : `int` = `0`, Optional (keyword only)
        The guild's identifier.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    guild_profiles_datas = []
    
    if guild_id:
        for user in users.values():
            try:
                guild_profile = user.guild_profiles[guild_id]
            except KeyError:
                continue
            
            guild_profile_data = guild_profile.to_data(defaults = defaults, include_internals = True)
            guild_profile_data['user'] = user.to_data(defaults = defaults, include_internals = True)
            guild_profiles_datas.append(guild_profile_data)
            continue
    
    data['members'] = guild_profiles_datas
    
    return data


validate_users = entity_dictionary_validator_factory('users', ClientUserBase)

# vanity_code

parse_vanity_code = nullable_string_parser_factory('vanity_url_code')
put_vanity_code_into = nullable_string_optional_putter_factory('vanity_url_code')
validate_vanity_code = nullable_string_validator_factory('vanity_code', 0, 1024)

# verification_level

parse_verification_level = preinstanced_parser_factory('verification_level', VerificationLevel, VerificationLevel.none)
put_verification_level_into = preinstanced_putter_factory('verification_level')
validate_verification_level = preinstanced_validator_factory('verification_level', VerificationLevel)

# voice_states

def parse_voice_states(data, voice_states, guild_id = 0):
    """
    Parses the guild's voice_states from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Guild data.
    voice_states : `dict<int, VoiceState>`
        The guild's voice_states.
        
    Returns
    -------
    voice_states : `dict<int, VoiceState>`
        Returns `voice_states` parameter.
    guild_id : `int` = `0`, Optional
        The guild's identifier.
    """
    if voice_states:
        voice_states.clear()
    
    voice_state_datas = data.get('voice_states', None)
    if (voice_state_datas is not None):
        for voice_state_data in voice_state_datas:
            voice_state = VoiceState.from_data(voice_state_data, guild_id, strong_cache = False)
            if (voice_state is not None):
                voice_states[voice_state.user_id] = voice_state
    
    return voice_states


put_voice_states_into = entity_dictionary_putter_factory('voice_states', VoiceState)


def validate_voice_states(field_value):
    """
    Validates the given voice states field.
    
    Parameters
    ----------
    field_value : `None`, `iterable` of ``VoiceState``, `dict` of (`int`, ``VoiceState``) items
        The field value to validate.
    
    Returns
    -------
    entity_dictionary : `dict` of (`int`, ``VoiceState``) items
    
    Raises
    ------
    TypeError
        - If `field_value`'s or it's elements type is incorrect.
    """
    validated = {}
    
    if field_value is not None:
        if isinstance(field_value, dict):
            iterator = iter(field_value.values())
        
        elif (getattr(field_value, '__iter__', None) is not None):
            iterator = iter(field_value)
        
        else:
            raise TypeError(
                f'`voice_states` can be `None`, `dict` of (`int`, `{VoiceState.__name__}`) items, `iterable` of '
                f'`{VoiceState.__name__}` items, got {field_value.__class__.__name__}; {field_value!r}.'
            )
        
        for voice_state in iterator:
            if not isinstance(voice_state, VoiceState):
                raise TypeError(
                    f'`voice_states` elements can be `{VoiceState.__name__}`, got {voice_state.__class__.__name__}; '
                    f'{voice_state!r}; voice_states = {field_value!r}.'
                )
            
            validated[voice_state.user_id] = voice_state
    
    return validated

# widget_channel_id

parse_widget_channel_id = entity_id_parser_factory('widget_channel_id')
put_widget_channel_id_into = entity_id_optional_putter_factory('widget_channel_id')
validate_widget_channel_id = entity_id_validator_factory('widget_channel_id', Channel)

# widget_enabled

parse_widget_enabled = bool_parser_factory('widget_enabled', False)
put_widget_enabled_into = bool_optional_putter_factory('widget_enabled', False)
validate_widget_enabled = bool_validator_factory('widget_enabled', False)


# ---- extra ----

def validate_channels_and_channel_datas(channels):
    """
    Validates the given `channels` value. This function is used when creating a new guild.
    
    Parameters
    ----------
    channels : `None`, `list` of (``Channel``, `dict`)
    
    Returns
    -------
    validated : `None`, `list` of (``Channel``, `dict`)
    
    Raises
    ------
    TypeError
        - If a `channel`'s type is incorrect.
    ValueError
        - If a `channel`'s channels is incorrect.
    """
    validated = None
    
    if channels is None:
        pass
    
    elif isinstance(channels, list):
        for element in channels:
            if not isinstance(element, (Channel, dict)):
                raise TypeError(
                    f'`channel` elements can be `{Channel.__name__}`, `dict`. '
                    f'Got {element.__class__.__name__}; {element!r}; channels = {channels!r}'
                )
        
            if validated is None:
                validated = []
            
            validated.append(element)
    
    else:
        raise TypeError(
            f'`channels` can be `None` or `dict` of `{Channel.__name__}`, `dict` elements. '
            f'Got {channels.__class__.__name__}; {channels!r}.'
        )
    
    return validated


def validate_roles_and_role_datas(roles):
    """
    Validates the given `roles` value. This function is used when creating a new guild.
    
    Parameters
    ----------
    roles : `None`, `list` of (``Role``, `dict`)
    
    Returns
    -------
    validated : `None`, `list` of (``Role``, `dict`)
    
    Raises
    ------
    TypeError
        - If a `role`'s type is incorrect.
    ValueError
        - If a `role`'s roles is incorrect.
    """
    validated = None
    
    if roles is None:
        pass
    
    elif isinstance(roles, list):
        for element in roles:
            if not isinstance(element, (Role, dict)):
                raise TypeError(
                    f'`role` elements can be `{Role.__name__}`, `dict`. '
                    f'Got {element.__class__.__name__}; {element!r}; roles = {roles!r}'
                )
        
            if validated is None:
                validated = []
            
            validated.append(element)
    
    else:
        raise TypeError(
            f'`roles` can be `None` or `dict` of `{Role.__name__}`, `dict` elements. '
            f'Got {roles.__class__.__name__}; {roles!r}.'
        )
    
    return validated


def put_channels_and_channel_datas_into(channels, data, defaults):
    """
    Puts the given channels or their data into the given `data` json serializable object.
    
    Parameters
    ----------
    channels : `None`, `list` of (``Channel``, `dict`)
        Channels or channel datas.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    channel_datas = []
    
    if (channels is not None):
        for channel in channels:
            if isinstance(channel, Channel):
                channel_data = channel.to_data(defaults = defaults, include_internals = True)
            else:
                channel_data = channel
            channel_datas.append(channel_data)
    
    data['channels'] = channel_datas
    return data


def put_roles_and_role_datas_into(roles, data, defaults):
    """
    Puts the given roles or their data into the given `data` json serializable object.
    
    Parameters
    ----------
    roles : `None`, `list` of (``Role``, `dict`)
        Roles or role datas.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    role_datas = []
    
    if (roles is not None):
        for role in roles:
            if isinstance(role, Role):
                role_data = role.to_data(defaults = defaults, include_internals = True)
            else:
                role_data = role
            role_datas.append(role_data)
    
    data['roles'] = role_datas
    return data
