import vampytest

from ....activity import Activity, ActivityType

from ...embedded_activity_state import EmbeddedActivityState

from ..fields import put_embedded_activity_states_into


def _iter_options():
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202306160020)
    channel_id = 202306160021
    guild_id = 202306160022
    user_ids = [202306160023, 202306160024]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    yield None, False, {'embedded_activities': []}
    yield None, True, {'embedded_activities': []}
    yield {}, True, {'embedded_activities': []}
    yield (
        {embedded_activity_state},
        True,
        {'embedded_activities': [embedded_activity_state.to_data(defaults = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_embedded_activity_states_into(input_value, defaults):
    """
    Tests whether ``put_embedded_activity_states_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<int, EmbeddedActivityState>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_embedded_activity_states_into(input_value, {}, defaults)
