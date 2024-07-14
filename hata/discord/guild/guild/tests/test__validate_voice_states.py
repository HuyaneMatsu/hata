import vampytest

from ....user import VoiceState

from ..fields import validate_voice_states


def _iter_options__passing():
    user_id = 202306150021
    channel_id = 202306150021
    guild_id = 202306150022
    
    voice_state = VoiceState(
        user_id = user_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    yield None, None
    yield [], None
    yield {}, None
    yield [voice_state], {user_id: voice_state}
    yield {user_id: voice_state}, {user_id: voice_state}


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {12.6}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_voice_states(input_value):
    """
    Tests whether ``validate_voice_states`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<int, VoiceState>`
    
    Raises
    ------
    TypeError
    """
    output = validate_voice_states(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
