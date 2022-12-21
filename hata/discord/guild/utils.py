__all__ = ('create_partial_guild_from_data', 'create_partial_guild_from_id')

from scarletio import export

from ..core import GUILDS

from .fields import parse_features
from .guild import Guild
from .preinstanced import VerificationLevel


# We need to ignore client adding, because clients count to being not partial.
# If a guild is not partial it wont get update on Guild.__new__

def create_partial_guild_from_data(data):
    """
    Creates a partial guild from partial guild data.
    
    Parameters
    ----------
    data : `None`, `dict` of (`str`, `Any`) items
        Partial channel data received from Discord.
    
    Returns
    -------
    channel : `None`, ``Guild``
        The created partial guild, or `None`, if no data was received.
    """
    if (data is None) or (not data):
        return None
    guild_id = int(data['id'])
    try:
        return GUILDS[guild_id]
    except KeyError:
        pass
    
    guild = Guild._create_empty(guild_id)
    GUILDS[guild_id] = guild
    
    # do not use pop, at later versions the received data might be read-only.
    try:
        available = not data['unavailable']
    except KeyError:
        available = True
    
    guild.available = available
    
    guild.name = data.get('name', '')
    guild._set_icon(data)
    guild._set_invite_splash(data)
    guild._set_discovery_splash(data)
    guild.description = data.get('description', None)
    
    try:
        verification_level = data['verification_level']
    except KeyError:
        pass
    else:
        guild.verification_level = VerificationLevel.get(verification_level)
    
    features = parse_features(data)
    if (features is not None):
        guild.features = features
    
    return guild


@export
def create_partial_guild_from_id(guild_id):
    """
    Creates a guild from the given identifier and stores it in the cache as well. If the guild already exists,
    returns that instead.
    
    Parameters
    ----------
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    guild : ``Guild``
        The created guild instance.
    """
    try:
        guild = GUILDS[guild_id]
    except KeyError:
        guild = Guild._create_empty(guild_id)
        GUILDS[guild_id] = guild
    
    return guild
