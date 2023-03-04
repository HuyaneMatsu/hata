import vampytest

from ..fields import parse_type
from ..preinstanced import OnboardingPromptType


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, OnboardingPromptType.multiple_choice),
        ({'type': OnboardingPromptType.multiple_choice.value}, OnboardingPromptType.multiple_choice),
        ({'type': OnboardingPromptType.dropdown.value}, OnboardingPromptType.dropdown),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
