import vampytest

from ....user import VoiceState

from ..fields import validate_voice_states


def test__validate_voice_states__0():
    """
    Tests whether ``validate_voice_states`` works as intended.
    
    Case: passing.
    """
    user_id = 202306150021
    channel_id = 202306150021
    guild_id = 202306150022
    
    voice_state = VoiceState(
        user_id = user_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    for input_value, expected_output in (
        (None, {}),
        ([], {}),
        ({}, {}),
        ([voice_state], {user_id: voice_state}),
        ({user_id: voice_state}, {user_id: voice_state}),
    ):
        output = validate_voice_states(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_voice_states__1():
    """
    Tests whether ``validate_voice_states`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_voice_states(input_value)
