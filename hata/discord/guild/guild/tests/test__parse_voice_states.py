import vampytest

from ....user import VoiceState

from ..fields import parse_voice_states
from ..guild import Guild


def iter_options():
    user_id = 202306150015
    channel_id = 202306150016
    guild_id = 202306150017
    
    
    voice_state = VoiceState(
        user_id = user_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    yield {}, guild_id, {}
    yield {'voice_states': []}, guild_id, {}
    yield (
        {'voice_states': [voice_state.to_data(defaults = True)]},
        guild_id,
        {user_id: voice_state},
    )


@vampytest._(vampytest.call_from(iter_options()).returning_last())
def test__parse_voice_states(input_data, guild_id):
    """
    Tests whether ``parse_voice_states`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to pass.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `dict<int, VoiceState>`
    """
    guild = Guild.precreate(guild_id)
    return parse_voice_states(input_data, guild.voice_states, guild_id)
