__all__ = ()

from ..channel import VoiceRegion
from ..core import CHANNELS


def try_get_voice_region(guild_id, channel_id):
    """
    Tries to get the voice region of the given channel and guild's id-s.
    
    Parameters
    ----------
    guild_id : `int`
        The respective guild's identifier.
    channel_id : `int`
        The respective channel's identifier.
    
    Returns
    -------
    region : ``VoiceRegion``
    """
    try:
        channel = CHANNELS[channel_id]
    except KeyError:
        region = VoiceRegion.unknown
    else:
        region = channel.region
    
    return region
