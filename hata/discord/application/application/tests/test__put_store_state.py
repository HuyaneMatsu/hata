import vampytest

from ..fields import put_store_state
from ..preinstanced import ApplicationStoreState


def _iter_options():
    yield (
        ApplicationStoreState.none,
        False,
        {'store_application_state': ApplicationStoreState.none.value},
    )
    yield (
        ApplicationStoreState.none,
        True,
        {'store_application_state': ApplicationStoreState.none.value},
    )
    
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
def test__put_store_state(input_value, defaults):
    """
    Tests whether ``put_store_state`` is working as intended.
    
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
    return put_store_state(input_value, {}, defaults)
