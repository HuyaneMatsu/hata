import vampytest

from ...guild_activity_overview_activity import GuildActivityOverviewActivity

from ..fields import put_activities


def _iter_options():
    application_id_0 = 202504200002
    application_id_1 = 202504200003
    
    yield (
        None,
        False,
        {
            'game_activity': {},
        },
    )
    
    yield (
        None,
        True,
        {
            'game_activity': {},
        },
    )
    
    yield (
        {
            application_id_0 : GuildActivityOverviewActivity(level = 1, score = 23),
            application_id_1 : GuildActivityOverviewActivity(level = 2, score = 664),
        },
        False,
        {
            'game_activity': {
                str(application_id_0) : {
                    'activity_level': 1,
                    'activity_score': 23,
                },
                str(application_id_1) : {
                    'activity_level': 2,
                    'activity_score': 664,
                },
            },
        },
    )
    
    yield (
        {
            application_id_0 : GuildActivityOverviewActivity(level = 1, score = 23),
            application_id_1 : GuildActivityOverviewActivity(level = 2, score = 664),
        },
        True,
        {
            'game_activity': {
                str(application_id_0) : {
                    'activity_level': 1,
                    'activity_score': 23,
                },
                str(application_id_1) : {
                    'activity_level': 2,
                    'activity_score': 664,
                },
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_activities(input_value, defaults):
    """
    Tests whether ``put_activities`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, GuildActivityOverviewActivity>`
        Value to serialize.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<int, object>`
    """
    return put_activities(input_value, {}, defaults)
