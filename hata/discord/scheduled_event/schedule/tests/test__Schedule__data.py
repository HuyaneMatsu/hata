from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ...schedule_nth_weeks_day import ScheduleNthWeeksDay, ScheduleWeeksDay

from ..preinstanced import ScheduleFrequency, ScheduleMonth
from ..schedule import Schedule

from .test__Schedule__constructor import _assert_fields_set


def test__Schedule__from_data():
    """
    Tests whether ``Schedule.from_data`` works as intended.
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
    
    data = {
        'by_month_day': by_month_days,
        'by_month': [value.value for value in by_months],
        'by_n_weekday': [value.to_data(defaults = True) for value in by_nth_weeks_days],
        'by_weekday': [value.value for value in by_weeks_days],
        'by_year_day': by_year_days,
        'end': datetime_to_timestamp(end),
        'frequency': frequency.value,
        'count': occurrence_count_limit,
        'interval': occurrence_spacing,
        'start': datetime_to_timestamp(start),
    }
    
    schedule = Schedule.from_data(data)
    
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


def test__Schedule__to_data():
    """
    Tests whether ``Schedule.to_data`` works as intended.
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
    
    expected_output = {
        'by_month_day': by_month_days,
        'by_month': [value.value for value in by_months],
        'by_n_weekday': [value.to_data(defaults = True) for value in by_nth_weeks_days],
        'by_weekday': [value.value for value in by_weeks_days],
        'by_year_day': by_year_days,
        'end': datetime_to_timestamp(end),
        'frequency': frequency.value,
        'count': occurrence_count_limit,
        'interval': occurrence_spacing,
        'start': datetime_to_timestamp(start),
    }
    
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
    
    vampytest.assert_eq(
        schedule.to_data(defaults = True),
        expected_output,
    )


def test__Schedule__to_data__no_start():
    """
    Tests whether ``Schedule.to_data`` works as intended.
    
    Case: No start, passed into `.to_data` instead.
    """
    start = DateTime(2016, 4, 14, tzinfo = TimeZone.utc)
    
    expected_output = {
        'frequency': ScheduleFrequency.yearly.value,
        'interval': 1,
        'start': datetime_to_timestamp(start),
    }
    
    schedule = Schedule()
    
    vampytest.assert_eq(
        schedule.to_data(start = start),
        expected_output,
    )
