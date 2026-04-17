import vampytest

from ..fields import validate_distributor


def test__validate_distributor__0():
    """
    Tests whether `validate_distributor` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, ''),
        ('a', 'a'),
    ):
        output = validate_distributor(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_distributor__1():
    """
    Tests whether `validate_distributor` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_distributor(input_value)
