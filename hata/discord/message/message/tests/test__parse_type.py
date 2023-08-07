import vampytest

from ..fields import parse_type
from ..preinstanced import MessageType


def _iter_options():
    yield {}, MessageType.default
    yield {'type': MessageType.call.value}, MessageType.call


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
    output : ``MessageType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, MessageType)
    return output
