import vampytest

from ..fields import validate_weeks_day
from ..preinstanced import ScheduleWeeksDay


def _iter_options__passing():
    yield None, ScheduleWeeksDay.monday
    yield ScheduleWeeksDay.monday, ScheduleWeeksDay.monday
    yield ScheduleWeeksDay.monday.value, ScheduleWeeksDay.monday
    yield ScheduleWeeksDay.tuesday, ScheduleWeeksDay.tuesday


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_weeks_day(input_value):
    """
    Tests whether ``validate_weeks_day`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ScheduleWeeksDay``
    
    Raises
    ------
    TypeError
    """
    output = validate_weeks_day(input_value)
    vampytest.assert_instance(output, ScheduleWeeksDay)
    return output
