import vampytest

from ..soundboard_sound import SoundBoardSound
from ..utils import create_partial_soundboard_sound_from_partial_data


def test__create_partial_soundboard_sound_from_partial_data():
    """
    Tests whether ``create_partial_soundboard_sound_from_partial_data`` works as intended.
    """
    sound_id = 202305250000
    guild_id = 202305250001
    
    data = {
        'sound_id': str(sound_id),
        'guild_id': str(guild_id),
    }
    
    soundboard_sound = create_partial_soundboard_sound_from_partial_data(data)
    vampytest.assert_instance(soundboard_sound, SoundBoardSound)
    
    vampytest.assert_eq(soundboard_sound.id, sound_id)
    vampytest.assert_eq(soundboard_sound.guild_id, guild_id)
    
    test_soundboard_sound = create_partial_soundboard_sound_from_partial_data(data)
    vampytest.assert_is(soundboard_sound, test_soundboard_sound)
