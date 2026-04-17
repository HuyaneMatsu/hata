import vampytest

from ..fields import validate_discoverability_state
from ..preinstanced import ApplicationDiscoverabilityState


def _iter_options__passing():
    yield None, ApplicationDiscoverabilityState.none
    yield ApplicationDiscoverabilityState.blocked, ApplicationDiscoverabilityState.blocked
    yield ApplicationDiscoverabilityState.blocked.value, ApplicationDiscoverabilityState.blocked


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_discoverability_state(input_value):
    """
    Tests whether ``validate_discoverability_state`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationDiscoverabilityState``
        
    Raises
    ------
    TypeError
    """
    output = validate_discoverability_state(input_value)
    vampytest.assert_instance(output, ApplicationDiscoverabilityState)
    return output
