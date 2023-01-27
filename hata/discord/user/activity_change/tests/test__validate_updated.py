import vampytest

from ...activity_update import ActivityUpdate

from ..fields import validate_updated


def test__validate_updated__0():
    """
    Tests whether ``validate_updated`` works as intended.
    
    Case: passing.
    """
    activity_update = ActivityUpdate(old_attributes = {'a': 'b'})
    
    for input_value, expected_output in (
        ([], None),
        ([activity_update], [activity_update]),
        (None, None),
    ):
        output = validate_updated(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_updated__1():
    """
    Tests whether ``validate_updated`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
        [12.6,]
    ):
        with vampytest.assert_raises(TypeError):
            validate_updated(input_value)
