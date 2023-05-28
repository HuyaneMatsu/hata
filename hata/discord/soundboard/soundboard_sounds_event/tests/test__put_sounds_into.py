import vampytest

from ...soundboard_sound import SoundboardSound

from ..fields import put_sounds_into


def test__put_sounds_into():
    """
    Tests whether ``put_sounds_into`` works as intended.
    """
    sound_id_0 = 202305260005
    sound_name_0 = 'Far'
    
    sound_id_1 = 202305260006
    sound_name_1 = 'East'
    
    sound_0 = SoundboardSound.precreate(
        sound_id_0,
        name = sound_name_0,
    )
    
    sound_1 = SoundboardSound.precreate(
        sound_id_1,
        name = sound_name_1,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {'soundboard_sounds': []}),
        (None, True, {'soundboard_sounds': []}),
        (
            (sound_0, sound_1),
            False,
            {
                'soundboard_sounds': [
                    sound_0.to_data(defaults = False, include_internals = True),
                    sound_1.to_data(defaults = False, include_internals = True),
                ],
            },
        ),
        (
            (sound_0, sound_1),
            True,
            {
                'soundboard_sounds': [
                    sound_0.to_data(defaults = True, include_internals = True),
                    sound_1.to_data(defaults = True, include_internals = True),
                ],
            },
        ),
    ):
        output = put_sounds_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
