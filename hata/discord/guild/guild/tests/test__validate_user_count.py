import vampytest

from ..fields import validate_user_count


def test__validate_user_count__0():
    """
    Tests whether `validate_user_count` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (0, 0),
        (1, 1),
    ):
        output = validate_user_count(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_user_count__1():
    """
    Tests whether `validate_user_count` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_user_count(input_value)


def test__validate_user_count__2():
    """
    Tests whether `validate_user_count` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_user_count(input_value)
