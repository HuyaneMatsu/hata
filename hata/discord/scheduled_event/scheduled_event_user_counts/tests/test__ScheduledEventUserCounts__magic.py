from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..scheduled_event_user_counts import ScheduledEventUserCounts


def test__ScheduledEventUserCounts__repr():
    """
    Tests whether ``ScheduledEventUserCounts.__repr__`` works as intended.
    """
    count = 120
    occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    scheduled_event_user_counts = ScheduledEventUserCounts(
        count = count,
        occasion_counts = occasion_counts,
    )
    
    output = repr(scheduled_event_user_counts)
    vampytest.assert_instance(output, str)


def test__ScheduledEventUserCounts__hash():
    """
    Tests whether ``ScheduledEventUserCounts.__hash__`` works as intended.
    """
    count = 120
    occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    scheduled_event_user_counts = ScheduledEventUserCounts(
        count = count,
        occasion_counts = occasion_counts,
    )
    
    output = hash(scheduled_event_user_counts)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    count = 120
    occasion_counts = {
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc) : 52,
    }
    
    keyword_parameters = {
        'count': count,
        'occasion_counts': occasion_counts,
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
            'count': 100,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'occasion_counts': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduledEventUserCounts__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventUserCounts.__eq__`` works as intended.
    
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
    scheduled_event_user_counts_0 = ScheduledEventUserCounts(**keyword_parameters_0)
    scheduled_event_user_counts_1 = ScheduledEventUserCounts(**keyword_parameters_1)
    
    output = scheduled_event_user_counts_0 == scheduled_event_user_counts_1
    vampytest.assert_instance(output, bool)
    return output
