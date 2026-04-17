import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....scheduled_event import PrivacyLevel

from ...guild import GuildFeature
from ...guild_activity_overview_activity import GuildActivityOverviewActivity, GuildActivityOverviewActivityLevel
from ...guild_activity_overview_tag import GuildActivityOverviewTag

from ..guild_activity_overview import GuildActivityOverview


def _assert_fields_set(guild_activity_overview):
    """
    Asserts whether every fields of the given
    
    Parameters
    ----------
    guild_activity_overview : ``GuildActivityOverview``
        Instance to check.
    """
    vampytest.assert_instance(guild_activity_overview, GuildActivityOverview)
    vampytest.assert_instance(guild_activity_overview.activities, dict, nullable = True)
    vampytest.assert_instance(guild_activity_overview.activity_application_ids, tuple, nullable = True)
    vampytest.assert_instance(guild_activity_overview.approximate_online_count, int)
    vampytest.assert_instance(guild_activity_overview.approximate_user_count, int)
    vampytest.assert_instance(guild_activity_overview.badge, int)
    vampytest.assert_instance(guild_activity_overview.badge_color_primary, Color, nullable = True)
    vampytest.assert_instance(guild_activity_overview.badge_color_secondary, Color, nullable = True)
    vampytest.assert_instance(guild_activity_overview.badge_icon, Icon)
    vampytest.assert_instance(guild_activity_overview.badge_tag, str)
    vampytest.assert_instance(guild_activity_overview.banner_color, Color, nullable = True)
    vampytest.assert_instance(guild_activity_overview.boost_count, int)
    vampytest.assert_instance(guild_activity_overview.boost_level, int)
    vampytest.assert_instance(guild_activity_overview.description, str, nullable = True)
    vampytest.assert_instance(guild_activity_overview.discovery_splash, Icon)
    vampytest.assert_instance(guild_activity_overview.features, tuple, nullable = True)
    vampytest.assert_instance(guild_activity_overview.icon, Icon)
    vampytest.assert_instance(guild_activity_overview.id, int)
    vampytest.assert_instance(guild_activity_overview.name, str)
    vampytest.assert_instance(guild_activity_overview.privacy_level, PrivacyLevel)
    vampytest.assert_instance(guild_activity_overview.tags, tuple, nullable = True)


def test__GuildActivityOverview__new__no_fields():
    """
    Tests whether ``GuildActivityOverview.__new__`` works as intended.
    
    Case: no fields given.
    """
    guild_activity_overview = GuildActivityOverview()
    _assert_fields_set(guild_activity_overview)


def test__GuildActivityOverview__new__all_fields():
    """
    Tests whether ``GuildActivityOverview.__new__`` works as intended.
    
    Case: all fields given.
    """
    activity_application_ids = [
        202504260000,
        202504260001,
    ]
    banner_color = Color.from_rgb(255, 12, 33)
    description = 'Rot in hell'
    discovery_splash = Icon(IconType.static, 3)
    icon = Icon(IconType.static, 2)
    name = '!!'
    privacy_level = PrivacyLevel.public
    tags = [
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['heart'], title = 'collecting'),
        GuildActivityOverviewTag(emoji = BUILTIN_EMOJIS['custard'], title = 'pudding'),
    ]
    
    guild_activity_overview = GuildActivityOverview(
        activity_application_ids = activity_application_ids,
        banner_color = banner_color,
        description = description,
        discovery_splash = discovery_splash,
        icon = icon,
        privacy_level = privacy_level,
        name = name,
        tags = tags,
    )
    _assert_fields_set(guild_activity_overview)
    
    vampytest.assert_eq(guild_activity_overview.activity_application_ids, tuple(activity_application_ids))
    vampytest.assert_eq(guild_activity_overview.banner_color, banner_color)
    vampytest.assert_eq(guild_activity_overview.description, description)
    vampytest.assert_eq(guild_activity_overview.discovery_splash, discovery_splash)
    vampytest.assert_eq(guild_activity_overview.icon, icon)
    vampytest.assert_eq(guild_activity_overview.name, name)
    vampytest.assert_eq(guild_activity_overview.tags, tuple(tags))
    vampytest.assert_is(guild_activity_overview.privacy_level, privacy_level)


def test__GuildActivityOverview__create_empty():
    """
    Tests whether ``GuildActivityOverview._create_empty`` works as intended.
    """
    guild_id = 202504260002
    
    guild_activity_overview = GuildActivityOverview._create_empty(guild_id)
    _assert_fields_set(guild_activity_overview)
    
    vampytest.assert_eq(guild_activity_overview.id, guild_id)


def test__GuildActivityOverview__precreate__all_fields():
    """
    Tests whether ``GuildActivityOverview.precreate`` works as intended.
    
    Case: all fields given.
    """
    guild_id = 202504260003
    
    activities = {
        202504260004 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 1022,
        ),
        202504260005 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 100,
        ),
    }
    activity_application_ids = [
        202504260004,
        202504260005,
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
    _assert_fields_set(guild_activity_overview)
    
    vampytest.assert_eq(guild_activity_overview.id, guild_id)
    vampytest.assert_eq(guild_activity_overview.activities, activities)
    vampytest.assert_eq(guild_activity_overview.activity_application_ids, tuple(activity_application_ids))
    vampytest.assert_eq(guild_activity_overview.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(guild_activity_overview.approximate_user_count, approximate_user_count)
    vampytest.assert_eq(guild_activity_overview.badge, badge)
    vampytest.assert_eq(guild_activity_overview.badge_color_primary, badge_color_primary)
    vampytest.assert_eq(guild_activity_overview.badge_color_secondary, badge_color_secondary)
    vampytest.assert_eq(guild_activity_overview.badge_icon, badge_icon)
    vampytest.assert_eq(guild_activity_overview.badge_tag, badge_tag)
    vampytest.assert_eq(guild_activity_overview.banner_color, banner_color)
    vampytest.assert_eq(guild_activity_overview.boost_count, boost_count)
    vampytest.assert_eq(guild_activity_overview.boost_level, boost_level)
    vampytest.assert_eq(guild_activity_overview.description, description)
    vampytest.assert_eq(guild_activity_overview.discovery_splash, discovery_splash)
    vampytest.assert_eq(guild_activity_overview.features, tuple(features))
    vampytest.assert_eq(guild_activity_overview.icon, icon)
    vampytest.assert_eq(guild_activity_overview.name, name)
    vampytest.assert_is(guild_activity_overview.privacy_level, privacy_level)
    vampytest.assert_eq(guild_activity_overview.tags, tuple(tags))
