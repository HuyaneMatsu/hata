import vampytest

from ..fields import validate_sort_value


def test__validate_sort_value__0():
    """
    Tests whether `validate_sort_value` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_sort_value(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_sort_value__1():
    """
    Tests whether `validate_sort_value` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_sort_value(input_value)


def test__validate_sort_value__2():
    """
    Tests whether `validate_sort_value` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_sort_value(input_value)
