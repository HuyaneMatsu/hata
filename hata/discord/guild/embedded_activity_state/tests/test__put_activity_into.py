import vampytest

from ....activity import Activity, ActivityType

from ..fields import put_activity_into


def test__put_activity_into():
    """
    Tests whether ``put_activity_into`` works as intended.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing)
    
    for input_value, expected_output in (
        (activity, {'embedded_activity': activity.to_data(include_internals = True, user = True)}),
    ):
        output = put_activity_into(input_value, {}, True)
        vampytest.assert_eq(output, expected_output)
