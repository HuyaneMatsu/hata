import vampytest

from ..fields import validate_max_value


def test__validate_max_value__0():
    """
    Tests whether `validate_max_value` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        (10, 10),
        (10.0, 10.0),
    ):
        output = validate_max_value(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_max_value__1():
    """
    Tests whether `validate_max_value` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'pepe',
    ):
        with vampytest.assert_raises(TypeError):
            validate_max_value(input_value)
