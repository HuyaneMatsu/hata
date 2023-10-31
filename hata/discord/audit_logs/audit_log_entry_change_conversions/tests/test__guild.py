from ....guild import (
    ContentFilterLevel, HubType, MFA, MessageNotificationLevel, NsfwLevel, SystemChannelFlag, VerificationLevel
)
from ....guild.guild.constants import (
    AFK_TIMEOUT_DEFAULT, MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT, MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT
)
from ....guild.guild.fields import (
    validate_afk_channel_id, validate_afk_timeout, validate_boost_progress_bar_enabled, validate_content_filter,
    validate_description, validate_hub_type, validate_locale, validate_max_stage_channel_video_users,
    validate_max_voice_channel_video_users, validate_message_notification, validate_mfa, validate_name,
    validate_nsfw_level, validate_owner_id, validate_public_updates_channel_id, validate_rules_channel_id,
    validate_safety_alerts_channel_id, validate_system_channel_flags, validate_system_channel_id, validate_vanity_code,
    validate_verification_level, validate_widget_channel_id, validate_widget_enabled
)
from ....guild.guild.guild import GUILD_BANNER, GUILD_DISCOVERY_SPLASH, GUILD_ICON, GUILD_INVITE_SPLASH
from ....localization import Locale
from ....localization.utils import LOCALE_DEFAULT
from ....bases import Icon
from ...audit_log_change.flags import FLAG_IS_MODIFICATION
from ...audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ...conversion_helpers.converters import (
    get_converter_description, get_converter_id, get_converter_name, put_converter_description, put_converter_id,
    put_converter_name
)
import vampytest
from ..guild import (
    GUILD_CONVERSIONS,
    AFK_CHANNEL_ID_CONVERSION,
    AFK_TIMEOUT_CONVERSION,
    BANNER_CONVERSION,
    BOOST_PROGRESS_BAR_ENABLED_CONVERSION,
    CONTENT_FILTER_CONVERSION,
    DESCRIPTION_CONVERSION,
    DISCOVERY_SPLASH_CONVERSION,
    HUB_TYPE_CONVERSION,
    ICON_CONVERSION,
    LOCALE_CONVERSION,
    MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION,
    MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION,
    MFA_CONVERSION,
    MESSAGE_NOTIFICATION_CONVERSION,
    NAME_CONVERSION,
    NSFW_LEVEL_CONVERSION,
    OWNER_ID_CONVERSION,
    PUBLIC_UPDATES_CHANNEL_ID_CONVERSION,
    RULES_CHANNEL_ID_CONVERSION,
    SAFETY_ALERTS_CHANNEL_ID_CONVERSION,
    INVITE_SPLASH_CONVERSION,
    SYSTEM_CHANNEL_ID_CONVERSION,
    SYSTEM_CHANNEL_FLAGS_CONVERSION,
    VANITY_CODE_CONVERSION,
    VERIFICATION_LEVEL_CONVERSION,
    WIDGET_CHANNEL_ID_CONVERSION,
    WIDGET_ENABLED_CONVERSION,
)



def test__GUILD_CONVERSIONS():
    """
    Tests whether `GUILD_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*GUILD_CONVERSIONS.get_converters.keys()},
        {
            'afk_channel_id', 'afk_timeout', 'banner_hash', 'premium_progress_bar_enabled', 'explicit_content_filter',
            'description', 'discovery_splash_hash', 'hub_type', 'icon_hash', 'preferred_locale',
            'max_stage_video_channel_users', 'max_voice_video_channel_users', 'mfa_level',
            'default_message_notifications', 'name', 'nsfw_level', 'owner_id', 'public_updates_channel_id',
            'rules_channel_id', 'safety_alerts_channel_id', 'splash_hash', 'system_channel_id',
            'system_channel_flags', 'vanity_url_code', 'verification_level', 'widget_channel_id', 'widget_enabled',
        },
    )

# ---- afk_channel_id ----

def test__AFK_CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``AFK_CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(AFK_CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(AFK_CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(AFK_CHANNEL_ID_CONVERSION.validator, validate_afk_channel_id)


# ---- afk_timeout ----

def test__AFK_TIMEOUT_CONVERSION__generic():
    """
    Tests whether ``AFK_TIMEOUT_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(AFK_TIMEOUT_CONVERSION.get_converter, )
    # vampytest.assert_is(AFK_TIMEOUT_CONVERSION.put_converter, )
    vampytest.assert_is(AFK_TIMEOUT_CONVERSION.validator, validate_afk_timeout)


