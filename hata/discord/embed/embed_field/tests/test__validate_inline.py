import vampytest

from ..fields import validate_inline


def test__validate_inline__0():
    """
    Tests whether `validate_inline` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, False),
        (True, True),
        (False, False)
    ):
        output = validate_inline(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_inline__1():
    """
    Tests whether `validate_inline` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_inline(input_value)
