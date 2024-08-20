import vampytest

from ..fields import parse_channel_id


def _iter_options():
    channel_id = 202303110000
    
    yield {}, 0
    yield {'channel_id': None}, 0
    yield {'channel_id': str(channel_id)}, channel_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_channel_id(input_data):
    """
    Tests whether ``parse_channel_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_channel_id(input_data)
    vampytest.assert_instance(output, int)
    return output
