import vampytest

from ..fields import validate_store_state
from ..preinstanced import ApplicationStoreState


def _iter_options__passing():
    yield None, ApplicationStoreState.none
    yield ApplicationStoreState.approved, ApplicationStoreState.approved
    yield ApplicationStoreState.approved.value, ApplicationStoreState.approved


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_store_state(input_value):
    """
    Tests whether ``validate_store_state`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationStoreState``
        
    Raises
    ------
    TypeError
    """
    output = validate_store_state(input_value)
    vampytest.assert_instance(output, ApplicationStoreState)
    return output
