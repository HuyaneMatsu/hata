import vampytest

from ..fields import parse_type
from ..preinstanced import WebhookType


def _iter_options():
    yield {}, WebhookType.none
    yield {'type': WebhookType.server.value}, WebhookType.server


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``WebhookType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, WebhookType)
    return output
