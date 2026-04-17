import vampytest

from ..fields import parse_type
from ..preinstanced import OnboardingPromptType


def _iter_options():
    yield {}, OnboardingPromptType.multiple_choice
    yield {'type': OnboardingPromptType.multiple_choice.value}, OnboardingPromptType.multiple_choice
    yield {'type': OnboardingPromptType.dropdown.value}, OnboardingPromptType.dropdown


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``OnboardingPromptType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, OnboardingPromptType)
    return output
