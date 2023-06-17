__all__ = ()

from ...core import GUILDS


def _add_embedded_activity_state_to_guild_cache(embedded_activity_state):
    """
    Adds the embedded activity to it's guild.
    
    Parameters
    ----------
    embedded_activity_state : ``EmbeddedActivityState``
        The embedded activity to add to it's guild's cache.
    """
    try:
        guild = GUILDS[embedded_activity_state.guild_id]
    except KeyError:
        pass
    else:
        embedded_activity_states = guild.embedded_activity_states
        if (embedded_activity_states is None):
            embedded_activity_states = set()
            guild.embedded_activity_states = embedded_activity_states
        
        embedded_activity_states.add(embedded_activity_state)


def _remove_embedded_activity_state_from_guild_cache(embedded_activity_state):
    """
    Adds the embedded activity to it's guild.
    
    Parameters
    ----------
    embedded_activity_state : ``EmbeddedActivityState``
        The embedded activity to add to it's guild's cache.
    """
    try:
        guild = GUILDS[embedded_activity_state.guild_id]
    except KeyError:
        pass
    else:
        embedded_activity_states = guild.embedded_activity_states
        if (embedded_activity_states is not None):
            try:
                embedded_activity_states.remove(embedded_activity_state)
            except KeyError:
                pass
            else:
                if not embedded_activity_state:
                    guild.embedded_activity_states = None
