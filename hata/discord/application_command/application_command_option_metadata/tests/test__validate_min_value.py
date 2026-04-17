import vampytest

from ..fields import validate_min_value


def test__validate_min_value__0():
    """
    Tests whether `validate_min_value` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        (10, 10),
        (10.0, 10.0),
    ):
        output = validate_min_value(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_min_value__1():
    """
    Tests whether `validate_min_value` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'pepe',
    ):
        with vampytest.assert_raises(TypeError):
            validate_min_value(input_value)
