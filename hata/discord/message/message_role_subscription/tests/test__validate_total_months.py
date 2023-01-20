import vampytest

from ..fields import validate_total_months


def test__validate_total_months__0():
    """
    Tests whether `validate_total_months` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_total_months(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_total_months__1():
    """
    Tests whether `validate_total_months` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_total_months(input_value)


def test__validate_total_months__2():
    """
    Tests whether `validate_total_months` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_total_months(input_value)
