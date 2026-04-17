import vampytest

from ..fields import validate_creator_monetization_state
from ..preinstanced import ApplicationMonetizationState


def _iter_options__passing():
    yield None, ApplicationMonetizationState.none
    yield ApplicationMonetizationState.disabled, ApplicationMonetizationState.disabled
    yield ApplicationMonetizationState.disabled.value, ApplicationMonetizationState.disabled


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_creator_monetization_state(input_value):
    """
    Tests whether ``validate_creator_monetization_state`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationMonetizationState``
        
    Raises
    ------
    TypeError
    """
    output = validate_creator_monetization_state(input_value)
    vampytest.assert_instance(output, ApplicationMonetizationState)
    return output
