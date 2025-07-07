from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..scheduled_event_occasion_overwrite_create_event import ScheduledEventOccasionOverwriteCreateEvent


def test__ScheduledEventOccasionOverwriteCreateEvent__repr():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.__repr__`` works as intended.
    """
    guild_id = 202506220016
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220017
    
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = guild_id,
        occasion_overwrite = occasion_overwrite,
        scheduled_event_id = scheduled_event_id,
    )
    
    vampytest.assert_instance(repr(event), str)


def test__ScheduledEventOccasionOverwriteCreateEvent__hash():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.__hash__`` works as intended.
    """
    guild_id = 202506220018
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220019
    
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = guild_id,
        occasion_overwrite = occasion_overwrite,
        scheduled_event_id = scheduled_event_id,
    )
    
    vampytest.assert_instance(hash(event), int)


def _iter_options__eq():
    guild_id = 202506220020
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220021
    
    keyword_parameters = {
        'guild_id': guild_id,
        'occasion_overwrite': occasion_overwrite,
        'scheduled_event_id': scheduled_event_id,
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
            'guild_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'occasion_overwrite': ScheduledEventOccasionOverwrite(
                timestamp = DateTime(2016, 5, 16, 13, 0, 0, tzinfo = TimeZone.utc),
            ),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 0,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduledEventOccasionOverwriteCreateEvent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent.__eq__`` works as intended.
    
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
    event_0 = ScheduledEventOccasionOverwriteCreateEvent(**keyword_parameters_0)
    event_1 = ScheduledEventOccasionOverwriteCreateEvent(**keyword_parameters_1)
    
    output = event_0 == event_1
    vampytest.assert_instance(output, bool)
    return output


def test__ScheduledEventOccasionOverwriteCreateEvent__unpack():
    """
    Tests whether ``ScheduledEventOccasionOverwriteCreateEvent`` unpacking works as intended.
    """
    guild_id = 202506220022
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    scheduled_event_id = 202506220023
    
    event = ScheduledEventOccasionOverwriteCreateEvent(
        guild_id = guild_id,
        occasion_overwrite = occasion_overwrite,
        scheduled_event_id = scheduled_event_id,
    )
    
    vampytest.assert_eq(len([*event]), len(event))
