import vampytest

from ...soundboard_sound import SoundBoardSound

from ..fields import validate_sounds


def test__validate_sounds__0():
    """
    Validates whether ``validate_sounds`` works as intended.
    
    Case: passing.
    """
    sound_id_0 = 202305260007
    sound_id_1 = 202305260008
    
    sound_0 = SoundBoardSound.precreate(sound_id_0)
    sound_1 = SoundBoardSound.precreate(sound_id_1)
    
    for input_value, expected_output in (
        ([], None),
        ([sound_0], (sound_0,)),
        ([sound_1, sound_0], (sound_0, sound_1)),
    ):
        output = validate_sounds(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_sounds__1():
    """
    Validates whether ``validate_sounds`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_sounds(input_value)
