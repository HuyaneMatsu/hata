import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....scheduled_event import PrivacyLevel

from ...guild import GuildFeature
from ...guild_activity_overview_activity import GuildActivityOverviewActivity, GuildActivityOverviewActivityLevel
from ...guild_activity_overview_tag import GuildActivityOverviewTag

from ..guild_activity_overview import GuildActivityOverview


def test__GuildActivityOverview__repr():
    """
    Tests whether ``GuildActivityOverview.__repr__`` works as intended.
    """
    guild_id = 202504260040
    
    activities = {
        202504260041 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 1022,
        ),
        202504260042 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 100,
        ),
    }
    activity_application_ids = [
        202504260041,
        202504260042,
    ]
    approximate_online_count = 23
    approximate_user_count = 123
    badge = 6
    badge_color_primary = Color.from_rgb(2, 3, 45)
    badge_color_secondary = Color.from_rgb(56, 13, 78)
    badge_icon = Icon(IconType.static, 13233)
    badge_tag = 'orin'
    banner_color = Color.from_rgb(255, 12, 33)
    boost_count = 6
    boost_level = 2
    description = 'Rot in hell'
    discovery_splash = Icon(IconType.static, 3)
    features = [GuildFeature.banner, GuildFeature.commerce]
    icon = Icon(IconType.static, 2)
    name = '!!'
    privacy_level = PrivacyLevel.public
    tags = [
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['heart'], title = 'collecting'),
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['custard'], title = 'pudding'),
    ]
    
    guild_activity_overview = GuildActivityOverview.precreate(
        guild_id,
        activities = activities,
        activity_application_ids = activity_application_ids,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
        badge = badge,
        badge_color_primary = badge_color_primary,
        badge_color_secondary = badge_color_secondary,
        badge_icon = badge_icon,
        badge_tag = badge_tag,
        banner_color = banner_color,
        boost_count = boost_count,
        boost_level = boost_level,
        description = description,
        discovery_splash = discovery_splash,
        features = features,
        icon = icon,
        name = name,
        privacy_level = privacy_level,
        tags = tags,
    )
    
    output = repr(guild_activity_overview)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(guild_activity_overview).__name__, output)
    vampytest.assert_in(f'id = {guild_id}', output)
    vampytest.assert_in(f'activity_application_ids = {tuple(activity_application_ids)!r}', output)
    vampytest.assert_in(f'approximate_online_count = {approximate_online_count!r}', output)
    vampytest.assert_in(f'approximate_user_count = {approximate_user_count!r}', output)
    vampytest.assert_in(f'badge = {badge!r}', output)
    vampytest.assert_in(f'badge_color_primary = {badge_color_primary!r}', output)
    vampytest.assert_in(f'badge_color_secondary = {badge_color_secondary!r}', output)
    vampytest.assert_in(f'badge_icon = {badge_icon!r}', output)
    vampytest.assert_in(f'banner_color = {banner_color!r}', output)
    vampytest.assert_in(f'boost_count = {boost_count!r}', output)
    vampytest.assert_in(f'boost_level = {boost_level!r}', output)
    vampytest.assert_in(f'description = {description!r}', output)
    vampytest.assert_in(f'discovery_splash = {discovery_splash!r}', output)
    vampytest.assert_in(f'features = {tuple(features)!r}', output)
    vampytest.assert_in(f'icon = {icon!r}', output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'privacy_level = {privacy_level.name!s} ~ {privacy_level.value!r}', output)
    vampytest.assert_in(f'tags = {tuple(tags)!r}', output)


