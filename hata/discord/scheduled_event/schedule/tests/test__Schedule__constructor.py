from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...schedule_nth_weeks_day import ScheduleNthWeeksDay, ScheduleWeeksDay

from ..preinstanced import ScheduleFrequency, ScheduleMonth
from ..schedule import Schedule


def _assert_fields_set(schedule):
    """
    Asserts whether every fields are set of the given schedule.
    
    Parameters
    ----------
    schedule : ``Schedule``
        The schedule to test.
    """
    vampytest.assert_instance(schedule, Schedule)
    vampytest.assert_instance(schedule.by_month_days, tuple, nullable = True)
    vampytest.assert_instance(schedule.by_months, tuple, nullable = True)
    vampytest.assert_instance(schedule.by_nth_weeks_days, tuple, nullable = True)
    vampytest.assert_instance(schedule.by_weeks_days, tuple, nullable = True)
    vampytest.assert_instance(schedule.by_year_days, tuple, nullable = True)
    vampytest.assert_instance(schedule.end, DateTime, nullable = True)
    vampytest.assert_instance(schedule.frequency, ScheduleFrequency)
    vampytest.assert_instance(schedule.occurrence_count_limit, int)
    vampytest.assert_instance(schedule.occurrence_spacing, int)
    vampytest.assert_instance(schedule.start, DateTime, nullable = True)


def test__Schedule__new__no_fields():
    """
    Tests whether ``Schedule.__new__`` works as intended.
    
    Case: No fields given.
    """
    schedule = Schedule()
    _assert_fields_set(schedule)
    

def test__Schedule__new__all_fields():
    """
    Tests whether ``Schedule.__new__`` works as intended.
    
    Case: All fields given.
    """
    by_month_days = [2, 3]
    by_months = [ScheduleMonth.august, ScheduleMonth.december]
    by_nth_weeks_days = [ScheduleNthWeeksDay(nth_week = 3), ScheduleNthWeeksDay(nth_week = 4)]
    by_weeks_days = [ScheduleWeeksDay.friday, ScheduleWeeksDay.saturday]
    by_year_days = [32, 33]
    end = DateTime(2016, 8, 14, tzinfo = TimeZone.utc)
    frequency = ScheduleFrequency.monthly
    occurrence_count_limit = 100
    occurrence_spacing = 2
    start = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    
    schedule = Schedule(
        by_month_days = by_month_days,
        by_months = by_months,
        by_nth_weeks_days = by_nth_weeks_days,
        by_weeks_days = by_weeks_days,
        by_year_days = by_year_days,
        end = end,
        frequency = frequency,
        occurrence_count_limit = occurrence_count_limit,
        occurrence_spacing = occurrence_spacing,
        start = start,
    )
    _assert_fields_set(schedule)
    
    vampytest.assert_eq(schedule.by_month_days, tuple(by_month_days))
    vampytest.assert_eq(schedule.by_months, tuple(by_months))
    vampytest.assert_eq(schedule.by_nth_weeks_days, tuple(by_nth_weeks_days))
    vampytest.assert_eq(schedule.by_weeks_days, tuple(by_weeks_days))
    vampytest.assert_eq(schedule.by_year_days, tuple(by_year_days))
    vampytest.assert_eq(schedule.end, end)
    vampytest.assert_is(schedule.frequency, frequency)
    vampytest.assert_eq(schedule.occurrence_count_limit, occurrence_count_limit)
    vampytest.assert_eq(schedule.occurrence_spacing, occurrence_spacing)
    vampytest.assert_eq(schedule.start, start)


def test__Schedule__create_weekly():
    """
    Tests whether ``Schedule.create_weekly`` works as intended.
    """
    day = ScheduleWeeksDay.tuesday
    
    schedule = Schedule.create_weekly(day)
    _assert_fields_set(schedule)
    
    vampytest.assert_eq(schedule.by_month_days, None)
    vampytest.assert_eq(schedule.by_months, None)
    vampytest.assert_eq(schedule.by_nth_weeks_days, None)
    vampytest.assert_eq(schedule.by_weeks_days, (day,))
    vampytest.assert_eq(schedule.by_year_days, None)
    vampytest.assert_eq(schedule.end, None)
    vampytest.assert_is(schedule.frequency, ScheduleFrequency.weekly)
    vampytest.assert_eq(schedule.occurrence_count_limit, 0)
    vampytest.assert_eq(schedule.occurrence_spacing, 1)
    vampytest.assert_eq(schedule.start, None)


def test__Schedule__create_bi_weekly():
    """
    Tests whether ``Schedule.create_bi_weekly`` works as intended.
    """
    day = ScheduleWeeksDay.tuesday
    
    schedule = Schedule.create_bi_weekly(day)
    _assert_fields_set(schedule)
    
    vampytest.assert_eq(schedule.by_month_days, None)
    vampytest.assert_eq(schedule.by_months, None)
    vampytest.assert_eq(schedule.by_nth_weeks_days, None)
    vampytest.assert_eq(schedule.by_weeks_days, (day,))
    vampytest.assert_eq(schedule.by_year_days, None)
    vampytest.assert_eq(schedule.end, None)
    vampytest.assert_is(schedule.frequency, ScheduleFrequency.weekly)
    vampytest.assert_eq(schedule.occurrence_count_limit, 0)
    vampytest.assert_eq(schedule.occurrence_spacing, 2)
    vampytest.assert_eq(schedule.start, None)


def test__Schedule__create_monthly_nth_weeks_day():
    """
    Tests whether ``Schedule.create_monthly_nth_weeks_day`` works as intended.
    """
    nth_week = 2
    weeks_day = ScheduleWeeksDay.friday
    
    schedule = Schedule.create_monthly_nth_weeks_day(nth_week, weeks_day)
    _assert_fields_set(schedule)
    
    vampytest.assert_eq(schedule.by_month_days, None)
    vampytest.assert_eq(schedule.by_months, None)
    vampytest.assert_eq(schedule.by_nth_weeks_days, (ScheduleNthWeeksDay(nth_week = nth_week, weeks_day = weeks_day), ))
    vampytest.assert_eq(schedule.by_weeks_days, None)
    vampytest.assert_eq(schedule.by_year_days, None)
    vampytest.assert_eq(schedule.end, None)
    vampytest.assert_is(schedule.frequency, ScheduleFrequency.monthly)
    vampytest.assert_eq(schedule.occurrence_count_limit, 0)
    vampytest.assert_eq(schedule.occurrence_spacing, 1)
    vampytest.assert_eq(schedule.start, None)


def test__Schedule__create_yearly_month_nth_day():
    """
    Tests whether ``Schedule.create_yearly_month_nth_day`` works as intended.
    """
    month = ScheduleMonth.august
    nth_day = 15
    
    schedule = Schedule.create_yearly_month_nth_day(month, nth_day)
    _assert_fields_set(schedule)
    
    vampytest.assert_eq(schedule.by_month_days, (nth_day, ))
    vampytest.assert_eq(schedule.by_months, (month, ))
    vampytest.assert_eq(schedule.by_nth_weeks_days, None)
    vampytest.assert_eq(schedule.by_weeks_days, None)
    vampytest.assert_eq(schedule.by_year_days, None)
    vampytest.assert_eq(schedule.end, None)
    vampytest.assert_is(schedule.frequency, ScheduleFrequency.yearly)
    vampytest.assert_eq(schedule.occurrence_count_limit, 0)
    vampytest.assert_eq(schedule.occurrence_spacing, 1)
    vampytest.assert_eq(schedule.start, None)
