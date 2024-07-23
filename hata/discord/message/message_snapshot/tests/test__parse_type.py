import vampytest

from ...message.preinstanced import MessageType

from ..fields import parse_type


def _iter_options():
    yield {}, MessageType.default
    yield {'message': {}}, MessageType.default
    yield {'message': {'type': MessageType.call.value}}, MessageType.call


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the type from.
    
    Returns
    -------
    output : ``MessageType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, MessageType)
    return output
