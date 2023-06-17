import vampytest

from ..fields import validate_premium_tier


def test__validate_premium_tier__0():
    """
    Tests whether `validate_premium_tier` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_premium_tier(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_premium_tier__1():
    """
    Tests whether `validate_premium_tier` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_premium_tier(input_value)


def test__validate_premium_tier__2():
    """
    Tests whether `validate_premium_tier` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_premium_tier(input_value)
