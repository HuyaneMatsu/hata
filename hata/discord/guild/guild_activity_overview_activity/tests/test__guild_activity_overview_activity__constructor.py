import vampytest

from ..guild_activity_overview_activity import GuildActivityOverviewActivity
from ..preinstanced import GuildActivityOverviewActivityLevel


def _assert_fields_set(guild_activity_overview_activity):
    """
    Asserts whether the given guild activity overview activity has all of its fields set.
    
    Parameters
    ----------
    guild_activity_overview_activity : ``GuildActivityOverviewActivity``
        Guild activity overview to test.
    """
    vampytest.assert_instance(guild_activity_overview_activity, GuildActivityOverviewActivity)
    vampytest.assert_instance(guild_activity_overview_activity.level, GuildActivityOverviewActivityLevel)
    vampytest.assert_instance(guild_activity_overview_activity.score, int)



def test__GuildActivityOverviewActivity__new__no_fields():
    """
    Tests whether ``GuildActivityOverviewActivity.__new__`` works as intended.
    
    Case: no fields given.
    """
    guild_activity_overview_activity = GuildActivityOverviewActivity()
    _assert_fields_set(guild_activity_overview_activity)


def test__GuildActivityOverviewActivity__new__all_fields():
    """
    Tests whether ``GuildActivityOverviewActivity.__new__`` works as intended.
    
    Case: all fields given.
    """
    level = GuildActivityOverviewActivityLevel.recently_popular
    score = 1352
    
    guild_activity_overview_activity = GuildActivityOverviewActivity(level = level, score = score)
    _assert_fields_set(guild_activity_overview_activity)
    
    vampytest.assert_is(guild_activity_overview_activity.level, level)
    vampytest.assert_eq(guild_activity_overview_activity.score, score)


def test__GuildActivityOverviewActivity__create_empty():
    """
    Tests whether ``GuildActivityOverviewActivity._create_empty`` works as intended.
    """
    guild_activity_overview_activity = GuildActivityOverviewActivity._create_empty()
    _assert_fields_set(guild_activity_overview_activity)
