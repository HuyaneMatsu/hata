import vampytest

from ...soundboard_sound import SoundBoardSound

from ..soundboard_sounds_event import SoundBoardSoundsEvent


def test__SoundBoardSoundsEvent__repr():
    """
    Tests whether ``SoundBoardSoundsEvent.__repr__`` works as intended.
    """
    guild_id = 202305270009
    sounds = [SoundBoardSound.precreate(202305270010), SoundBoardSound.precreate(202305270011)]
    
    soundboard_sounds_event = SoundBoardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    
    vampytest.assert_instance(repr(soundboard_sounds_event), str)


def test__SoundBoardSoundsEvent__eq():
    """
    Tests whether ``SoundBoardSoundsEvent.__repr__`` works as intended.
    """
    guild_id = 202305270012
    sounds = [SoundBoardSound.precreate(202305270013), SoundBoardSound.precreate(202305270014)]
    
    keyword_parameters = {
        'guild_id': guild_id,
        'sounds': sounds,
    }
    
    soundboard_sounds_event_original = SoundBoardSoundsEvent(**keyword_parameters)
    
    vampytest.assert_eq(soundboard_sounds_event_original, soundboard_sounds_event_original)
    
    for field_name, field_value in (
        ('guild_id', 0),
        ('sounds', None),
    ):
        soundboard_sounds_event_altered = SoundBoardSoundsEvent(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(soundboard_sounds_event_original, soundboard_sounds_event_altered)


def test__SoundBoardSoundsEvent__hash():
    """
    Tests whether ``SoundBoardSoundsEvent.__hash__`` works as intended.
    """
    guild_id = 202305270015
    sounds = [SoundBoardSound.precreate(202305270016), SoundBoardSound.precreate(202305270017)]
    
    soundboard_sounds_event = SoundBoardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    
    vampytest.assert_instance(hash(soundboard_sounds_event), int)


def test__SoundBoardSoundsEvent__unpack():
    """
    Tests whether ``SoundBoardSoundsEvent`` unpacking works as intended.
    """
    guild_id = 202305270018
    sounds = [SoundBoardSound.precreate(202305270019), SoundBoardSound.precreate(202305270020)]
    
    soundboard_sounds_event = SoundBoardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    
    vampytest.assert_eq(len([*soundboard_sounds_event]), len(soundboard_sounds_event))
