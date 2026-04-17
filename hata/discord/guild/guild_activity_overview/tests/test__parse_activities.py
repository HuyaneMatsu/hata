import vampytest

from ...guild_activity_overview_activity import GuildActivityOverviewActivity

from ..fields import parse_activities


def _iter_options():
    application_id_0 = 202504200000
    application_id_1 = 202504200001
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'game_activity': None,
        },
        None,
    )
    
    yield (
        {
            'game_activity': {},
        },
        None,
    )
    
    yield (
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
        {
            application_id_0 : GuildActivityOverviewActivity(level = 1, score = 23),
            application_id_1 : GuildActivityOverviewActivity(level = 2, score = 664),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_activities(input_data):
    """
    Tests whether ``parse_activities`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | dict<int, GuildActivityOverviewActivity>`
    """
    output = parse_activities(input_data)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
