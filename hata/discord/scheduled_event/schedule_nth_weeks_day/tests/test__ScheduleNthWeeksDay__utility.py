import vampytest

from ..preinstanced import ScheduleWeeksDay
from ..schedule_nth_weeks_day import ScheduleNthWeeksDay

from .test__ScheduleNthWeeksDay__constructor import _assert_fields_set


def test__ScheduleNthWeeksDay__copy():
    """
    Tests whether ``ScheduleNthWeeksDay.copy`` works as intended.
    """
    nth_week = 3
    weeks_day = ScheduleWeeksDay.sunday
    
    nth_weeks_day = ScheduleNthWeeksDay(
        nth_week = nth_week,
        weeks_day = weeks_day,
    )
    
    copy = nth_weeks_day.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(nth_weeks_day, copy)
    vampytest.assert_eq(nth_weeks_day, copy)


def test__ScheduleNthWeeksDay__copy_with__no_fields():
    """
    Tests whether ``ScheduleNthWeeksDay.copy_with`` works as intended.
    
    Case: No fields given.
    """
    nth_week = 3
    weeks_day = ScheduleWeeksDay.sunday
    
    nth_weeks_day = ScheduleNthWeeksDay(
        nth_week = nth_week,
        weeks_day = weeks_day,
    )
    
    copy = nth_weeks_day.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(nth_weeks_day, copy)
    vampytest.assert_eq(nth_weeks_day, copy)


def test__ScheduleNthWeeksDay__copy_with__all_fields():
    """
    Tests whether ``ScheduleNthWeeksDay.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_nth_week = 3
    old_weeks_day = ScheduleWeeksDay.sunday
    
    new_nth_week = 4
    new_weeks_day = ScheduleWeeksDay.friday
    
    nth_weeks_day = ScheduleNthWeeksDay(
        nth_week = old_nth_week,
        weeks_day = old_weeks_day,
    )
    
    copy = nth_weeks_day.copy_with(
        nth_week = new_nth_week,
        weeks_day = new_weeks_day,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(nth_weeks_day, copy)
    vampytest.assert_ne(nth_weeks_day, copy)
    
    vampytest.assert_eq(copy.nth_week, new_nth_week)
    vampytest.assert_is(copy.weeks_day, new_weeks_day)
