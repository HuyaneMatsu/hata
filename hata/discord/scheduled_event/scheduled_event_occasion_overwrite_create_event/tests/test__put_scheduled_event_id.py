import vampytest

from ..fields import put_scheduled_event_id


def _iter_options():
    scheduled_event_id = 202506210044
    
    yield 0, False, {'event_id': None}
    yield 0, True, {'event_id': None}
    yield scheduled_event_id, False, {'event_id': str(scheduled_event_id)}
    yield scheduled_event_id, True, {'event_id': str(scheduled_event_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_scheduled_event_id(input_value, defaults):
    """
    Tests whether ``put_scheduled_event_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_scheduled_event_id(input_value, {}, defaults)
