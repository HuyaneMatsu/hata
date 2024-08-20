import vampytest

from ...schedule_nth_weeks_day import ScheduleNthWeeksDay

from ..fields import validate_by_nth_weeks_days


def _iter_options__passing():
    nth_weeks_day_0 = ScheduleNthWeeksDay(nth_week = 1)
    nth_weeks_day_1 = ScheduleNthWeeksDay(nth_week = 2)
    
    yield None, None
    yield [], None
    yield [nth_weeks_day_0, nth_weeks_day_1], (nth_weeks_day_0, nth_weeks_day_1)
    yield [nth_weeks_day_1, nth_weeks_day_0], (nth_weeks_day_0, nth_weeks_day_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_nth_weeks_day(input_value):
    """
    Tests whether ``validate_by_nth_weeks_days`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<ScheduleNthWeeksDay>`
    
    Raises
    ------
    TypeError
    """
    return validate_by_nth_weeks_days(input_value)
