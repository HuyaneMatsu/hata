import vampytest

from ..guild_activity_overview_activity import GuildActivityOverviewActivity
from ..preinstanced import GuildActivityOverviewActivityLevel

from .test__guild_activity_overview_activity__constructor import _assert_fields_set


def test__GuildActivityOverviewActivity__from_data():
    """
    Tests whether ``GuildActivityOverviewActivity.from_data`` works as intended.
    """
    level = GuildActivityOverviewActivityLevel.recently_popular
    score = 1352
    
    data = {
        'activity_level': level.value,
        'activity_score': score,
    }
    
    guild_activity_overview_activity = GuildActivityOverviewActivity.from_data(data)
    _assert_fields_set(guild_activity_overview_activity)
    
    vampytest.assert_is(guild_activity_overview_activity.level, level)
    vampytest.assert_eq(guild_activity_overview_activity.score, score)


def test__GuildActivityOverviewActivity__to_data():
    """
    Tests whether ``GuildActivityOverviewActivity.to_data`` works as intended.
    
    Case: include defaults.
    """
    level = GuildActivityOverviewActivityLevel.recently_popular
    score = 1352
    
    expected_output = {
        'activity_level': level.value,
        'activity_score': score,
    }
    
    guild_activity_overview_activity = GuildActivityOverviewActivity(level = level, score = score)
    
    vampytest.assert_eq(
        guild_activity_overview_activity.to_data(defaults = True),
        expected_output,
    )
