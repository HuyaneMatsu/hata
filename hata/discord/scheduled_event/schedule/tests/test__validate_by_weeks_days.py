import vampytest

from ...schedule_nth_weeks_day import ScheduleWeeksDay

from ..fields import validate_by_weeks_days


def _iter_options__passing():
    yield None, None
    yield [], None
    yield ScheduleWeeksDay.monday, (ScheduleWeeksDay.monday, )
    yield ScheduleWeeksDay.monday.value, (ScheduleWeeksDay.monday, )
    yield [ScheduleWeeksDay.monday], (ScheduleWeeksDay.monday, )
    yield [ScheduleWeeksDay.monday.value], (ScheduleWeeksDay.monday, )
    yield (
        [ScheduleWeeksDay.monday, ScheduleWeeksDay.wednesday],
        (ScheduleWeeksDay.monday, ScheduleWeeksDay.wednesday,),
    )
    yield (
        [ScheduleWeeksDay.wednesday, ScheduleWeeksDay.monday],
        (ScheduleWeeksDay.monday, ScheduleWeeksDay.wednesday,),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_by_weeks_days(input_value):
    """
    Tests whether `validate_by_weeks_days` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<ScheduleWeeksDay>`
    
    Raises
    ------
    TypeError
    """
    return validate_by_weeks_days(input_value)
