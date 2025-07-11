import vampytest

from ..fields import parse_scheduled_event_id


def _iter_options():
    scheduled_event_id = 202506210043
    
    yield {}, 0
    yield {'event_id': None}, 0
    yield {'event_id': str(scheduled_event_id)}, scheduled_event_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_scheduled_event_id(input_data):
    """
    Tests whether ``parse_scheduled_event_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_scheduled_event_id(input_data)
    vampytest.assert_instance(output, int)
    return output
