__all__ = ('Button', 'ButtonStyle', 'Row', 'Select', 'Option')

from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.core import APPLICATION_ID_TO_CLIENT

from ...discord.interaction import ComponentButton as Button, ComponentRow as Row, ComponentSelect as Select, \
    ComponentSelectOption as Option, ButtonStyle


async def acknowledge_component_interaction(interaction_event):
    """
    Acknowledges the given `interaction_event`. If error occurs, calls `client.events.error`.
    
    This function is a coroutine.
    
    Parameter
    ---------
    interaction_event : ``InteractionEvent``
        The component interaction event to acknowledge.
    """
    try:
        client = APPLICATION_ID_TO_CLIENT[interaction_event.application_id]
    except KeyError:
        return
        
    try:
        await client.interaction_component_acknowledge(interaction_event)
    except BaseException as err:
        if isinstance(err, ConnectionError):
            # No Internet connection
            return
        
        if isinstance(err, DiscordException) and (err.code == ERROR_CODES.unknown_interaction):
            # We timed out, bad connection.
            return
        
        await client.events.error(client, f'acknowledge_component_interaction', err)
