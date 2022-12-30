import vampytest

from ....activity import Activity, ActivityType

from ..fields import parse_activity


def test__parse_activity():
    """
    Tests whether ``parse_activity`` works as intended.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing)
    
    for input_data, expected_output in (
        ({'embedded_activity': activity.to_data(include_internals = True, user = True)}, activity),
        ({'embedded_activity': None}, Activity()),
        ({}, Activity()),
    ):
        output = parse_activity(input_data)
        vampytest.assert_eq(output, expected_output)
