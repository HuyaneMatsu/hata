import vampytest

from ..fields import put_id


def _iter_options():
    scheduled_event_id = 202303150004
    
    yield 0, False, {'id': None}
    yield 0, True, {'id': None}
    yield scheduled_event_id, False, {'id': str(scheduled_event_id)}
    yield scheduled_event_id, True, {'id': str(scheduled_event_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id(input_value, defaults):
    """
    Tests whether ``put_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_id(input_value, {}, defaults)
