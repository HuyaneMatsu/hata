import vampytest

from ..fields import validate_mode
from ..preinstanced import OnboardingMode


def _iter_options():
    yield OnboardingMode.advanced, OnboardingMode.advanced
    yield OnboardingMode.advanced.value, OnboardingMode.advanced


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_mode__passing(input_value):
    """
    Tests whether `validate_mode` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``OnboardingMode``
    """
    output = validate_mode(input_value)
    vampytest.assert_instance(output, OnboardingMode)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with('default')
def test__validate_mode__mode_error(input_value):
    """
    Tests whether `validate_mode` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value where we are expecting `TypeError`.
    
    Raises
    ------
    TypeError
    """
    validate_mode(input_value)