def _iter_options__afk_timeout__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, AFK_TIMEOUT_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__afk_timeout__get_converter()).returning_last())
def test__AFK_TIMEOUT_CONVERSION__get_converter(input_value):
    """
    Tests whether `AFK_TIMEOUT_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return AFK_TIMEOUT_CONVERSION.get_converter(input_value)


def _iter_options__afk_timeout__put_converter():
    yield 60, 60
    yield AFK_TIMEOUT_DEFAULT, AFK_TIMEOUT_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__afk_timeout__put_converter()).returning_last())
def test__AFK_TIMEOUT_CONVERSION__put_converter(input_value):
    """
    Tests whether `AFK_TIMEOUT_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return AFK_TIMEOUT_CONVERSION.put_converter(input_value)


# ---- banner ----

def test__BANNER_CONVERSION__generic():
    """
    Tests whether ``BANNER_CONVERSION`` works as intended.
    """
    vampytest.assert_eq(BANNER_CONVERSION.get_converter, Icon.from_base_16_hash)
    vampytest.assert_eq(BANNER_CONVERSION.put_converter, Icon.as_base_16_hash)
    vampytest.assert_eq(BANNER_CONVERSION.validator, GUILD_BANNER.validate_icon)


# ---- boost_progress_bar_enabled ----

def test__BOOST_PROGRESS_BAR_ENABLED_CONVERSION__generic():
    """
    Tests whether ``BOOST_PROGRESS_BAR_ENABLED_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(BOOST_PROGRESS_BAR_ENABLED_CONVERSION.get_converter, )
    # vampytest.assert_is(BOOST_PROGRESS_BAR_ENABLED_CONVERSION.put_converter, )
    vampytest.assert_is(BOOST_PROGRESS_BAR_ENABLED_CONVERSION.validator, validate_boost_progress_bar_enabled)


def _iter_options__boost_progress_bar_enabled__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__boost_progress_bar_enabled__get_converter()).returning_last())
def test__BOOST_PROGRESS_BAR_ENABLED_CONVERSION__get_converter(input_value):
    """
    Tests whether `BOOST_PROGRESS_BAR_ENABLED_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return BOOST_PROGRESS_BAR_ENABLED_CONVERSION.get_converter(input_value)


def _iter_options__boost_progress_bar_enabled__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__boost_progress_bar_enabled__put_converter()).returning_last())
def test__BOOST_PROGRESS_BAR_ENABLED_CONVERSION__put_converter(input_value):
    """
    Tests whether `BOOST_PROGRESS_BAR_ENABLED_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return BOOST_PROGRESS_BAR_ENABLED_CONVERSION.put_converter(input_value)


# ---- content_filter ----

def test__CONTENT_FILTER_CONVERSION__generic():
    """
    Tests whether ``CONTENT_FILTER_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(CONTENT_FILTER_CONVERSION.get_converter, )
    # vampytest.assert_is(CONTENT_FILTER_CONVERSION.put_converter, )
    vampytest.assert_is(CONTENT_FILTER_CONVERSION.validator, validate_content_filter)


def _iter_options__content_filter__get_converter():
    yield None, ContentFilterLevel.disabled
    yield ContentFilterLevel.everyone.value, ContentFilterLevel.everyone


@vampytest._(vampytest.call_from(_iter_options__content_filter__get_converter()).returning_last())
def test__CONTENT_FILTER_CONVERSION__get_converter(input_value):
    """
    Tests whether `CONTENT_FILTER_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``ContentFilterLevel``
    """
    return CONTENT_FILTER_CONVERSION.get_converter(input_value)


def _iter_options__content_filter__put_converter():
    yield ContentFilterLevel.disabled, ContentFilterLevel.disabled.value
    yield ContentFilterLevel.everyone, ContentFilterLevel.everyone.value


