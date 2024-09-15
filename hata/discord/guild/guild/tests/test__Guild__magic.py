import vampytest

from ....bases import Icon, IconType
from ....localization import Locale

from ..flags import SystemChannelFlag
from ..guild import Guild
from ..preinstanced import (
    ExplicitContentFilterLevel, GuildFeature, HubType, MfaLevel, MessageNotificationLevel, NsfwLevel, VerificationLevel
)


def test__Guild__repr():
    """
    Tests whether ``Guild.__repr__`` works as intended.
    """
    guild_id = 202306220131
    name = 'Orin'
    
    guild = Guild.precreate(guild_id, name = name)
    
    vampytest.assert_instance(repr(guild), str)


@vampytest.call_with('')
@vampytest.call_with('c')
def test__Guild__format__passing(code):
    """
    Tests whether ``Guild.__format__`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    code : `str`
        Format code to format with.
    """
    guild_id = 202306220132
    name = 'Orin'
    
    guild = Guild.precreate(guild_id, name = name)
    
    vampytest.assert_instance(format(guild, code), str)


@vampytest.raising(ValueError)
@vampytest.call_with('d')
@vampytest.call_with('c_')
def test__Guild__format__wrong_code(code):
    """
    Tests whether ``Guild.__format__`` works as intended.
    
    Case: Failing.
    
    Parameters
    ----------
    code : `str`
        Format code to format with.
    """
    guild_id = 202306220133
    name = 'Orin'
    
    guild = Guild.precreate(guild_id, name = name)
    
    return format(guild, code)


def _iter_options__eq():
    
    afk_channel_id = 202306220134
    afk_timeout = 1800
    banner = Icon(IconType.animated, 12)
    boost_progress_bar_enabled = True
    explicit_content_filter_level = ExplicitContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    hub_type = HubType.college
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    default_message_notification_level = MessageNotificationLevel.no_messages
    mfa_level = MfaLevel.elevated
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    owner_id = 202306220135
    locale = Locale.finnish
    public_updates_channel_id = 202306220136
    rules_channel_id = 202306220137
    safety_alerts_channel_id = 202306220139
    system_channel_id = 202306220140
    system_channel_flags = SystemChannelFlag(12)
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    widget_channel_id = 202306220141
    widget_enabled = True
    
    keyword_parameters = {
        'afk_channel_id': afk_channel_id,
        'afk_timeout': afk_timeout,
        'banner': banner,
        'boost_progress_bar_enabled': boost_progress_bar_enabled,
        'explicit_content_filter_level': explicit_content_filter_level,
        'description': description,
        'discovery_splash': discovery_splash,
        'features': features,
        'hub_type': hub_type,
        'icon': icon,
        'invite_splash': invite_splash,
        'default_message_notification_level': default_message_notification_level,
        'mfa_level': mfa_level,
        'name': name,
        'nsfw_level': nsfw_level,
        'owner_id': owner_id,
        'locale': locale,
        'public_updates_channel_id': public_updates_channel_id,
        'rules_channel_id': rules_channel_id,
        'safety_alerts_channel_id': safety_alerts_channel_id,
        'system_channel_id': system_channel_id,
        'system_channel_flags': system_channel_flags,
        'vanity_code': vanity_code,
        'verification_level': verification_level,
        'widget_channel_id': widget_channel_id,
        'widget_enabled': widget_enabled,
    }
    
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'afk_channel_id': 202306220143,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'afk_timeout': 60,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'banner': Icon(IconType.animated, 112),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'boost_progress_bar_enabled': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'explicit_content_filter_level': ExplicitContentFilterLevel.everyone,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'Orin',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'discovery_splash': Icon(IconType.animated, 114),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'features': [GuildFeature.animated_banner],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'hub_type': HubType.high_school,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'icon': Icon(IconType.animated, 116),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'invite_splash': Icon(IconType.animated, 118),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'default_message_notification_level': MessageNotificationLevel.only_mentions,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mfa_level': MfaLevel.none,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Okuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'nsfw_level': NsfwLevel.safe,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'owner_id': 202306220144,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'locale': Locale.dutch,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'public_updates_channel_id': 202306220145,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'rules_channel_id': 202306220146,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'safety_alerts_channel_id': 202306220147,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'system_channel_id': 202306220148,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'system_channel_flags': SystemChannelFlag(11),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'vanity_code': 'Satori',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'verification_level': VerificationLevel.high,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'widget_channel_id': 202306220149,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'widget_enabled': False,
        },
        False,
    )



@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Guild__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Guild.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    guild_0 = Guild(**keyword_parameters_0)
    guild_1 = Guild(**keyword_parameters_1)
    
    output = guild_0 == guild_1
    vampytest.assert_instance(output, bool)
    return output


def test__Guild__eq__has_id():
    """
    Tests whether ``Guild.__eq__`` works as intended.
    
    Case: has id.
    """
    guild_id_0 = 202409040011
    guild_id_1 = 202409040012
    
    name_0 = 'hey mister'
    name_1 = 'water heater for sale'
    
    guild_0 = Guild.precreate(guild_id_0, name = name_0)
    guild_1 = Guild.precreate(guild_id_1, name = name_1)
    guild_2 = Guild(name = name_0)
    
    vampytest.assert_eq(guild_0, guild_0)
    vampytest.assert_ne(guild_0, guild_1)
    vampytest.assert_eq(guild_0, guild_2)
    vampytest.assert_ne(guild_1, guild_2)


def test__Guild__hash():
    """
    Tests whether ``Guild.__hash__`` works as intended.
    """
    guild_id = 202306220150
    
    afk_channel_id = 202306220151
    afk_timeout = 1800
    banner = Icon(IconType.animated, 12)
    boost_progress_bar_enabled = True
    explicit_content_filter_level = ExplicitContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    hub_type = HubType.college
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    default_message_notification_level = MessageNotificationLevel.no_messages
    mfa_level = MfaLevel.elevated
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    owner_id = 202306220152
    locale = Locale.finnish
    public_updates_channel_id = 202306220153
    rules_channel_id = 202306220154
    safety_alerts_channel_id = 202306220155
    system_channel_id = 202306220156
    system_channel_flags = SystemChannelFlag(12)
    vanity_code = 'koi'
    verification_level = VerificationLevel.medium
    widget_channel_id = 202306220157
    widget_enabled = True
    
    keyword_parameters = {
        'afk_channel_id': afk_channel_id,
        'afk_timeout': afk_timeout,
        'banner': banner,
        'boost_progress_bar_enabled': boost_progress_bar_enabled,
        'explicit_content_filter_level': explicit_content_filter_level,
        'description': description,
        'discovery_splash': discovery_splash,
        'features': features,
        'hub_type': hub_type,
        'icon': icon,
        'invite_splash': invite_splash,
        'default_message_notification_level': default_message_notification_level,
        'mfa_level': mfa_level,
        'name': name,
        'nsfw_level': nsfw_level,
        'owner_id': owner_id,
        'locale': locale,
        'public_updates_channel_id': public_updates_channel_id,
        'rules_channel_id': rules_channel_id,
        'safety_alerts_channel_id': safety_alerts_channel_id,
        'system_channel_id': system_channel_id,
        'system_channel_flags': system_channel_flags,
        'vanity_code': vanity_code,
        'verification_level': verification_level,
        'widget_channel_id': widget_channel_id,
        'widget_enabled': widget_enabled,
    }
    
    guild = Guild.precreate(guild_id, **keyword_parameters)
    vampytest.assert_instance(hash(guild), int)

    guild = Guild(**keyword_parameters)
    vampytest.assert_instance(hash(guild), int)
