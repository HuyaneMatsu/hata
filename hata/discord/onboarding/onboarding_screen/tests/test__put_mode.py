import vampytest

from ..fields import put_mode
from ..preinstanced import OnboardingMode


def _iter_options():
    yield OnboardingMode.advanced, False, {'mode': OnboardingMode.advanced.value}
    yield OnboardingMode.advanced, True, {'mode': OnboardingMode.advanced.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mode(input_value, defaults):
    """
    Tests whether ``put_mode`` is working as intended.
    
    Parameters
    ----------
    input_value : ``OnboardingMode``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_mode(input_value, {}, defaults)