@vampytest._(vampytest.call_from(_iter_options__content_filter__put_converter()).returning_last())
def test__CONTENT_FILTER_CONVERSION__put_converter(input_value):
    """
    Tests whether `CONTENT_FILTER_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``ContentFilterLevel``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return CONTENT_FILTER_CONVERSION.put_converter(input_value)


# ---- description ----

def test__DESCRIPTION_CONVERSION__generic():
    """
    Tests whether ``DESCRIPTION_CONVERSION`` works as intended.
    """
    vampytest.assert_is(DESCRIPTION_CONVERSION.get_converter, get_converter_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.put_converter, put_converter_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.validator, validate_description)


# ---- discovery_splash ----

def test__DISCOVERY_SPLASH_CONVERSION__generic():
    """
    Tests whether ``DISCOVERY_SPLASH_CONVERSION`` works as intended.
    """
    vampytest.assert_eq(DISCOVERY_SPLASH_CONVERSION.get_converter, Icon.from_base_16_hash)
    vampytest.assert_eq(DISCOVERY_SPLASH_CONVERSION.put_converter, Icon.as_base_16_hash)
    vampytest.assert_eq(DISCOVERY_SPLASH_CONVERSION.validator, GUILD_DISCOVERY_SPLASH.validate_icon)


# ---- hub_type ----

def test__HUB_TYPE_CONVERSION__generic():
    """
    Tests whether ``HUB_TYPE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(HUB_TYPE_CONVERSION.get_converter, )
    # vampytest.assert_is(HUB_TYPE_CONVERSION.put_converter, )
    vampytest.assert_is(HUB_TYPE_CONVERSION.validator, validate_hub_type)


def _iter_options__hub_type__get_converter():
    yield None, HubType.none
    yield HubType.college.value, HubType.college


@vampytest._(vampytest.call_from(_iter_options__hub_type__get_converter()).returning_last())
def test__HUB_TYPE_CONVERSION__get_converter(input_value):
    """
    Tests whether `HUB_TYPE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``HubType``
    """
    return HUB_TYPE_CONVERSION.get_converter(input_value)


def _iter_options__hub_type__put_converter():
    yield HubType.none, HubType.none.value
    yield HubType.college, HubType.college.value


@vampytest._(vampytest.call_from(_iter_options__hub_type__put_converter()).returning_last())
def test__HUB_TYPE_CONVERSION__put_converter(input_value):
    """
    Tests whether `HUB_TYPE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``HubType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return HUB_TYPE_CONVERSION.put_converter(input_value)


# ---- icon ----

def test__ICON_CONVERSION__generic():
    """
    Tests whether ``ICON_CONVERSION`` works as intended.
    """
    vampytest.assert_eq(ICON_CONVERSION.get_converter, Icon.from_base_16_hash)
    vampytest.assert_eq(ICON_CONVERSION.put_converter, Icon.as_base_16_hash)
    vampytest.assert_eq(ICON_CONVERSION.validator, GUILD_ICON.validate_icon)


# ---- invite_splash ----

def test__INVITE_SPLASH_CONVERSION__generic():
    """
    Tests whether ``INVITE_SPLASH_CONVERSION`` works as intended.
    """
    vampytest.assert_eq(INVITE_SPLASH_CONVERSION.get_converter, Icon.from_base_16_hash)
    vampytest.assert_eq(INVITE_SPLASH_CONVERSION.put_converter, Icon.as_base_16_hash)
    vampytest.assert_eq(INVITE_SPLASH_CONVERSION.validator, GUILD_INVITE_SPLASH.validate_icon)


# ---- locale ----

def test__LOCALE_CONVERSION__generic():
    """
    Tests whether ``LOCALE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(LOCALE_CONVERSION.get_converter, )
    # vampytest.assert_is(LOCALE_CONVERSION.put_converter, )
    vampytest.assert_is(LOCALE_CONVERSION.validator, validate_locale)


def _iter_options__locale__get_converter():
    yield None, LOCALE_DEFAULT
    yield Locale.dutch.value, Locale.dutch


@vampytest._(vampytest.call_from(_iter_options__locale__get_converter()).returning_last())
def test__LOCALE_CONVERSION__get_converter(input_value):
    """
    Tests whether `LOCALE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``Locale``
    """
    return LOCALE_CONVERSION.get_converter(input_value)


