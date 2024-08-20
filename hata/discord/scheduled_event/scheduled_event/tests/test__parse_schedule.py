from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...schedule import Schedule

from ..fields import parse_schedule


def _iter_options():
    schedule = Schedule(occurrence_spacing = 2, start = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    
    yield (
        {},
        None
    )
    
    yield (
        {
            'recurrence_rule': None,
        },
        None,
    )
    
    yield (
        {
            'recurrence_rule': schedule.to_data(),
        },
        schedule,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_schedule(input_data):
    """
    Tests whether ``parse_schedule`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | Schedule`
    """
    output = parse_schedule(input_data)
    vampytest.assert_instance(output, Schedule, nullable = True)
    return output
