import vampytest

from ...soundboard_sound import SoundboardSound

from ..soundboard_sounds_event import SoundboardSoundsEvent


def test__SoundboardSoundsEvent__repr():
    """
    Tests whether ``SoundboardSoundsEvent.__repr__`` works as intended.
    """
    guild_id = 202305270009
    sounds = [SoundboardSound.precreate(202305270010), SoundboardSound.precreate(202305270011)]
    
    soundboard_sounds_event = SoundboardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    
    vampytest.assert_instance(repr(soundboard_sounds_event), str)


def test__SoundboardSoundsEvent__eq():
    """
    Tests whether ``SoundboardSoundsEvent.__repr__`` works as intended.
    """
    guild_id = 202305270012
    sounds = [SoundboardSound.precreate(202305270013), SoundboardSound.precreate(202305270014)]
    
    keyword_parameters = {
        'guild_id': guild_id,
        'sounds': sounds,
    }
    
    soundboard_sounds_event_original = SoundboardSoundsEvent(**keyword_parameters)
    
    vampytest.assert_eq(soundboard_sounds_event_original, soundboard_sounds_event_original)
    
    for field_name, field_value in (
        ('guild_id', 0),
        ('sounds', None),
    ):
        soundboard_sounds_event_altered = SoundboardSoundsEvent(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(soundboard_sounds_event_original, soundboard_sounds_event_altered)


def test__SoundboardSoundsEvent__hash():
    """
    Tests whether ``SoundboardSoundsEvent.__hash__`` works as intended.
    """
    guild_id = 202305270015
    sounds = [SoundboardSound.precreate(202305270016), SoundboardSound.precreate(202305270017)]
    
    soundboard_sounds_event = SoundboardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    
    vampytest.assert_instance(hash(soundboard_sounds_event), int)


def test__SoundboardSoundsEvent__unpack():
    """
    Tests whether ``SoundboardSoundsEvent`` unpacking works as intended.
    """
    guild_id = 202305270018
    sounds = [SoundboardSound.precreate(202305270019), SoundboardSound.precreate(202305270020)]
    
    soundboard_sounds_event = SoundboardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    
    vampytest.assert_eq(len([*soundboard_sounds_event]), len(soundboard_sounds_event))