def _iter_options__locale__put_converter():
    yield LOCALE_DEFAULT, LOCALE_DEFAULT.value
    yield Locale.dutch, Locale.dutch.value


@vampytest._(vampytest.call_from(_iter_options__locale__put_converter()).returning_last())
def test__LOCALE_CONVERSION__put_converter(input_value):
    """
    Tests whether `LOCALE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``Locale``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return LOCALE_CONVERSION.put_converter(input_value)


# ---- max_stage_channel_video_users ----

def test__MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION__generic():
    """
    Tests whether ``MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.get_converter, )
    # vampytest.assert_is(MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.put_converter, )
    vampytest.assert_is(MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.validator, validate_max_stage_channel_video_users)


def _iter_options__max_stage_channel_video_users__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__max_stage_channel_video_users__get_converter()).returning_last())
def test__MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION__get_converter(input_value):
    """
    Tests whether `MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.get_converter(input_value)


def _iter_options__max_stage_channel_video_users__put_converter():
    yield 60, 60
    yield MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT, MAX_STAGE_CHANNEL_VIDEO_USERS_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__max_stage_channel_video_users__put_converter()).returning_last())
def test__MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION__put_converter(input_value):
    """
    Tests whether `MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return MAX_STAGE_CHANNEL_VIDEO_USERS_CONVERSION.put_converter(input_value)


# ---- max_voice_channel_video_users ----

def test__MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION__generic():
    """
    Tests whether ``MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.get_converter, )
    # vampytest.assert_is(MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.put_converter, )
    vampytest.assert_is(MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.validator, validate_max_voice_channel_video_users)


def _iter_options__max_voice_channel_video_users__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__max_voice_channel_video_users__get_converter()).returning_last())
def test__MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION__get_converter(input_value):
    """
    Tests whether `MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.get_converter(input_value)


def _iter_options__max_voice_channel_video_users__put_converter():
    yield 60, 60
    yield MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT, MAX_VOICE_CHANNEL_VIDEO_USERS_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__max_voice_channel_video_users__put_converter()).returning_last())
def test__MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION__put_converter(input_value):
    """
    Tests whether `MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return MAX_VOICE_CHANNEL_VIDEO_USERS_CONVERSION.put_converter(input_value)


# ---- mfa ----

def test__MFA_CONVERSION__generic():
    """
    Tests whether ``MFA_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(MFA_CONVERSION.get_converter, )
    # vampytest.assert_is(MFA_CONVERSION.put_converter, )
    vampytest.assert_is(MFA_CONVERSION.validator, validate_mfa)


def _iter_options__mfa__get_converter():
    yield None, MFA.none
    yield MFA.elevated.value, MFA.elevated


@vampytest._(vampytest.call_from(_iter_options__mfa__get_converter()).returning_last())
def test__MFA_CONVERSION__get_converter(input_value):
    """
    Tests whether `MFA_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``MFA``
    """
    return MFA_CONVERSION.get_converter(input_value)


def _iter_options__mfa__put_converter():
    yield MFA.none, MFA.none.value
    yield MFA.elevated, MFA.elevated.value


@vampytest._(vampytest.call_from(_iter_options__mfa__put_converter()).returning_last())
def test__MFA_CONVERSION__put_converter(input_value):
    """
    Tests whether `MFA_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``MFA``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return MFA_CONVERSION.put_converter(input_value)


# --- message_notification ----

def test__MESSAGE_NOTIFICATION_CONVERSION__generic():
    """
    Tests whether ``MESSAGE_NOTIFICATION_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(MESSAGE_NOTIFICATION_CONVERSION.get_converter, )
    # vampytest.assert_is(MESSAGE_NOTIFICATION_CONVERSION.put_converter, )
    vampytest.assert_is(MESSAGE_NOTIFICATION_CONVERSION.validator, validate_message_notification)


def _iter_options__message_notification__get_converter():
    yield None, MessageNotificationLevel.all_messages
    yield MessageNotificationLevel.only_mentions.value, MessageNotificationLevel.only_mentions


@vampytest._(vampytest.call_from(_iter_options__message_notification__get_converter()).returning_last())
def test__MESSAGE_NOTIFICATION_CONVERSION__get_converter(input_value):
    """
    Tests whether `MESSAGE_NOTIFICATION_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``MessageNotificationLevel``
    """
    return MESSAGE_NOTIFICATION_CONVERSION.get_converter(input_value)


