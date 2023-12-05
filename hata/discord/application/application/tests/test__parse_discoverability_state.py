import vampytest

from ..fields import parse_discoverability_state
from ..preinstanced import ApplicationDiscoverabilityState


def _iter_options():
    yield {}, ApplicationDiscoverabilityState.none
    yield (
        {'discoverability_state': ApplicationDiscoverabilityState.blocked.value},
        ApplicationDiscoverabilityState.blocked,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_discoverability_state(input_data):
    """
    Tests whether ``parse_discoverability_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationDiscoverabilityState``
    """
    output = parse_discoverability_state(input_data)
    vampytest.assert_instance(output, ApplicationDiscoverabilityState)
    return output