def _iter_options__eq():
    guild_id = 202504260050
    
    activities = {
        202504260051 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 1022,
        ),
        202504260052 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 100,
        ),
    }
    activity_application_ids = [
        202504260051,
        202504260052,
    ]
    approximate_online_count = 23
    approximate_user_count = 123
    badge = 6
    badge_color_primary = Color.from_rgb(2, 3, 45)
    badge_color_secondary = Color.from_rgb(56, 13, 78)
    badge_icon = Icon(IconType.static, 13233)
    badge_tag = 'orin'
    banner_color = Color.from_rgb(255, 12, 33)
    boost_count = 6
    boost_level = 2
    description = 'Rot in hell'
    discovery_splash = Icon(IconType.static, 3)
    features = [GuildFeature.banner, GuildFeature.commerce]
    icon = Icon(IconType.static, 2)
    name = '!!'
    privacy_level = PrivacyLevel.public
    tags = [
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['heart'], title = 'collecting'),
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['custard'], title = 'pudding'),
    ]
    
    keyword_parameters = {
        'guild_id': guild_id,
        'activities': activities,
        'activity_application_ids': activity_application_ids,
        'approximate_online_count': approximate_online_count,
        'approximate_user_count': approximate_user_count,
        'badge': badge,
        'badge_color_primary': badge_color_primary,
        'badge_color_secondary': badge_color_secondary,
        'badge_icon': badge_icon,
        'badge_tag': badge_tag,
        'banner_color': banner_color,
        'boost_count': boost_count,
        'boost_level': boost_level,
        'description': description,
        'discovery_splash': discovery_splash,
        'features': features,
        'icon': icon,
        'name': name,
        'privacy_level': privacy_level,
        'tags': tags,
    }
    
    yield (
        'true',
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        'false > guild_id',
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 202504260053,
        },
        False,
    )
    
    yield (
        'false > activities',
        keyword_parameters,
        {
            **keyword_parameters,
            'activities': None,
        },
        False,
    )
    
    yield (
        'false > activity_application_ids',
        keyword_parameters,
        {
            **keyword_parameters,
            'activity_application_ids': None,
        },
        False,
    )
    
    yield (
        'false > approximate_online_count',
        keyword_parameters,
        {
            **keyword_parameters,
            'approximate_online_count': 0,
        },
        False,
    )
    
    yield (
        'false > approximate_user_count',
        keyword_parameters,
        {
            **keyword_parameters,
            'approximate_user_count': 0,
        },
        False,
    )
    
    yield (
        'false > badge',
        keyword_parameters,
        {
            **keyword_parameters,
            'badge': 0,
        },
        False,
    )
    
    yield (
        'false > badge_color_primary',
        keyword_parameters,
        {
            **keyword_parameters,
            'badge_color_primary': None,
        },
        False,
    )
    
    yield (
        'false > badge_color_secondary',
        keyword_parameters,
        {
            **keyword_parameters,
            'badge_color_secondary': None,
        },
        False,
    )
    
    yield (
        'false > badge_icon',
        keyword_parameters,
        {
            **keyword_parameters,
            'badge_icon': None,
        },
        False,
    )
    
    yield (
        'false > badge_tag',
        keyword_parameters,
        {
            **keyword_parameters,
            'badge_tag': '',
        },
        False,
    )
    
    yield (
        'false > banner_color',
        keyword_parameters,
        {
            **keyword_parameters,
            'banner_color': None,
        },
        False,
    )
    
    yield (
        'false > boost_count',
        keyword_parameters,
        {
            **keyword_parameters,
            'boost_count': 0,
        },
        False,
    )
    
    yield (
        'false > boost_level',
        keyword_parameters,
        {
            **keyword_parameters,
            'boost_level': 0,
        },
        False,
    )
    
    yield (
        'false > description',
        keyword_parameters,
        {
            **keyword_parameters,
            'description': None,
        },
        False,
    )
    
    yield (
        'false > discovery_splash',
        keyword_parameters,
        {
            **keyword_parameters,
            'discovery_splash': None,
        },
        False,
    )
    
    yield (
        'false > features',
        keyword_parameters,
        {
            **keyword_parameters,
            'features': None,
        },
        False,
    )
    
    yield (
        'false > icon',
        keyword_parameters,
        {
            **keyword_parameters,
            'icon': None,
        },
        False,
    )
    
    yield (
        'false > name',
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Orin\'s dance house',
        },
        False,
    )
    
    yield (
        'false > privacy_level',
        keyword_parameters,
        {
            **keyword_parameters,
            'privacy_level': PrivacyLevel.none,
        },
        False,
    )
    
    yield (
        'false > tags',
        keyword_parameters,
        {
            **keyword_parameters,
            'tags': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).named_first().returning_last())
def test__GuildActivityOverview__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``GuildActivityOverview.__eq__`` works as intended.
    
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
    guild_activity_overview_0 = GuildActivityOverview.precreate(**keyword_parameters_0)
    guild_activity_overview_1 = GuildActivityOverview.precreate(**keyword_parameters_1)
    
    output = guild_activity_overview_0 == guild_activity_overview_1
    vampytest.assert_instance(output, bool)
    return output


def test__GuildActivityOverview__hash():
    """
    Tests whether ``GuildActivityOverview.__hash__`` works as intended.
    """
    guild_id = 202504260060
    
    activities = {
        202504260061 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 1022,
        ),
        202504260062 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 100,
        ),
    }
    activity_application_ids = [
        202504260061,
        202504260062,
    ]
    approximate_online_count = 23
    approximate_user_count = 123
    badge = 6
    badge_color_primary = Color.from_rgb(2, 3, 45)
    badge_color_secondary = Color.from_rgb(56, 13, 78)
    badge_icon = Icon(IconType.static, 13233)
    badge_tag = 'orin'
    banner_color = Color.from_rgb(255, 12, 33)
    boost_count = 6
    boost_level = 2
    description = 'Rot in hell'
    discovery_splash = Icon(IconType.static, 3)
    features = [GuildFeature.banner, GuildFeature.commerce]
    icon = Icon(IconType.static, 2)
    name = '!!'
    privacy_level = PrivacyLevel.public
    tags = [
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['heart'], title = 'collecting'),
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['custard'], title = 'pudding'),
    ]
    
    guild_activity_overview = GuildActivityOverview.precreate(
        guild_id,
        activities = activities,
        activity_application_ids = activity_application_ids,
        approximate_online_count = approximate_online_count,
        approximate_user_count = approximate_user_count,
        badge = badge,
        badge_color_primary = badge_color_primary,
        badge_color_secondary = badge_color_secondary,
        badge_icon = badge_icon,
        badge_tag = badge_tag,
        banner_color = banner_color,
        boost_count = boost_count,
        boost_level = boost_level,
        description = description,
        discovery_splash = discovery_splash,
        features = features,
        icon = icon,
        name = name,
        privacy_level = privacy_level,
        tags = tags,
    )
    
    output = hash(guild_activity_overview)
    vampytest.assert_instance(output, int)
