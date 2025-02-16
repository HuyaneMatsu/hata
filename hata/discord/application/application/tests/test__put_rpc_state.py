import vampytest

from ..fields import put_rpc_state
from ..preinstanced import ApplicationRPCState


def _iter_options():
    yield (
        ApplicationRPCState.approved,
        False,
        {'rpc_application_state': ApplicationRPCState.approved.value},
    )
    yield (
        ApplicationRPCState.approved,
        True,
        {'rpc_application_state': ApplicationRPCState.approved.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_rpc_state(input_value, defaults):
    """
    Tests whether ``put_rpc_state`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationRPCState``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_rpc_state(input_value, {}, defaults)
