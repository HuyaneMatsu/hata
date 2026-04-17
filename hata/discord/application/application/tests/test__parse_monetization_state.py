import vampytest

from ..fields import parse_monetization_state
from ..preinstanced import ApplicationMonetizationState


def _iter_options():
    yield {}, ApplicationMonetizationState.none
    yield {'monetization_state': ApplicationMonetizationState.disabled.value}, ApplicationMonetizationState.disabled


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_monetization_state(input_data):
    """
    Tests whether ``parse_monetization_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationMonetizationState``
    """
    output = parse_monetization_state(input_data)
    vampytest.assert_instance(output, ApplicationMonetizationState)
    return output
