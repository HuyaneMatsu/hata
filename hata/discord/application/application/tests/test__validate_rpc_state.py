import vampytest

from ..fields import validate_rpc_state
from ..preinstanced import ApplicationRPCState


def _iter_options__passing():
    yield None, ApplicationRPCState.none
    yield ApplicationRPCState.approved, ApplicationRPCState.approved
    yield ApplicationRPCState.approved.value, ApplicationRPCState.approved


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_rpc_state(input_value):
    """
    Tests whether ``validate_rpc_state`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationRPCState``
        
    Raises
    ------
    TypeError
    """
    output = validate_rpc_state(input_value)
    vampytest.assert_instance(output, ApplicationRPCState)
    return output
