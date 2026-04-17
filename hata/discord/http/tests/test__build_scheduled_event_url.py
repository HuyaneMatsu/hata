import vampytest

from ..urls import DISCORD_ENDPOINT, build_scheduled_event_url


def _iter_options():
    scheduled_event_id = 202504180020
    guild_id = 202504180021
    
    yield (
        scheduled_event_id,
        guild_id,
        f'{DISCORD_ENDPOINT}/events/{guild_id}/{scheduled_event_id}',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_scheduled_event_url(scheduled_event_id, guild_id):
    """
    Tests whether ``build_scheduled_event_url`` works as intended.
    
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
    output = build_scheduled_event_url(guild_id, scheduled_event_id)
    vampytest.assert_instance(output, str, nullable = True)
    return output
