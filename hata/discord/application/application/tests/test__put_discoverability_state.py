import vampytest

from ..fields import put_discoverability_state
from ..preinstanced import ApplicationDiscoverabilityState


def _iter_options():
    yield (
        ApplicationDiscoverabilityState.blocked,
        False,
        {'discoverability_state': ApplicationDiscoverabilityState.blocked.value},
    )
    yield (
        ApplicationDiscoverabilityState.blocked,
        True,
        {'discoverability_state': ApplicationDiscoverabilityState.blocked.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_discoverability_state(input_value, defaults):
    """
    Tests whether ``put_discoverability_state`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationDiscoverabilityState``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_discoverability_state(input_value, {}, defaults)
