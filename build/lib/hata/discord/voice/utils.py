__all__ = ()

from ..core import CHANNELS, GUILDS

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
    region : `None` or ``VoiceRegion``
    """
    try:
        channel = CHANNELS[channel_id]
    except KeyError:
        region = None
    else:
        region = channel.region
        if region is None:
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                region = None
            else:
                region = guild.region
    
    return region
