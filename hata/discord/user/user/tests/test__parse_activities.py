import vampytest

from ....activity import Activity

from ..fields import parse_activities


def test__parse_activities():
    """
    Tests whether ``parse_activities`` works as intended.
    """
    activity_0 = Activity('my master')
    activity_1 = Activity('my lord')
    
    for input_data, expected_output in (
        ({}, None),
        ({'activities': None}, None),
        ({'activities': []}, None),
        ({'activities': [activity_0.to_data()]}, [activity_0]),
        ({'activities': [activity_0.to_data(), activity_1.to_data()]}, [activity_0, activity_1]),
    ):
        output = parse_activities(input_data)
        vampytest.assert_eq(output, expected_output)
