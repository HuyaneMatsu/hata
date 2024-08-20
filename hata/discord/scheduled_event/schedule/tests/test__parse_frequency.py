import vampytest

from ..fields import parse_frequency
from ..preinstanced import ScheduleFrequency


def _iter_options():
    yield {}, ScheduleFrequency.yearly
    yield {'frequency': ScheduleFrequency.yearly.value}, ScheduleFrequency.yearly
    yield {'frequency': ScheduleFrequency.daily.value}, ScheduleFrequency.daily


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_frequency(input_data):
    """
    Tests whether ``parse_frequency`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ScheduleFrequency``
    """
    output = parse_frequency(input_data)
    vampytest.assert_instance(output, ScheduleFrequency)
    return output
