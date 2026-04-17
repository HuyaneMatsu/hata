import vampytest

from ..fields import validate_tier_name


def test__validate_tier_name__0():
    """
    Tests whether `validate_tier_name` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, ''),
        ('a', 'a'),
    ):
        output = validate_tier_name(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_tier_name__1():
    """
    Tests whether `validate_tier_name` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_tier_name(input_value)
