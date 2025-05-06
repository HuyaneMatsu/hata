import vampytest

from ...guild_activity_overview_activity import GuildActivityOverviewActivity

from ..fields import validate_activities


def _iter_options__passing():
    application_id_0 = 202504200004
    application_id_1 = 202504200005
    
    yield (
        None,
        None,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            application_id_0 : GuildActivityOverviewActivity(level = 1, score = 23),
            application_id_1 : GuildActivityOverviewActivity(level = 2, score = 664),
        },
        {
            application_id_0 : GuildActivityOverviewActivity(level = 1, score = 23),
            application_id_1 : GuildActivityOverviewActivity(level = 2, score = 664),
        },
    )


def _iter_options__type_error():
    application_id_0 = 202504200006
    yield ''
    yield {'56' : GuildActivityOverviewActivity(level = 1, score = 23)}
    yield {application_id_0 : 'level, score'}
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_activities(activities):
    """
    Tests whether ``validate_activities`` works as intended.
    
    Parameters
    ----------
    activities : `object`
        Activities to validate.
    
    Returns
    -------
    output : `None | dict<int, GuildActivityOverviewActivity>`
    
    Raises
    ------
    TypeError
        - If `activities` type is incorrect.
    """
    return validate_activities(activities)
