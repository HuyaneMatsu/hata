import vampytest

from ....soundboard import SoundboardSound

from ..fields import validate_soundboard_sounds


def _iter_options__passing():
    soundboard_sound_id_0 = 202501300004
    soundboard_sound_id_1 = 202501300005
    
    soundboard_sound_0 = SoundboardSound.precreate(soundboard_sound_id_0)
    soundboard_sound_1 = SoundboardSound.precreate(soundboard_sound_id_1)
    
    yield None, None
    yield [], None
    yield [soundboard_sound_0], (soundboard_sound_0,)
    yield [soundboard_sound_1, soundboard_sound_0], (soundboard_sound_0, soundboard_sound_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_soundboard_sounds(input_value):
    """
    Validates whether ``validate_soundboard_sounds`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<SoundboardSound>`
    
    Raises
    ------
    TypeError
    """
    output = validate_soundboard_sounds(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
