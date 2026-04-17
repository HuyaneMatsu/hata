import vampytest

from ..fields import validate_verify_key


def test__validate_verify_key__0():
    """
    Tests whether `validate_verify_key` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_verify_key(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_verify_key__1():
    """
    Tests whether `validate_verify_key` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_verify_key(input_value)
