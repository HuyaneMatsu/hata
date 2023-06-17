import vampytest

from ....activity import Activity, ActivityType

from ...embedded_activity_state import EmbeddedActivityState

from ..fields import validate_embedded_activity_states


def test__validate_embedded_activity_states__0():
    """
    Tests whether ``validate_embedded_activity_states`` works as intended.
    
    Case: passing.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202306160025)
    channel_id = 202306160026
    guild_id = 202306160027
    user_ids = [202306160028, 202306160029]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ({}, None),
        ([embedded_activity_state], {embedded_activity_state}),
    ):
        output = validate_embedded_activity_states(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_embedded_activity_states__1():
    """
    Tests whether ``validate_embedded_activity_states`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_embedded_activity_states(input_value)
