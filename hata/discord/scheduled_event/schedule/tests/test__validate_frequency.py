import vampytest

from ..fields import validate_frequency
from ..preinstanced import ScheduleFrequency


def _iter_options__passing():
    yield None, ScheduleFrequency.yearly
    yield ScheduleFrequency.yearly, ScheduleFrequency.yearly
    yield ScheduleFrequency.yearly.value, ScheduleFrequency.yearly
    yield ScheduleFrequency.daily, ScheduleFrequency.daily


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_frequency(input_value):
    """
    Tests whether ``validate_frequency`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ScheduleFrequency``
    
    Raises
    ------
    TypeError
    """
    output = validate_frequency(input_value)
    vampytest.assert_instance(output, ScheduleFrequency)
    return output
