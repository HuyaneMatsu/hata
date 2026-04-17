import vampytest

from ....scheduled_event import ScheduledEvent

from ..fields import parse_scheduled_events


def _iter_options():
    scheduled_event_id_0 = 202406240013
    scheduled_event_id_1 = 202406240014
    
    scheduled_event_0 = ScheduledEvent.precreate(scheduled_event_id_0)
    scheduled_event_1 = ScheduledEvent.precreate(scheduled_event_id_1)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'guild_scheduled_events': [],
        },
        None,
    )
    
    yield (
        {
            'guild_scheduled_events': [
                scheduled_event_0.to_data(defaults = True, include_internals = True),
                scheduled_event_1.to_data(defaults = True, include_internals = True),
            ],
        },
        {
            scheduled_event_id_0: scheduled_event_0,
            scheduled_event_id_1: scheduled_event_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_scheduled_events(input_data):
    """
    Tests whether ``parse_scheduled_events`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `dict<int, ScheduledEvent>`
    """
    return parse_scheduled_events(input_data)
