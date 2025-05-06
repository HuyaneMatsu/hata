import vampytest

from ....soundboard import SoundboardSound

from ..fields import put_soundboard_sounds


def _iter_options():
    sound_id = 202409210002
    guild_id = 202409210003
    name = 'aaaa'
    
    soundboard_sound = SoundboardSound.precreate(
        sound_id,
        guild_id = guild_id,
        name = name,
    )
    
    yield None, False, {'soundboard_sounds': []}
    yield None, True, {'soundboard_sounds': []}
    yield (
        {sound_id: soundboard_sound},
        False,
        {'soundboard_sounds': [soundboard_sound.to_data(defaults = False, include_internals = True)]},
    )
    yield (
        {sound_id: soundboard_sound},
        True,
        {'soundboard_sounds': [soundboard_sound.to_data(defaults = True, include_internals = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_soundboard_sounds(input_value, defaults):
    """
    Tests whether ``put_soundboard_sounds`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, SoundboardSound>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_soundboard_sounds(input_value, {}, defaults)
