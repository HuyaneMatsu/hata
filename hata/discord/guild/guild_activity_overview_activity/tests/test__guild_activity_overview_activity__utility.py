import vampytest

from ..guild_activity_overview_activity import GuildActivityOverviewActivity
from ..preinstanced import GuildActivityOverviewActivityLevel

from .test__guild_activity_overview_activity__constructor import _assert_fields_set


def test__GuildActivityOverviewActivity__copy():
    """
    Tests whether ``GuildActivityOverviewActivity.copy`` works as intended.
    """
    level = GuildActivityOverviewActivityLevel.recently_popular
    score = 1352
    
    guild_activity_overview_activity = GuildActivityOverviewActivity(level = level, score = score)
    
    copy = guild_activity_overview_activity.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_activity_overview_activity)
    vampytest.assert_eq(copy, guild_activity_overview_activity)


def test__GuildActivityOverviewActivity__copy_with__no_fields():
    """
    Tests whether ``GuildActivityOverviewActivity.copy`` works as intended.
    
    Case: no fields given.
    """
    level = GuildActivityOverviewActivityLevel.recently_popular
    score = 1352
    
    guild_activity_overview_activity = GuildActivityOverviewActivity(level = level, score = score)
    
    copy = guild_activity_overview_activity.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_activity_overview_activity)
    vampytest.assert_eq(copy, guild_activity_overview_activity)


def test__GuildActivityOverviewActivity__copy_with__all_fields():
    """
    Tests whether ``GuildActivityOverviewActivity.copy`` works as intended.
    
    Case: all fields given.
    """
    old_level = GuildActivityOverviewActivityLevel.recently_popular
    old_score = 1352
    
    new_level = GuildActivityOverviewActivityLevel.any_previous
    new_score = 1463
    
    guild_activity_overview_activity = GuildActivityOverviewActivity(level = old_level, score = old_score)
    
    copy = guild_activity_overview_activity.copy_with(level = new_level, score = new_score)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_activity_overview_activity)
    
    vampytest.assert_is(copy.level, new_level)
    vampytest.assert_eq(copy.score, new_score)
