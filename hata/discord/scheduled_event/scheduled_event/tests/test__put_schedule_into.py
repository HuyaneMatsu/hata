from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...schedule import Schedule

from ..fields import put_schedule_into


def _iter_options():
    schedule = Schedule(occurrence_spacing = 2)
    start_0 = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    start_1 = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    
    yield (
        None,
        False,
        start_0,
        {},
    )
    
    yield (
        None,
        True,
        start_0,
        {
            'recurrence_rule': None,
        },
    )
    
    yield (
        schedule,
        False,
        start_0,
        {
            'recurrence_rule': schedule.to_data(defaults = False, start = start_0),
        },
    )
    
    yield (
        schedule,
        True,
        start_0,
        {
            'recurrence_rule': schedule.to_data(defaults = True, start = start_0),
        },
    )
    
    yield (
        schedule.copy_with(start = start_1),
        True,
        start_0,
        {
            'recurrence_rule': schedule.to_data(defaults = True, start = start_1),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_schedule_into(input_value, defaults, start):
    """
    Tests whether ``put_schedule_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Schedule`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    start : `None | DateTime`
        Alternative start to use if `.start` is not present.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_schedule_into(input_value, {}, defaults, start = start)
