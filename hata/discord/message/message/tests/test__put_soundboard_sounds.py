import vampytest

from ....soundboard import SoundboardSound

from ..fields import put_soundboard_sounds


def _iter_options():
    soundboard_sound_id_0 = 202501290002
    soundboard_sound_name_0 = 'Divine'
    
    soundboard_sound_id_1 = 202501290003
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
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'soundboard_sounds': [],
        },
    )
    
    yield (
        (soundboard_sound_0, soundboard_sound_1),
        False,
        {
            'soundboard_sounds': [
                soundboard_sound_0.to_data(defaults = False, include_internals = True),
                soundboard_sound_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        (soundboard_sound_0, soundboard_sound_1),
        True,
        {
            'soundboard_sounds': [
                soundboard_sound_0.to_data(defaults = True, include_internals = True),
                soundboard_sound_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_soundboard_sounds(input_value, defaults):
    """
    Tests whether ``put_soundboard_sounds`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<SoundboardSound>``
        Value to serialize.
    
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_soundboard_sounds(input_value, {}, defaults)
