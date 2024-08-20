from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...schedule_nth_weeks_day import ScheduleNthWeeksDay, ScheduleWeeksDay

from ..preinstanced import ScheduleFrequency, ScheduleMonth
from ..schedule import Schedule


def _iter_options__repr():
    yield from ScheduleFrequency.INSTANCES.values()


@vampytest.call_from(_iter_options__repr())
def test__Schedule__repr(frequency):
    """
    Tests whether ``Schedule.__repr__`` works as intended.
    
    Parameters
    ----------
    frequency : ``ScheduleFrequency``
        Frequency to create the instance with.
    """
    by_month_days = [2, 3]
    by_months = [ScheduleMonth.august, ScheduleMonth.december]
    by_nth_weeks_days = [ScheduleNthWeeksDay(nth_week = 3), ScheduleNthWeeksDay(nth_week = 4)]
    by_weeks_days = [ScheduleWeeksDay.friday, ScheduleWeeksDay.saturday]
    by_year_days = [32, 33]
    end = DateTime(2016, 8, 14, tzinfo = TimeZone.utc)
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
    
    output = repr(schedule)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
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
    
    keyword_parameters = {
        'by_month_days': by_month_days,
        'by_months': by_months,
        'by_nth_weeks_days': by_nth_weeks_days,
        'by_weeks_days': by_weeks_days,
        'by_year_days': by_year_days,
        'end': end,
        'frequency': frequency,
        'occurrence_count_limit': occurrence_count_limit,
        'occurrence_spacing': occurrence_spacing,
        'start': start,
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
            'by_month_days': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'by_months': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'by_nth_weeks_days': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'by_weeks_days': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'by_year_days': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'end': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'frequency': ScheduleFrequency.daily,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'occurrence_count_limit': 99,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'occurrence_spacing': 3,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'start': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Schedule__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Schedule.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<object, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    schedule_0 = Schedule(**keyword_parameters_0)
    schedule_1 = Schedule(**keyword_parameters_1)
    
    output = schedule_0 == schedule_1
    vampytest.assert_instance(output, bool)
    return output


def test__Schedule__hash():
    """
    Tests whether ``Schedule.__hash__`` works as intended.
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
    
    output = hash(schedule)
    vampytest.assert_instance(output, int)
