import vampytest

from ....bases import Icon, IconType
from ....localization import Locale

from ..flags import SystemChannelFlag
from ..guild import Guild
from ..preinstanced import (
    ContentFilterLevel, GuildFeature, HubType, MFA, MessageNotificationLevel, NsfwLevel, VerificationLevel
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


def test__Guild__eq():
    """
    Tests whether ``Guild.__eq__`` works as intended.
    """
    guild_id = 202306220142
    
    afk_channel_id = 202306220134
    afk_timeout = 1800
    banner = Icon(IconType.animated, 12)
    boost_progress_bar_enabled = True
    content_filter = ContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    hub_type = HubType.college
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    message_notification = MessageNotificationLevel.no_messages
    mfa = MFA.elevated
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    owner_id = 202306220135
    preferred_locale = Locale.finnish
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
        'content_filter': content_filter,
        'description': description,
        'discovery_splash': discovery_splash,
        'features': features,
        'hub_type': hub_type,
        'icon': icon,
        'invite_splash': invite_splash,
        'message_notification': message_notification,
        'mfa': mfa,
        'name': name,
        'nsfw_level': nsfw_level,
        'owner_id': owner_id,
        'preferred_locale': preferred_locale,
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
    vampytest.assert_eq(guild, guild)
    vampytest.assert_ne(guild, object())
    
    test_guild = Guild(**keyword_parameters)
    vampytest.assert_eq(guild, test_guild)
    
    for field_name, field_value in (
        ('afk_channel_id', 202306220143),
        ('afk_timeout', 60),
        ('banner', Icon(IconType.animated, 112)),
        ('boost_progress_bar_enabled', False),
        ('content_filter', ContentFilterLevel.everyone),
        ('description', 'Orin'),
        ('discovery_splash', Icon(IconType.animated, 114)),
        ('features', [GuildFeature.animated_banner]),
        ('hub_type', HubType.high_school),
        ('icon', Icon(IconType.animated, 116)),
        ('invite_splash', Icon(IconType.animated, 118)),
        ('message_notification', MessageNotificationLevel.only_mentions),
        ('mfa', MFA.none),
        ('name', 'Okuu'),
        ('nsfw_level', NsfwLevel.safe),
        ('owner_id', 202306220144),
        ('preferred_locale', Locale.dutch),
        ('public_updates_channel_id', 202306220145),
        ('rules_channel_id', 202306220146),
        ('safety_alerts_channel_id', 202306220147),
        ('system_channel_id', 202306220148),
        ('system_channel_flags', SystemChannelFlag(11)),
        ('vanity_code', 'Satori'),
        ('verification_level', VerificationLevel.high),
        ('widget_channel_id', 202306220149),
        ('widget_enabled', False),
    ):
        test_guild = Guild(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(guild, test_guild)


def test__Guild__hash():
    """
    Tests whether ``Guild.__hash__`` works as intended.
    """
    guild_id = 202306220150
    
    afk_channel_id = 202306220151
    afk_timeout = 1800
    banner = Icon(IconType.animated, 12)
    boost_progress_bar_enabled = True
    content_filter = ContentFilterLevel.no_role
    description = 'Koishi'
    discovery_splash = Icon(IconType.animated, 14)
    features = [GuildFeature.animated_icon]
    hub_type = HubType.college
    icon = Icon(IconType.animated, 16)
    invite_splash = Icon(IconType.animated, 18)
    message_notification = MessageNotificationLevel.no_messages
    mfa = MFA.elevated
    name = 'Komeiji'
    nsfw_level = NsfwLevel.explicit
    owner_id = 202306220152
    preferred_locale = Locale.finnish
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
        'content_filter': content_filter,
        'description': description,
        'discovery_splash': discovery_splash,
        'features': features,
        'hub_type': hub_type,
        'icon': icon,
        'invite_splash': invite_splash,
        'message_notification': message_notification,
        'mfa': mfa,
        'name': name,
        'nsfw_level': nsfw_level,
        'owner_id': owner_id,
        'preferred_locale': preferred_locale,
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
