import vampytest

from ....activity import Activity, ActivityType

from ..fields import validate_removed


def test__validate_removed__0():
    """
    Tests whether ``validate_removed`` works as intended.
    
    Case: passing.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing)
    
    for input_value, expected_output in (
        ([], None),
        ([activity], [activity]),
        (None, None),
    ):
        output = validate_removed(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_removed__1():
    """
    Tests whether ``validate_removed`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
        [12.6,]
    ):
        with vampytest.assert_raises(TypeError):
            validate_removed(input_value)
