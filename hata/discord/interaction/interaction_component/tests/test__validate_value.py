import vampytest

from ..fields import validate_value


def test__validate_value__0():
    """
    Tests whether `validate_value` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_value(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_value__1():
    """
    Tests whether `validate_value` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        object(),
    ):
        with vampytest.assert_raises(TypeError):
            validate_value(input_value)
