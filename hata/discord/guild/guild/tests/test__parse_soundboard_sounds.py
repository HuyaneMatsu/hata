import vampytest

from ....soundboard import SoundboardSound

from ..fields import parse_soundboard_sounds
from ..guild import Guild


def _iter_options():
    sound_id = 202409210000
    guild_id = 202409210001
    name = 'aaaa'
    
    soundboard_sound = SoundboardSound.precreate(
        sound_id,
        guild_id = guild_id,
        name = name,
    )
    
    yield {}, guild_id, None
    yield {'soundboard_sounds': []}, guild_id, None
    yield (
        {'soundboard_sounds': [soundboard_sound.to_data(include_internals = True)]},
        guild_id,
        {sound_id: soundboard_sound},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_soundboard_sounds(input_data, guild_id):
    """
    Tests whether ``parse_soundboard_sounds`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to pass.
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | dict<int, SoundboardSound>`
    """
    guild = Guild.precreate(guild_id)
    return parse_soundboard_sounds(input_data, guild.soundboard_sounds)
