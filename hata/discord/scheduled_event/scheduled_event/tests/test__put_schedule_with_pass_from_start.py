from copy import deepcopy as deep_copy
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...schedule import Schedule

from ....utils import datetime_to_timestamp

from ..fields import put_schedule_with_pass_from_start


def _iter_options():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    schedule = Schedule(occurrence_spacing = 2)
    start = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    
    yield (
        {},
        None,
        False,
        {},
    )
    
    
    yield (
        {},
        schedule,
        False,
        {
            'recurrence_rule': schedule.to_data(defaults = False, start = None),
        },
    )
    
    yield (
        {
            'scheduled_start_time': datetime_to_timestamp(timestamp),
        },
        None,
        False,
        {
            'scheduled_start_time': datetime_to_timestamp(timestamp),
        },
    )
    
    
    yield (
        {
            'scheduled_start_time': datetime_to_timestamp(timestamp),
        },
        schedule,
        False,
        {
            'recurrence_rule': schedule.to_data(defaults = False, start = timestamp),
            'scheduled_start_time': datetime_to_timestamp(timestamp),
        },
    )
    
    yield (
        {
            'scheduled_start_time': datetime_to_timestamp(timestamp),
        },
        schedule.copy_with(start = start),
        False,
        {
            'recurrence_rule': schedule.to_data(defaults = False, start = start),
            'scheduled_start_time': datetime_to_timestamp(timestamp),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_schedule_with_pass_from_start(initial_data, input_value, defaults):
    """
    Tests whether ``put_schedule_with_pass_from_start`` works as intended.
    
    Parameters
    ----------
    initial_data : `dict<str, object>`
        Initial data to serialise into.
    
    input_value : ``None | Schedule``
        Value to serialize.
    
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_schedule_with_pass_from_start(input_value, deep_copy(initial_data), defaults)
