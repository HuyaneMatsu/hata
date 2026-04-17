import vampytest

from ..soundboard_sound import SoundboardSound
from ..utils import create_partial_soundboard_sound_from_id


def test__create_partial_soundboard_sound_from_id():
    """
    Tests whether ``create_partial_soundboard_sound_from_id`` works as intended.
    """
    sound_id = 202305240055
    guild_id = 202305240056
    
    soundboard_sound = create_partial_soundboard_sound_from_id(sound_id, guild_id)
    vampytest.assert_instance(soundboard_sound, SoundboardSound)
    
    vampytest.assert_eq(soundboard_sound.id, sound_id)
    vampytest.assert_eq(soundboard_sound.guild_id, guild_id)
    
    test_soundboard_sound = create_partial_soundboard_sound_from_id(sound_id, guild_id)
    vampytest.assert_is(soundboard_sound, test_soundboard_sound)
