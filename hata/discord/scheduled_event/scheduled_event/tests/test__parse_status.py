import vampytest

from ..fields import parse_status
from ..preinstanced import ScheduledEventStatus


def _iter_options():
    yield {}, ScheduledEventStatus.none
    yield {'status': ScheduledEventStatus.active.value}, ScheduledEventStatus.active


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_status(input_data):
    """
    Tests whether ``parse_status`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ScheduledEventStatus``
    """
    output = parse_status(input_data)
    vampytest.assert_instance(output, ScheduledEventStatus)
    return output
