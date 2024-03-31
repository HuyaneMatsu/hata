import vampytest

from ..fields import parse_interacted_message_id


def _iter_options():
    interacted_message_id = 202403050017
    
    yield {}, 0
    yield {'interacted_message_id': None}, 0
    yield {'interacted_message_id': str(interacted_message_id)}, interacted_message_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_interacted_message_id(input_data):
    """
    Tests whether ``parse_interacted_message_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    return parse_interacted_message_id(input_data)
