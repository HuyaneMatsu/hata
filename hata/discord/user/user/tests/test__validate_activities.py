import vampytest

from ....activity import Activity, ActivityType

from ..fields import validate_activities


def test__validate_activities__0():
    """
    Tests whether ``validate_activities`` works as intended.
    
    Case: passing.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing)
    
    for input_value, expected_output in (
        ([], None),
        ([activity], [activity]),
        (None, None),
    ):
        output = validate_activities(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_activities__1():
    """
    Tests whether ``validate_activities`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
        [12.6,]
    ):
        with vampytest.assert_raises(TypeError):
            validate_activities(input_value)
