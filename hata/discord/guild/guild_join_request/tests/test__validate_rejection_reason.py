import vampytest

from ..fields import validate_rejection_reason


def test__validate_rejection_reason__0():
    """
    Tests whether `validate_rejection_reason` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_rejection_reason(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_rejection_reason__1():
    """
    Tests whether `validate_rejection_reason` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_rejection_reason(input_value)
