import vampytest

from ..fields import validate_discriminator


def test__validate_discriminator__0():
    """
    Tests whether `validate_discriminator` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
        ('0099', 99),
    ):
        output = validate_discriminator(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_discriminator__1():
    """
    Tests whether `validate_discriminator` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
        100000,
        "999999",
        "aaa",
    ):
        with vampytest.assert_raises(ValueError):
            validate_discriminator(input_value)


def test__validate_discriminator__2():
    """
    Tests whether `validate_discriminator` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_discriminator(input_value)
