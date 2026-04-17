import vampytest

from ..fields import parse_creator_monetization_state
from ..preinstanced import ApplicationMonetizationState


def _iter_options():
    yield {}, ApplicationMonetizationState.none
    yield {'creator_monetization_state': ApplicationMonetizationState.disabled.value}, ApplicationMonetizationState.disabled


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_creator_monetization_state(input_data):
    """
    Tests whether ``parse_creator_monetization_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationMonetizationState``
    """
    output = parse_creator_monetization_state(input_data)
    vampytest.assert_instance(output, ApplicationMonetizationState)
    return output
