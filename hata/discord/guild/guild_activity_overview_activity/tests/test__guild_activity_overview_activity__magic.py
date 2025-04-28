import vampytest

from ..guild_activity_overview_activity import GuildActivityOverviewActivity
from ..preinstanced import GuildActivityOverviewActivityLevel


def test__GuildActivityOverviewActivity__repr():
    """
    Tests whether ``GuildActivityOverviewActivity.__repr__`` works as intended.
    """
    level = GuildActivityOverviewActivityLevel.recently_popular
    score = 1352
    
    guild_activity_overview_activity = GuildActivityOverviewActivity(level = level, score = score)
    
    output = repr(guild_activity_overview_activity)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(guild_activity_overview_activity).__name__, output)
    vampytest.assert_in(f'level = {level.name} ~ {level.value}', output)
    vampytest.assert_in(f'score = {score!r}', output)


def test__GuildActivityOverviewActivity__hash():
    """
    Tests whether ``GuildActivityOverviewActivity.__repr__`` works as intended.
    """
    level = 2
    score = 1352
    
    guild_activity_overview_activity = GuildActivityOverviewActivity(level = level, score = score)
    
    output = hash(guild_activity_overview_activity)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    level = GuildActivityOverviewActivityLevel.recently_popular
    score = 1352
    
    keyword_parameters = {
        'level': level,
        'score': score,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'level': GuildActivityOverviewActivityLevel.any_previous,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'score': 1436,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__GuildActivityOverviewActivity__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``GuildActivityOverviewActivity.__eq__`` works as intended.
    
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
    guild_activity_overview_activity_0 = GuildActivityOverviewActivity(**keyword_parameters_0)
    guild_activity_overview_activity_1 = GuildActivityOverviewActivity(**keyword_parameters_1)
    
    output = guild_activity_overview_activity_0 == guild_activity_overview_activity_1
    vampytest.assert_instance(output, bool)
    return output
