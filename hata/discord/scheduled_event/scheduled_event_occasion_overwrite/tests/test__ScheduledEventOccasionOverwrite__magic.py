from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite


def test__ScheduledEventOccasionOverwrite__repr():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.__repr__`` works as intended.
    """
    cancelled = True
    end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite(
        cancelled = cancelled,
        end = end,
        start = start,
        timestamp = timestamp,
    )
    
    vampytest.assert_instance(repr(scheduled_event_occasion_overwrite), str)


def test__ScheduledEventOccasionOverwrite__hash():
    """
    Tests whether ``ScheduledEventOccasionOverwrite.__hash__`` works as intended.
    """
    cancelled = True
    end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    scheduled_event_occasion_overwrite = ScheduledEventOccasionOverwrite(
        cancelled = cancelled,
        end = end,
        start = start,
        timestamp = timestamp,
    )
    
    vampytest.assert_instance(hash(scheduled_event_occasion_overwrite), int)


def _iter_options__eq():
    cancelled = True
    end = DateTime(2016, 5, 14, 20, 0, 0, tzinfo = TimeZone.utc)
    start = DateTime(2016, 5, 14, 10, 0, 0, tzinfo = TimeZone.utc)
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    keyword_parameters = {
        'cancelled': cancelled,
        'end': end,
        'start': start,
        'timestamp': timestamp,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'cancelled': False,
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
            'start': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'timestamp': DateTime(2016, 5, 16, 13, 0, 0, tzinfo = TimeZone.utc),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduledEventOccasionOverwrite__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventOccasionOverwrite.__eq__`` works as intended.
    
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
    scheduled_event_occasion_overwrite_0 = ScheduledEventOccasionOverwrite(**keyword_parameters_0)
    scheduled_event_occasion_overwrite_1 = ScheduledEventOccasionOverwrite(**keyword_parameters_1)
    
    output = scheduled_event_occasion_overwrite_0 == scheduled_event_occasion_overwrite_1
    vampytest.assert_instance(output, bool)
    return output



def test__ScheduledEventOccasionOverwrite__sorting():
    """
    Tests whether ``ScheduledEventOccasionOverwrite`` sorting works as intended.
    """
    scheduled_event_occasion_overwrite_0 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    
    scheduled_event_occasion_overwrite_1 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 15, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    
    scheduled_event_occasion_overwrite_2 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 16, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    
    to_sort = [
        scheduled_event_occasion_overwrite_0,
        scheduled_event_occasion_overwrite_1,
        scheduled_event_occasion_overwrite_2,
        scheduled_event_occasion_overwrite_2,
        scheduled_event_occasion_overwrite_1,
        scheduled_event_occasion_overwrite_0,
    ]
    
    to_sort.sort()
    
    vampytest.assert_eq(
        to_sort,
        [
            scheduled_event_occasion_overwrite_0,
            scheduled_event_occasion_overwrite_0,
            scheduled_event_occasion_overwrite_1,
            scheduled_event_occasion_overwrite_1,
            scheduled_event_occasion_overwrite_2,
            scheduled_event_occasion_overwrite_2,
        ],
    )