def _iter_options__message_notification__put_converter():
    yield MessageNotificationLevel.all_messages, MessageNotificationLevel.all_messages.value
    yield MessageNotificationLevel.only_mentions, MessageNotificationLevel.only_mentions.value


@vampytest._(vampytest.call_from(_iter_options__message_notification__put_converter()).returning_last())
def test__MESSAGE_NOTIFICATION_CONVERSION__put_converter(input_value):
    """
    Tests whether `MESSAGE_NOTIFICATION_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``MessageNotificationLevel``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return MESSAGE_NOTIFICATION_CONVERSION.put_converter(input_value)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)


# ---- nsfw_level ----

def test__NSFW_LEVEL_CONVERSION__generic():
    """
    Tests whether ``NSFW_LEVEL_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(NSFW_LEVEL_CONVERSION.get_converter, )
    # vampytest.assert_is(NSFW_LEVEL_CONVERSION.put_converter, )
    vampytest.assert_is(NSFW_LEVEL_CONVERSION.validator, validate_nsfw_level)


def _iter_options__nsfw_level__get_converter():
    yield None, NsfwLevel.none
    yield NsfwLevel.explicit.value, NsfwLevel.explicit


@vampytest._(vampytest.call_from(_iter_options__nsfw_level__get_converter()).returning_last())
def test__NSFW_LEVEL_CONVERSION__get_converter(input_value):
    """
    Tests whether `NSFW_LEVEL_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``NsfwLevel``
    """
    return NSFW_LEVEL_CONVERSION.get_converter(input_value)


def _iter_options__nsfw_level__put_converter():
    yield NsfwLevel.none, NsfwLevel.none.value
    yield NsfwLevel.explicit, NsfwLevel.explicit.value


