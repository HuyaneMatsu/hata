import vampytest

from ....scheduled_event import ScheduledEvent

from ..guild import Guild

from ..fields import parse_scheduled_events


def _iter_options():
    scheduled_event_id = 202306110000
    guild_id = 202306110005
    scheduled_event_name = 'Koishi'
    
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
        name = scheduled_event_name,
    )
    
    yield {}, 202306110001, None
    yield {'guild_scheduled_events': []}, 202306110004, None
    yield (
        {'guild_scheduled_events': [scheduled_event.to_data(defaults = True, include_internals = True)]},
        guild_id,
        {scheduled_event_id: scheduled_event},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_scheduled_events(input_value, guild_id):
    """
    Tests whether ``parse_scheduled_events`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    guild_id : `int`
        The guild's identifier we are populating its scheduled events of.
    
    Returns
    -------
    output : `None | dict<int, ScheduledEvent>`
    """
    guild = Guild.precreate(guild_id)
    
    return parse_scheduled_events(input_value, guild.scheduled_events)
