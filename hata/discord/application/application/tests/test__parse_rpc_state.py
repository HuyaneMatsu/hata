import vampytest

from ..fields import parse_rpc_state
from ..preinstanced import ApplicationRPCState


def _iter_options():
    yield {}, ApplicationRPCState.none
    yield {'rpc_application_state': ApplicationRPCState.submitted.value}, ApplicationRPCState.submitted


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_rpc_state(input_data):
    """
    Tests whether ``parse_rpc_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationRPCState``
    """
    output = parse_rpc_state(input_data)
    vampytest.assert_instance(output, ApplicationRPCState)
    return output
