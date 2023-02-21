import vampytest

from ..fields import validate_target_id


def test__validate_target_id__0():
    """
    Tests whether `validate_target_id` works as intended.
    
    Case: passing.
    """
    target_id = 202302200002
    
    for input_value, expected_output in (
        (target_id, target_id),
        (str(target_id), target_id),
    ):
        output = validate_target_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_target_id__1():
    """
    Tests whether `validate_target_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_target_id(input_value)


def test__validate_target_id__2():
    """
    Tests whether `validate_target_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_target_id(input_value)
