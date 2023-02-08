__all__ = ()

from scarletio import export, include

from ...core import GUILDS

Guild = include('Guild')


@export
def _try_get_guild_id(guild):
    """
    Tries to get the guild's identifier.
    
    Parameters
    ----------
    guild : `None`, `int`, ``Guild``
        The guild or it's identifier.
    
    Returns
    -------
    guild_id : `int`
        The guild's identifier. Defaults to `0`.
    """
    if isinstance(guild, int):
        guild_id = guild
    elif guild is None:
        guild_id = 0
    elif isinstance(guild, Guild):
        guild_id = guild.id
    else:
        guild_id = 0
    
    return guild_id


def _try_get_guild_and_id(guild):
    """
    Tries to get the guild and it's identifier.
    
    Parameters
    ----------
    guild : `None`, `int`, ``Guild``
        The guild or it's identifier.
    
    Returns
    -------
    guild : `None`, ``Guild``
        The guild if found.
    guild_id : `int`
        The guild's identifier. Defaults to `0`.
    """
    if isinstance(guild, int):
        guild_id = guild
        guild = GUILDS.get(guild_id)
    elif guild is None:
        guild_id = 0
    elif isinstance(guild, Guild):
        guild_id = guild.id
    else:
        guild_id = 0
        guild = None
    
    return guild, guild_id
