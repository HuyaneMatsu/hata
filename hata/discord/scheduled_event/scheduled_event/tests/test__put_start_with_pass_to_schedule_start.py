from copy import deepcopy as deep_copy
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ...schedule import Schedule

from ..fields import put_start_with_pass_to_schedule_start


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
        timestamp,
        False,
        {
            'scheduled_start_time': datetime_to_timestamp(timestamp),
        },
    )
    
    yield (
        {
            'recurrence_rule': schedule.to_data(defaults = False),
        },
        None,
        False,
        {
            'recurrence_rule': schedule.to_data(defaults = False),
        },
    )
    
    yield (
        {
            'recurrence_rule': schedule.to_data(defaults = False, start = None),
        },
        timestamp,
        False,
        {
            'scheduled_start_time': datetime_to_timestamp(timestamp),
            'recurrence_rule': schedule.to_data(defaults = False, start = timestamp),
        },
    )
    
    yield (
        {
            'recurrence_rule': schedule.to_data(defaults = False, start = start),
        },
        None,
        False,
        {
            'recurrence_rule': schedule.to_data(defaults = False, start = start),
        },
    )
    
    yield (
        {
            'recurrence_rule': schedule.to_data(defaults = False, start = start),
        },
        timestamp,
        False,
        {
            'scheduled_start_time': datetime_to_timestamp(timestamp),
            'recurrence_rule': schedule.to_data(defaults = False, start = start),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_start_with_pass_to_schedule_start(initial_data, input_value, defaults):
    """
    Tests whether ``put_start_with_pass_to_schedule_start`` works as intended.
    
    Parameters
    ----------
    initial_data : `dict<str, object>`
        Initial data to serialise into.
    
    input_value : `None | DateTime`
        Value to serialize.
    
    defaults : `bool`
        Whether fields with their default values should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_start_with_pass_to_schedule_start(input_value, deep_copy(initial_data), defaults)
