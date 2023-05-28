import vampytest

from ...soundboard import SoundboardSound
from ...utils import is_url

from ..urls import soundboard_sound_url


def test__soundboard_sound_url():
    """
    Tests whether ``soundboard_sound_url`` works as intended.
    """
    sound_id = 202305240053
    
    sound = SoundboardSound.precreate(sound_id)
    output = soundboard_sound_url(sound)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_true(is_url(output))
    vampytest.assert_in(str(sound_id), output)
