import vampytest

from ....soundboard import SoundboardSound

from ..fields import parse_soundboard_sounds


def _iter_options():
    soundboard_sound_id_0 = 202501290000
    soundboard_sound_name_0 = 'Divine'
    
    soundboard_sound_id_1 = 202501290001
    soundboard_sound_name_1 = 'Lotus'
    
    soundboard_sound_0 = SoundboardSound.precreate(
        soundboard_sound_id_0,
        name = soundboard_sound_name_0,
    )
    
    soundboard_sound_1 = SoundboardSound.precreate(
        soundboard_sound_id_1,
        name = soundboard_sound_name_1,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'soundboard_sounds': None,
        },
        None,
    )
    
    yield (
        {
            'soundboard_sounds': [],
        },
        None,
    )
    
    yield (
        {
            'soundboard_sounds': [
                soundboard_sound_0.to_data(include_internals = True),
            ],
        },
        (soundboard_sound_0,),
    )
    
    yield (
        {
            'soundboard_sounds': [
                soundboard_sound_0.to_data(include_internals = True),
                soundboard_sound_1.to_data(include_internals = True),
            ],
        },
        (soundboard_sound_0, soundboard_sound_1),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_soundboard_sounds(input_data):
    """
    Tests whether ``parse_soundboard_sounds`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<SoundboardSound>`
    """
    output = parse_soundboard_sounds(input_data)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, SoundboardSound)
        
    return output
