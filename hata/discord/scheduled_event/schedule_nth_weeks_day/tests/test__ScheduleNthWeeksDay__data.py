import vampytest

from ..preinstanced import ScheduleWeeksDay
from ..schedule_nth_weeks_day import ScheduleNthWeeksDay

from .test__ScheduleNthWeeksDay__constructor import _assert_fields_set


def test__ScheduleNthWeeksDay__from_data():
    """
    Tests whether ``ScheduleNthWeeksDay.from_data`` works as intended.
    """
    nth_week = 3
    weeks_day = ScheduleWeeksDay.sunday
    
    data = {
        'n': nth_week,
        'day': weeks_day.value,
    }
    
    nth_weeks_day = ScheduleNthWeeksDay.from_data(data)
    _assert_fields_set(nth_weeks_day)
    
    vampytest.assert_eq(nth_weeks_day.nth_week, nth_week)
    vampytest.assert_is(nth_weeks_day.weeks_day, weeks_day)


def test__ScheduleNthWeeksDay__to_data():
    """
    Tests whether ``ScheduleNthWeeksDay.to_data`` works as intended.
    """
    nth_week = 3
    weeks_day = ScheduleWeeksDay.sunday
    
    nth_weeks_day = ScheduleNthWeeksDay(
        nth_week = nth_week,
        weeks_day = weeks_day,
    )
    
    output = nth_weeks_day.to_data(defaults = True)
    
    vampytest.assert_eq(
        output,
        {
            'n': nth_week,
            'day': weeks_day.value,
        },
    )
