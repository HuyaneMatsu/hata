from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..fields import parse_occasion_overwrites


def _iter_options():
    occasion_overwrite_0 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    occasion_overwrite_1 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 15, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506210030
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'guild_scheduled_event_exceptions': None,
        },
        None,
    )
    
    yield (
        {
            'guild_scheduled_event_exceptions': [],
        },
        None,
    )
    
    yield (
        {
            'guild_scheduled_event_exceptions': [
                {
                    "event_id": str(scheduled_event_id),
                    **occasion_overwrite_0.to_data(defaults = False, include_internals = True),
                }, {
                    "event_id": str(scheduled_event_id),
                    **occasion_overwrite_1.to_data(defaults = False, include_internals = True),
                },
            ],
        },
        (occasion_overwrite_0, occasion_overwrite_1),
    )
    
    yield (
        {
            'guild_scheduled_event_exceptions': [
                {
                    "event_id": str(scheduled_event_id),
                    **occasion_overwrite_1.to_data(defaults = False, include_internals = True),
                }, {
                    "event_id": str(scheduled_event_id),
                    **occasion_overwrite_0.to_data(defaults = False, include_internals = True),
                }
            ],
        },
        (occasion_overwrite_0, occasion_overwrite_1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_occasion_overwrites(input_data):
    """
    Tests whether ``parse_occasion_overwrites`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<ScheduledEventOccasionOverwrite>``
    """
    output = parse_occasion_overwrites(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ScheduledEventOccasionOverwrite)
    
    return output
