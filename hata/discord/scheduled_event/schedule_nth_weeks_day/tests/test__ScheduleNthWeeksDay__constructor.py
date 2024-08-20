import vampytest

from ..preinstanced import ScheduleWeeksDay
from ..schedule_nth_weeks_day import ScheduleNthWeeksDay


def _assert_fields_set(nth_weeks_day):
    """
    Asserts whether every field is set of the given nth week's day.
    
    Parameters
    ----------
    nth_weeks_day : ``ScheduleNthWeeksDay``
        The instance to check.
    """
    vampytest.assert_instance(nth_weeks_day, ScheduleNthWeeksDay)
    vampytest.assert_instance(nth_weeks_day.nth_week, int)
    vampytest.assert_instance(nth_weeks_day.weeks_day, ScheduleWeeksDay)


def test__ScheduleNthWeeksDay__new__no_fields():
    """
    Tests whether ``ScheduleNthWeeksDay.__new__`` works as intended.
    
    Case: no fields given.
    """
    nth_weeks_day = ScheduleNthWeeksDay()
    _assert_fields_set(nth_weeks_day)


def test__ScheduleNthWeeksDay__new__all_fields():
    """
    Tests whether ``ScheduleNthWeeksDay.__new__`` works as intended.
    
    Case: all fields given.
    """
    nth_week = 3
    weeks_day = ScheduleWeeksDay.sunday
    
    nth_weeks_day = ScheduleNthWeeksDay(
        nth_week = nth_week,
        weeks_day = weeks_day,
    )
    _assert_fields_set(nth_weeks_day)
    
    vampytest.assert_eq(nth_weeks_day.nth_week, nth_week)
    vampytest.assert_is(nth_weeks_day.weeks_day, weeks_day)
