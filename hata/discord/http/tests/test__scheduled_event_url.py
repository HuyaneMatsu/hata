import vampytest

from ...scheduled_event import ScheduledEvent
from ...utils import is_url

from ..urls import DISCORD_ENDPOINT, scheduled_event_url


def _iter_options():
    scheduled_event_id = 202504180020
    guild_id = 202504180021
    yield (
        scheduled_event_id,
        guild_id,
        f'{DISCORD_ENDPOINT}/events/{guild_id}/{scheduled_event_id}',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__scheduled_event_url(scheduled_event_id, guild_id):
    """
    Tests whether ``scheduled_event_url`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        ScheduledEvent identifier.
    
    guild_id : `int`
        Scheduled event's guild's identifier.
    
    Returns
    -------
    output : `None | str`
    """
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id, guild_id = guild_id)
    
    output = scheduled_event_url(scheduled_event)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
