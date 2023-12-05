import vampytest

from ..fields import parse_interaction_version
from ..preinstanced import ApplicationInteractionVersion


def _iter_options():
    yield {}, ApplicationInteractionVersion.none
    yield {'interactions_version': ApplicationInteractionVersion.selective.value}, ApplicationInteractionVersion.selective


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_interaction_version(input_data):
    """
    Tests whether ``parse_interaction_version`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationInteractionVersion``
    """
    output = parse_interaction_version(input_data)
    vampytest.assert_instance(output, ApplicationInteractionVersion)
    return output
