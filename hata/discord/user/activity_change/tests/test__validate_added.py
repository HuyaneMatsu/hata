import vampytest

from ....activity import Activity, ActivityType

from ..fields import validate_added


def test__validate_added__0():
    """
    Tests whether ``validate_added`` works as intended.
    
    Case: passing.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing)
    
    for input_value, expected_output in (
        ([], None),
        ([activity], [activity]),
        (None, None),
    ):
        output = validate_added(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_added__1():
    """
    Tests whether ``validate_added`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
        [12.6,]
    ):
        with vampytest.assert_raises(TypeError):
            validate_added(input_value)
