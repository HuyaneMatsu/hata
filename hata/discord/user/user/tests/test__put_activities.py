import vampytest

from ....activity import Activity

from ..fields import put_activities


def test__put_activities():
    """
    Tests whether ``put_activities`` works as intended.
    """
    activity_0 = Activity('hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {'activities': []}),
        ([activity_0], True, {'activities': [activity_0.to_data(defaults = True, include_internals = True, user = True)]}),
    ):
        output = put_activities(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