@vampytest._(vampytest.call_from(_iter_options__nsfw_level__put_converter()).returning_last())
def test__NSFW_LEVEL_CONVERSION__put_converter(input_value):
    """
    Tests whether `NSFW_LEVEL_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``NsfwLevel``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return NSFW_LEVEL_CONVERSION.put_converter(input_value)


# ---- owner_id ----

def test__OWNER_ID_CONVERSION__generic():
    """
    Tests whether ``OWNER_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(OWNER_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(OWNER_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(OWNER_ID_CONVERSION.validator, validate_owner_id)


# ---- public_updates_channel_id ----

def test__PUBLIC_UPDATES_CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``PUBLIC_UPDATES_CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(PUBLIC_UPDATES_CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(PUBLIC_UPDATES_CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(PUBLIC_UPDATES_CHANNEL_ID_CONVERSION.validator, validate_public_updates_channel_id)



# ---- rules_channel_id ----

def test__RULES_CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``RULES_CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(RULES_CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(RULES_CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(RULES_CHANNEL_ID_CONVERSION.validator, validate_rules_channel_id)


# ---- safety_alerts_channel_id ----

def test__SAFETY_ALERTS_CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``SAFETY_ALERTS_CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(SAFETY_ALERTS_CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(SAFETY_ALERTS_CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(SAFETY_ALERTS_CHANNEL_ID_CONVERSION.validator, validate_safety_alerts_channel_id)


# ---- system_channel_id ----

def test__SYSTEM_CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``SYSTEM_CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(SYSTEM_CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(SYSTEM_CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(SYSTEM_CHANNEL_ID_CONVERSION.validator, validate_system_channel_id)


# ---- flags ----

def test__SYSTEM_CHANNEL_FLAGS_CONVERSION__generic():
    """
    Tests whether ``SYSTEM_CHANNEL_FLAGS_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(SYSTEM_CHANNEL_FLAGS_CONVERSION.get_converter, )
    # vampytest.assert_is(SYSTEM_CHANNEL_FLAGS_CONVERSION.put_converter, )
    vampytest.assert_is(SYSTEM_CHANNEL_FLAGS_CONVERSION.validator, validate_system_channel_flags)


def _iter_options__system_channel_flags__get_converter():
    yield 60, SystemChannelFlag(60)
    yield 0, SystemChannelFlag()
    yield None, SystemChannelFlag()


@vampytest._(vampytest.call_from(_iter_options__system_channel_flags__get_converter()).returning_last())
def test__SYSTEM_CHANNEL_FLAGS_CONVERSION__get_converter(input_value):
    """
    Tests whether `SYSTEM_CHANNEL_FLAGS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``SystemChannelFlag``
    """
    output = SYSTEM_CHANNEL_FLAGS_CONVERSION.get_converter(input_value)
    vampytest.assert_instance(output, SystemChannelFlag)
    return output


def _iter_options__system_channel_flag__put_converter():
    yield SystemChannelFlag(60), 60
    yield SystemChannelFlag(), 0


@vampytest._(vampytest.call_from(_iter_options__system_channel_flag__put_converter()).returning_last())
def test__SYSTEM_CHANNEL_FLAGS_CONVERSION__put_converter(input_value):
    """
    Tests whether `SYSTEM_CHANNEL_FLAGS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``SystemChannelFlag``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = SYSTEM_CHANNEL_FLAGS_CONVERSION.put_converter(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- vanity_code ----

def test__VANITY_CODE_CONVERSION__generic():
    """
    Tests whether ``VANITY_CODE_CONVERSION`` works as intended.
    """
    vampytest.assert_is(VANITY_CODE_CONVERSION.get_converter, get_converter_description)
    vampytest.assert_is(VANITY_CODE_CONVERSION.put_converter, put_converter_description)
    vampytest.assert_is(VANITY_CODE_CONVERSION.validator, validate_vanity_code)


# ---- verification_level ----

def test__VERIFICATION_LEVEL_CONVERSION__generic():
    """
    Tests whether ``VERIFICATION_LEVEL_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(VERIFICATION_LEVEL_CONVERSION.get_converter, )
    # vampytest.assert_is(VERIFICATION_LEVEL_CONVERSION.put_converter, )
    vampytest.assert_is(VERIFICATION_LEVEL_CONVERSION.validator, validate_verification_level)


def _iter_options__verification_level__get_converter():
    yield None, VerificationLevel.none
    yield VerificationLevel.low.value, VerificationLevel.low


@vampytest._(vampytest.call_from(_iter_options__verification_level__get_converter()).returning_last())
def test__VERIFICATION_LEVEL_CONVERSION__get_converter(input_value):
    """
    Tests whether `VERIFICATION_LEVEL_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``VerificationLevel``
    """
    return VERIFICATION_LEVEL_CONVERSION.get_converter(input_value)


def _iter_options__verification_level__put_converter():
    yield VerificationLevel.none, VerificationLevel.none.value
    yield VerificationLevel.low, VerificationLevel.low.value


@vampytest._(vampytest.call_from(_iter_options__verification_level__put_converter()).returning_last())
def test__VERIFICATION_LEVEL_CONVERSION__put_converter(input_value):
    """
    Tests whether `VERIFICATION_LEVEL_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``VerificationLevel``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return VERIFICATION_LEVEL_CONVERSION.put_converter(input_value)


# ---- widget_channel_id ----

def test__WIDGET_CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``WIDGET_CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(WIDGET_CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(WIDGET_CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(WIDGET_CHANNEL_ID_CONVERSION.validator, validate_widget_channel_id)


# ---- widget_enabled ----

def test__WIDGET_ENABLED_CONVERSION__generic():
    """
    Tests whether ``WIDGET_ENABLED_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(WIDGET_ENABLED_CONVERSION.get_converter, )
    # vampytest.assert_is(WIDGET_ENABLED_CONVERSION.put_converter, )
    vampytest.assert_is(WIDGET_ENABLED_CONVERSION.validator, validate_widget_enabled)


def _iter_options__widget_enabled__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__widget_enabled__get_converter()).returning_last())
def test__WIDGET_ENABLED_CONVERSION__get_converter(input_value):
    """
    Tests whether `WIDGET_ENABLED_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return WIDGET_ENABLED_CONVERSION.get_converter(input_value)


def _iter_options__widget_enabled__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__widget_enabled__put_converter()).returning_last())
def test__WIDGET_ENABLED_CONVERSION__put_converter(input_value):
    """
    Tests whether `WIDGET_ENABLED_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return WIDGET_ENABLED_CONVERSION.put_converter(input_value)
