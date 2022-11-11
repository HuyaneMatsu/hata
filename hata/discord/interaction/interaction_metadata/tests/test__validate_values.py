import vampytest

from ..fields import validate_values


def test__validate_values__0():
    """
    Tests whether `validate_values` works as intended.
    
    Case: passing.
    """
    for input_values, expected_output in (
        (None, None),
        ([], None),
        (['a'], ('a', )),
    ):
        output = validate_values(input_values)
        vampytest.assert_eq(output, expected_output)


def test__validate_values__1():
    """
    Tests whether `validate_values` works as intended.
    
    Case: `TypeError`.
    """
    for input_values in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_values(input_values)
