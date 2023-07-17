import vampytest

from ..fields import parse_mode
from ..preinstanced import OnboardingMode


def _iter_options():
    yield {}, OnboardingMode.default
    yield {'mode': OnboardingMode.advanced.value}, OnboardingMode.advanced


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mode(input_data):
    """
    Tests whether ``parse_mode`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``OnboardingMode``
    """
    return parse_mode(input_data)
