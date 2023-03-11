import vampytest

from ...scheduled_event import PrivacyLevel

from ..fields import validate_privacy_level


def test__validate_privacy_level__0():
    """
    Tests whether `validate_privacy_level` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (PrivacyLevel.public, PrivacyLevel.public),
        (PrivacyLevel.public.value, PrivacyLevel.public)
    ):
        output = validate_privacy_level(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_privacy_level__1():
    """
    Tests whether `validate_privacy_level` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_privacy_level(input_value)
