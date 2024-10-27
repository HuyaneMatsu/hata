import vampytest

from ..fields import parse_target_message_id


def _iter_options():
    target_message_id = 202410060003
    
    yield {}, 0
    yield {'target_message_id': None}, 0
    yield {'target_message_id': str(target_message_id)}, target_message_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_target_message_id(input_data):
    """
    Tests whether ``parse_target_message_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_target_message_id(input_data)
    vampytest.assert_instance(output, int)
    return output
