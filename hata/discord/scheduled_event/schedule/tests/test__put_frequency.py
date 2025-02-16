import vampytest

from ..fields import put_frequency
from ..preinstanced import ScheduleFrequency


def _iter_options():
    yield ScheduleFrequency.yearly, False, {'frequency': ScheduleFrequency.yearly.value}
    yield ScheduleFrequency.yearly, True, {'frequency': ScheduleFrequency.yearly.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_frequency(input_value, defaults):
    """
    Tests whether ``put_frequency`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ScheduleFrequency``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_frequency(input_value, {}, defaults)
