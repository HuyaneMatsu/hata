import vampytest

from ....soundboard import SoundboardSound

from ..fields import validate_soundboard_sounds


def test__validate_soundboard_sounds__0():
    """
    Tests whether ``validate_soundboard_sounds`` works as intended.
    
    Case: passing.
    """
    sound_id = 202305290008
    sound_name = 'Okuu'
    
    sound = SoundboardSound.precreate(
        sound_id,
        name = sound_name,
    )
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ({}, None),
        ([sound], {sound_id: sound}),
        ({sound_id: sound}, {sound_id: sound}),
    ):
        output = validate_soundboard_sounds(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_soundboard_sounds__1():
    """
    Tests whether ``validate_soundboard_sounds`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_soundboard_sounds(input_value)
