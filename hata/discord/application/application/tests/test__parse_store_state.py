import vampytest

from ..fields import parse_store_state
from ..preinstanced import ApplicationStoreState


def _iter_options():
    yield {}, ApplicationStoreState.none
    yield {'store_application_state': ApplicationStoreState.submitted.value}, ApplicationStoreState.submitted


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_store_state(input_data):
    """
    Tests whether ``parse_store_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationStoreState``
    """
    output = parse_store_state(input_data)
    vampytest.assert_instance(output, ApplicationStoreState)
    return output
