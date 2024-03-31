import vampytest

from ....activity import Activity, ActivityType

from ...embedded_activity_state import EmbeddedActivityState

from ..fields import parse_embedded_activity_states
from ..guild import Guild



def _iter_options():
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202306160015)
    channel_id = 202306160016
    guild_id = 202306160017
    user_ids = [202306160018, 202306160019]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    yield {}, guild_id, None
    yield {'embedded_activities': []}, guild_id, None
    yield (
        {'embedded_activities': [embedded_activity_state.to_data(defaults = True)]},
        guild_id,
        {embedded_activity_state},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_embedded_activity_states(input_value, guild_id):
    """
    Tests whether ``parse_embedded_activity_states`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    guild_id : `int`
        The guild's identifier we are populating its scheduled events of.
    
    Returns
    -------
    output : `None | dict<int, EmbeddedActivityState>`
    """
    guild = Guild.precreate(guild_id)
    
    return parse_embedded_activity_states(input_value, guild.embedded_activity_states)
