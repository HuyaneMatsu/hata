import vampytest

from ..fields import validate_default

from ..preinstanced import ApplicationCommandOptionType

def test__validate_default__0():
    """
    Tests whether `validate_default` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (True, True),
        (False, False)
    ):
        output = validate_default(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_default__1():
    """
    Tests whether `validate_default` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_default(input_value)


def test__validate_default__2():
    """
    Tests whether `validate_default` works as intended.
    
    Case: `ValueError`.
    """
    with vampytest.assert_raises(ValueError):
        validate_default(True, ApplicationCommandOptionType.string)
