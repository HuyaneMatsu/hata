import vampytest

from ..preinstanced import ScheduleWeeksDay
from ..schedule_nth_weeks_day import ScheduleNthWeeksDay


def test__ScheduleNthWeeksDay__repr():
    """
    Tests whether ``ScheduleNthWeeksDay.__repr__`` works as intended.
    """
    nth_week = 3
    weeks_day = ScheduleWeeksDay.sunday
    
    nth_weeks_day = ScheduleNthWeeksDay(
        nth_week = nth_week,
        weeks_day = weeks_day,
    )
    
    output = repr(nth_weeks_day)
    vampytest.assert_instance(output, str)


def test__ScheduleNthWeeksDay__hash():
    """
    Tests whether ``ScheduleNthWeeksDay.__hash__`` works as intended.
    """
    nth_week = 3
    weeks_day = ScheduleWeeksDay.sunday
    
    nth_weeks_day = ScheduleNthWeeksDay(
        nth_week = nth_week,
        weeks_day = weeks_day,
    )
    
    output = hash(nth_weeks_day)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    nth_week = 3
    weeks_day = ScheduleWeeksDay.sunday
    
    keyword_parameters = {
        'nth_week': nth_week,
        'weeks_day': weeks_day,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'nth_week': 4,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'weeks_day': ScheduleWeeksDay.friday,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduleNthWeeksDay__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduleNthWeeksDay.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    nth_weeks_day_0 = ScheduleNthWeeksDay(**keyword_parameters_0)
    nth_weeks_day_1 = ScheduleNthWeeksDay(**keyword_parameters_1)
    output = nth_weeks_day_0 == nth_weeks_day_1
    vampytest.assert_instance(output, bool)
    return output


def test__ScheduleNthWeeksDay__sorting():
    """
    Tests whether sorting ``ScheduleNthWeeksDay`` works as intended.
    """
    nth_weeks_day_0 = ScheduleNthWeeksDay(
        nth_week = 1,
        weeks_day = ScheduleWeeksDay.sunday,
    )
    
    nth_weeks_day_1 = ScheduleNthWeeksDay(
        nth_week = 2,
        weeks_day = ScheduleWeeksDay.sunday,
    )
    
    nth_weeks_day_2 = ScheduleNthWeeksDay(
        nth_week = 2,
        weeks_day = ScheduleWeeksDay.friday,
    )
    
    output = [nth_weeks_day_0, nth_weeks_day_1, nth_weeks_day_2]
    output.sort()
    
    vampytest.assert_eq(
        output,
        [nth_weeks_day_0, nth_weeks_day_2, nth_weeks_day_1],
    )
