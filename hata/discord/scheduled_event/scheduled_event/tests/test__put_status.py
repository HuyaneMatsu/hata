import vampytest

from ..fields import put_status
from ..preinstanced import ScheduledEventStatus


def _iter_options():
    yield ScheduledEventStatus.none, False, {}
    yield ScheduledEventStatus.none, True, {'status': ScheduledEventStatus.none.value}
    yield ScheduledEventStatus.active, False, {'status': ScheduledEventStatus.active.value}
    yield ScheduledEventStatus.active, True, {'status': ScheduledEventStatus.active.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_status(input_value, defaults):
    """
    Tests whether ``put_status`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ScheduledEventStatus``
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_status(input_value, {}, defaults)
