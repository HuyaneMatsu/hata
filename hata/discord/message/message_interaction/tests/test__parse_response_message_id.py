import vampytest

from ..fields import parse_response_message_id


def _iter_options():
    response_message_id = 202403050001
    
    yield {}, 0
    yield {'original_response_message_id': None}, 0
    yield {'original_response_message_id': str(response_message_id)}, response_message_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_response_message_id(input_data):
    """
    Tests whether ``parse_response_message_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    return parse_response_message_id(input_data)
