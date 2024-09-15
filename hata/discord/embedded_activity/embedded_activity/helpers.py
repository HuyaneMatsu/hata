__all__ = ()

from ...core import GUILDS


def _add_embedded_activity_to_guild_cache(embedded_activity):
    """
    Adds the embedded activity to it's guild.
    
    Parameters
    ----------
    embedded_activity : ``EmbeddedActivity``
        The embedded activity to add to it's guild's cache.
    """
    try:
        guild = GUILDS[embedded_activity.guild_id]
    except KeyError:
        pass
    else:
        embedded_activities = guild.embedded_activities
        if (embedded_activities is None):
            embedded_activities = set()
            guild.embedded_activities = embedded_activities
        
        embedded_activities.add(embedded_activity)


def _remove_embedded_activity_from_guild_cache(embedded_activity):
    """
    Adds the embedded activity to it's guild.
    
    Parameters
    ----------
    embedded_activity : ``EmbeddedActivity``
        The embedded activity to add to it's guild's cache.
    """
    try:
        guild = GUILDS[embedded_activity.guild_id]
    except KeyError:
        pass
    else:
        embedded_activities = guild.embedded_activities
        if (embedded_activities is not None):
            try:
                embedded_activities.remove(embedded_activity)
            except KeyError:
                pass
            else:
                if not embedded_activities:
                    guild.embedded_activities = None
