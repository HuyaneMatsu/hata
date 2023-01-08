__all__ = ()

from ...exceptions import DiscordException, ERROR_CODES


async def _delete_reaction_with_task(reaction_add_event, client):
    """
    Removes the given reaction event's emoji from it's message if applicable. Expected error codes are silenced.
    
    Parameters
    ----------
    reaction_add_event : ``ReactionAddEvent``, ``ReactionDeleteEvent``
        The respective reaction event.
    client : ``Client``
        The client who should remove the reaction if applicable.
    """
    try:
        await client.reaction_delete(reaction_add_event.message, reaction_add_event.emoji, reaction_add_event.user)
    except GeneratorExit:
        raise
    
    except BaseException as err:
        
        if isinstance(err, ConnectionError):
            # no internet
            return
        
        if isinstance(err, DiscordException):
            if err.code in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
            ):
                return
        
        await client.events.error(client, f'_delete_reaction_with_task called from {reaction_add_event!r}', err)
        return
