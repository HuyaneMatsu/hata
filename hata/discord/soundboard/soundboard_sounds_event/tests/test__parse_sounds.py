import vampytest

from ...soundboard_sound import SoundBoardSound

from ..fields import parse_sounds


def test__parse_sounds():
    """
    Tests whether ``parse_sounds`` works as intended.
    """
    sound_id_0 = 202305260003
    sound_name_0 = 'Far'
    
    sound_id_1 = 202305260004
    sound_name_1 = 'East'
    
    sound_0 = SoundBoardSound.precreate(
        sound_id_0,
        name = sound_name_0,
    )
    
    sound_1 = SoundBoardSound.precreate(
        sound_id_1,
        name = sound_name_1,
    )
    
    for input_data, expected_output in (
        ({}, None),
        ({'soundboard_sounds': None}, None),
        ({'soundboard_sounds': []}, None),
        (
            {
                'soundboard_sounds': [
                    sound_0.to_data(include_internals = True),
                ],
            },
            (sound_0,),
        ),
        (
            {
                'soundboard_sounds': [
                    sound_0.to_data(include_internals = True),
                    sound_1.to_data(include_internals = True),
                ],
            },
            (sound_0, sound_1),
        ),
    ):
        output = parse_sounds(input_data)
        vampytest.assert_eq(output, expected_output)
