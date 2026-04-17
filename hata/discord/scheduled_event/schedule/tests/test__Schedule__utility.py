from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...schedule_nth_weeks_day import ScheduleNthWeeksDay, ScheduleWeeksDay

from ..preinstanced import ScheduleFrequency, ScheduleMonth
from ..schedule import Schedule

from .test__Schedule__constructor import _assert_fields_set


def test__Schedule__copy():
    """
    Tests whether ``Schedule.copy`` works as intended.
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
    
    copy = schedule.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(schedule, copy)
    vampytest.assert_eq(schedule, copy)


def test__Schedule__copy_with__no_fields():
    """
    Tests whether ``Schedule.copy_with`` works as intended.
    
    Case: No fields given.
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
    
    copy = schedule.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(schedule, copy)
    vampytest.assert_eq(schedule, copy)


def test__Schedule__copy_with__all_fields():
    """
    Tests whether ``Schedule.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_by_month_days = [2, 3]
    old_by_months = [ScheduleMonth.august, ScheduleMonth.december]
    old_by_nth_weeks_days = [ScheduleNthWeeksDay(nth_week = 3), ScheduleNthWeeksDay(nth_week = 4)]
    old_by_weeks_days = [ScheduleWeeksDay.friday, ScheduleWeeksDay.saturday]
    old_by_year_days = [32, 33]
    old_end = DateTime(2016, 8, 14, tzinfo = TimeZone.utc)
    old_frequency = ScheduleFrequency.monthly
    old_occurrence_count_limit = 100
    old_occurrence_spacing = 2
    old_start = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    
    new_by_month_days = [2, 4]
    new_by_months = [ScheduleMonth.august, ScheduleMonth.november]
    new_by_nth_weeks_days = [ScheduleNthWeeksDay(nth_week = 2), ScheduleNthWeeksDay(nth_week = 3)]
    new_by_weeks_days = [ScheduleWeeksDay.friday, ScheduleWeeksDay.sunday]
    new_by_year_days = [32, 34]
    new_end = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    new_frequency = ScheduleFrequency.yearly
    new_occurrence_count_limit = 99
    new_occurrence_spacing = 3
    new_start = DateTime(2016, 5, 13, tzinfo = TimeZone.utc)
    
    schedule = Schedule(
        by_month_days = old_by_month_days,
        by_months = old_by_months,
        by_nth_weeks_days = old_by_nth_weeks_days,
        by_weeks_days = old_by_weeks_days,
        by_year_days = old_by_year_days,
        end = old_end,
        frequency = old_frequency,
        occurrence_count_limit = old_occurrence_count_limit,
        occurrence_spacing = old_occurrence_spacing,
        start = old_start,
    )
    
    copy = schedule.copy_with(
        by_month_days = new_by_month_days,
        by_months = new_by_months,
        by_nth_weeks_days = new_by_nth_weeks_days,
        by_weeks_days = new_by_weeks_days,
        by_year_days = new_by_year_days,
        end = new_end,
        frequency = new_frequency,
        occurrence_count_limit = new_occurrence_count_limit,
        occurrence_spacing = new_occurrence_spacing,
        start = new_start,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(schedule, copy)
    vampytest.assert_ne(schedule, copy)


    vampytest.assert_eq(copy.by_month_days, tuple(new_by_month_days))
    vampytest.assert_eq(copy.by_months, tuple(new_by_months))
    vampytest.assert_eq(copy.by_nth_weeks_days, tuple(new_by_nth_weeks_days))
    vampytest.assert_eq(copy.by_weeks_days, tuple(new_by_weeks_days))
    vampytest.assert_eq(copy.by_year_days, tuple(new_by_year_days))
    vampytest.assert_eq(copy.end, new_end)
    vampytest.assert_is(copy.frequency, new_frequency)
    vampytest.assert_eq(copy.occurrence_count_limit, new_occurrence_count_limit)
    vampytest.assert_eq(copy.occurrence_spacing, new_occurrence_spacing)
    vampytest.assert_eq(copy.start, new_start)
