import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....scheduled_event import PrivacyLevel

from ...guild import GuildFeature
from ...guild_activity_overview_activity import GuildActivityOverviewActivity, GuildActivityOverviewActivityLevel
from ...guild_activity_overview_tag import GuildActivityOverviewTag

from ..guild_activity_overview import GuildActivityOverview

from .test__GuildActivityOverview__construct import _assert_fields_set


def test__GuildActivityOverview__from_data():
    """
    Tests whether ``GuildActivityOverview.from_data`` works as intended.
    """
    guild_id = 202504260020
    
    activities = {
        202504260021 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 1022,
        ),
        202504260022 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 100,
        ),
    }
    activity_application_ids = [
        202504260021,
        202504260022,
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
    
    data = {
        'game_activity': {
            str(application_id): guild_activity_overview_activity.to_data()
            for application_id, guild_activity_overview_activity in activities.items()
        },
        'game_application_ids': [str(application_id) for application_id in activity_application_ids],
        'online_count': approximate_online_count,
        'member_count': approximate_user_count,
        'badge': badge,
        'badge_color_primary': badge_color_primary.as_html,
        'badge_color_secondary': badge_color_secondary.as_html,
        'tag': badge_tag,
        'brand_color_primary': banner_color.as_html,
        'premium_subscription_count': boost_count,
        'premium_tier': boost_level,
        'description': description,
        'features': [feature.value for feature in features],
        'id': str(guild_id),
        'name': name,
        'visibility': privacy_level.value,
        'traits': [{**tag.to_data(), 'position': index} for index, tag in enumerate(tags)],
        
        'badge_hash': badge_icon.as_base_16_hash,
        'custom_banner_hash': discovery_splash.as_base_16_hash,
        'icon': icon.as_base_16_hash,
    }
    
    guild_activity_overview = GuildActivityOverview.from_data(data)
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


def test__GuildActivityOverview__to_data():
    """
    Tests whether ``GuildActivityOverview.to_data`` works as intended.
    
    Case: include internals and defaults.
    """
    guild_id = 202504260030
    
    activities = {
        202504260031 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 1022,
        ),
        202504260032 : GuildActivityOverviewActivity(
            level = GuildActivityOverviewActivityLevel.recently_popular,
            score = 100,
        ),
    }
    activity_application_ids = [
        202504260031,
        202504260032,
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
    
    expected_output = {
        'game_activity': {
            str(application_id): guild_activity_overview_activity.to_data(defaults = True)
            for application_id, guild_activity_overview_activity in activities.items()
        },
        'game_application_ids': [str(application_id) for application_id in activity_application_ids],
        'online_count': approximate_online_count,
        'member_count': approximate_user_count,
        'badge': badge,
        'badge_color_primary': badge_color_primary.as_html,
        'badge_color_secondary': badge_color_secondary.as_html,
        'tag': badge_tag,
        'brand_color_primary': banner_color.as_html,
        'premium_subscription_count': boost_count,
        'premium_tier': boost_level,
        'description': description,
        'features': [feature.value for feature in features],
        'id': str(guild_id),
        'name': name,
        'visibility': privacy_level.value,
        'traits': [{**tag.to_data(defaults = True), 'position': index} for index, tag in enumerate(tags)],
        
        'badge_hash': badge_icon.as_base_16_hash,
        'custom_banner_hash': discovery_splash.as_base_16_hash,
        'icon': icon.as_base_16_hash,
    }
    
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
    
    vampytest.assert_eq(
        guild_activity_overview.to_data(defaults = True, include_internals = True),
        expected_output,
    )
