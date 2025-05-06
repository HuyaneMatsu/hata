import vampytest

from ....user import VoiceState

from ..fields import put_voice_states


def _iter_options():
    user_id = 202306150018
    channel_id = 202306150019
    guild_id = 202306150020
    
    voice_state = VoiceState(
        user_id = user_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    yield None, False, {'voice_states': []}
    yield None, True, {'voice_states': []}
    yield {user_id: voice_state}, False, {'voice_states': [voice_state.to_data(defaults = False)]}
    yield {user_id: voice_state}, True, {'voice_states': [voice_state.to_data(defaults = True)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_voice_states(input_value, defaults):
    """
    Tests whether ``put_voice_states`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, VoiceState>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_voice_states(input_value, {}, defaults)
