import vampytest

from ....activity import Activity

from ..fields import put_activities_into


def test__put_activities_into():
    """
    Tests whether ``put_activities_into`` works as intended.
    """
    activity_0 = Activity('hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {'activities': []}),
        ([activity_0], True, {'activities': [activity_0.to_data(defaults = True, include_internals = True, user = True)]}),
    ):
        output = put_activities_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
