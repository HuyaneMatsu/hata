import vampytest

from ....scheduled_event import ScheduledEvent

from ..fields import put_scheduled_events_into


def _iter_options():
    scheduled_event_id_0 = 202406250010
    scheduled_event_id_1 = 202406250011
    
    scheduled_event_0 = ScheduledEvent.precreate(scheduled_event_id_0)
    scheduled_event_1 = ScheduledEvent.precreate(scheduled_event_id_1)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'guild_scheduled_events': [],
        },
    )
    
    yield (
        {
            scheduled_event_id_0: scheduled_event_0,
            scheduled_event_id_1: scheduled_event_1,
        },
        False,
        {
            'guild_scheduled_events': [
                scheduled_event_0.to_data(defaults = False, include_internals = True),
                scheduled_event_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        {
            scheduled_event_id_0: scheduled_event_0,
            scheduled_event_id_1: scheduled_event_1,
        },
        True,
        {
            'guild_scheduled_events': [
                scheduled_event_0.to_data(defaults = True, include_internals = True),
                scheduled_event_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_scheduled_events_into(input_value, defaults):
    """
    Tests whether ``put_scheduled_events_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, ScheduledEvent>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_scheduled_events_into(input_value, {}, defaults)
