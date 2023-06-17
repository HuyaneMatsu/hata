import vampytest

from ....user import VoiceState

from ..fields import put_voice_states_into


def iter_options():
    user_id = 202306150018
    channel_id = 202306150019
    guild_id = 202306150020
    
    voice_state = VoiceState(
        user_id = user_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    yield {}, True, {'voice_states': []}
    yield {user_id: voice_state}, True, {'voice_states': [voice_state.to_data(defaults = True)]}


@vampytest._(vampytest.call_from(iter_options()).returning_last())
def test__put_voice_states_into(input_value, defaults):
    """
    Tests whether ``put_voice_states_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<int, VoiceState>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_voice_states_into(input_value, {}, defaults)
