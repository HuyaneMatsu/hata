import vampytest

from ..fields import validate_verification_level
from ..preinstanced import VerificationLevel


def test__validate_verification_level__0():
    """
    Tests whether `validate_verification_level` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (VerificationLevel.medium, VerificationLevel.medium),
        (VerificationLevel.medium.value, VerificationLevel.medium)
    ):
        output = validate_verification_level(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_verification_level__1():
    """
    Tests whether `validate_verification_level` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_verification_level(input_value)
