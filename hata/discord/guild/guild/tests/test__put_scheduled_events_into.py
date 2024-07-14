import vampytest

from ....scheduled_event import ScheduledEvent

from ..fields import put_scheduled_events_into


def _iter_options():
    scheduled_event_id = 202306110002
    scheduled_event_name = 'Koishi'
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        name = scheduled_event_name,
    )
    
    yield None, False, {'guild_scheduled_events': []}
    yield None, True, {'guild_scheduled_events': []}
    yield (
        {scheduled_event_id: scheduled_event},
        False,
        {'guild_scheduled_events': [scheduled_event.to_data(defaults = False, include_internals = True)]},
    )
    yield (
        {scheduled_event_id: scheduled_event},
        True,
        {'guild_scheduled_events': [scheduled_event.to_data(defaults = True, include_internals = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_scheduled_events_into(input_value, defaults):
    """
    Tests whether ``put_scheduled_events_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, ScheduledEvent>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_scheduled_events_into(input_value, {}, defaults)
