import vampytest

from ...soundboard_sound import SoundBoardSound

from ..soundboard_sounds_event import SoundBoardSoundsEvent

from .test__SoundBoardSoundsEvent__constructor import _assert_fields_set


def test__SoundBoardSoundsEvent__from_data__0():
    """
    Tests whether ``SoundBoardSoundsEvent.from_data`` works as intended.
    
    Case: all soundboard_sounds_events given.
    """
    guild_id = 202305270003
    sounds = [SoundBoardSound.precreate(202305270004), SoundBoardSound.precreate(202305270005)]
    
    data = {
        'guild_id': str(guild_id),
        'soundboard_sounds': [sound.to_data(defaults = True, include_internals = True) for sound in sounds],
    }
    
    soundboard_sounds_event = SoundBoardSoundsEvent.from_data(data)
    _assert_fields_set(soundboard_sounds_event)
    
    vampytest.assert_eq(soundboard_sounds_event.guild_id, guild_id)
    vampytest.assert_eq(soundboard_sounds_event.sounds, tuple(sounds))


def test__SoundBoardSoundsEvent__to_data__0():
    """
    Tests whether ``SoundBoardSoundsEvent.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    guild_id = 202305270006
    sounds = [SoundBoardSound.precreate(202305270007), SoundBoardSound.precreate(202305270008)]
    
    soundboard_sounds_event = SoundBoardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    
    expected_output = {
        'guild_id': str(guild_id),
        'soundboard_sounds': [sound.to_data(defaults = True, include_internals = True) for sound in sounds],
    }
    
    vampytest.assert_eq(
        soundboard_sounds_event.to_data(defaults = True),
        expected_output,
    )
