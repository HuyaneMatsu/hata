__all__ = ('create_partial_soundboard_sound_from_id', 'create_partial_soundboard_sound_from_partial_data')

from ...core import SOUNDBOARD_SOUNDS

from .fields import (
    parse_guild_id, parse_id, put_emoji_into, put_name_into, put_volume_into, validate_emoji, validate_name,
    validate_volume
)
from .soundboard_sound import SoundboardSound


SOUNDBOARD_SOUND_FIELD_CONVERTERS = {
    'emoji': (validate_emoji, put_emoji_into),
    'name': (validate_name, put_name_into),
    'volume': (validate_volume, put_volume_into),
}


def create_partial_soundboard_sound_from_id(sound_id, guild_id = 0):
    """
    Creates a partial soundboard sound from the given `sound_id`. If the sound already exists returns that instead.
    
    Parameters
    ----------
    sound_id : `int`
        The unique identifier number of the sound.
    guild_id : `int` = `0`, Optional
        The sound's guild's identifier.
    
    Returns
    -------
    sound : ``SoundboardSound``
    """
    try:
        sound = SOUNDBOARD_SOUNDS[sound_id]
    except KeyError:
        sound = SoundboardSound._create_empty(sound_id, guild_id)
        SOUNDBOARD_SOUNDS[sound_id] = sound
    
    return sound


def create_partial_soundboard_sound_from_partial_data(data):
    """
    Creates a soundboard instance from the given partial data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Soundboard data.
    
    Returns
    -------
    sound : ``SoundboardSound``
    """
    sound_id = parse_id(data)
    
    try:
        sound = SOUNDBOARD_SOUNDS[sound_id]
    except KeyError:
        sound = SoundboardSound._create_empty(sound_id, parse_guild_id(data))
        SOUNDBOARD_SOUNDS[sound_id] = sound
    
    return sound
