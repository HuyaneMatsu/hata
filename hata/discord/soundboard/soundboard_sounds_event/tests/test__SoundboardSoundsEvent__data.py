import vampytest

from ....guild import Guild

from ...soundboard_sound import SoundboardSound

from ..soundboard_sounds_event import SoundboardSoundsEvent

from .test__SoundboardSoundsEvent__constructor import _assert_fields_set


def test__SoundboardSoundsEvent__from_data__0():
    """
    Tests whether ``SoundboardSoundsEvent.from_data`` works as intended.
    
    Case: all fields given.
    """
    guild_id = 202305270003
    sounds = [SoundboardSound.precreate(202305270004), SoundboardSound.precreate(202305270005)]
    
    data = {
        'guild_id': str(guild_id),
        'soundboard_sounds': [sound.to_data(defaults = True, include_internals = True) for sound in sounds],
    }
    
    soundboard_sounds_event = SoundboardSoundsEvent.from_data(data)
    _assert_fields_set(soundboard_sounds_event)
    
    vampytest.assert_eq(soundboard_sounds_event.guild_id, guild_id)
    vampytest.assert_eq(soundboard_sounds_event.sounds, tuple(sounds))


def test__SoundboardSoundsEvent__from_data__1():
    """
    Tests whether ``SoundboardSoundsEvent.from_data`` works as intended.
    
    Case: all fields given.
    """
    guild_id = 202305280010
    sound_id_0 = 202305280011
    sound_id_1 = 202305280012
    sound_0 = SoundboardSound.precreate(sound_id_0, guild_id = guild_id)
    sound_1 = SoundboardSound.precreate(sound_id_1, guild_id = guild_id)
    sounds = [sound_0, sound_1]
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'guild_id': str(guild_id),
        'soundboard_sounds': [sound.to_data(defaults = True, include_internals = True) for sound in sounds],
    }
    
    SoundboardSoundsEvent.from_data(data)
    
    vampytest.assert_true(guild.soundboard_sounds_cached)
    vampytest.assert_eq(guild.soundboard_sounds, {sound_id_0: sound_0, sound_id_1: sound_1})


def test__SoundboardSoundsEvent__to_data__0():
    """
    Tests whether ``SoundboardSoundsEvent.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    guild_id = 202305270006
    sounds = [SoundboardSound.precreate(202305270007), SoundboardSound.precreate(202305270008)]
    
    soundboard_sounds_event = SoundboardSoundsEvent(
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
