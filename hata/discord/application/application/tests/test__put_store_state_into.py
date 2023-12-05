import vampytest

from ..fields import put_store_state_into
from ..preinstanced import ApplicationStoreState


def _iter_options():
    yield (
        ApplicationStoreState.approved,
        False,
        {'store_application_state': ApplicationStoreState.approved.value},
    )
    yield (
        ApplicationStoreState.approved,
        True,
        {'store_application_state': ApplicationStoreState.approved.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_store_state_into(input_value, defaults):
    """
    Tests whether ``put_store_state_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationStoreState``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_store_state_into(input_value, {}, defaults)
