__all__ = (
    'Button', 'ButtonStyle', 'ChannelSelect', 'Form', 'MentionableSelect', 'Option', 'RoleSelect', 'Row', 'Select',
    'StringSelect', 'TextInput', 'TextInputStyle', 'UserSelect'
)

from ...discord.component import (
    ButtonStyle, InteractionForm as Form, StringSelectOption as Option, TextInputStyle, create_button as Button,
    create_channel_select as ChannelSelect, create_mentionable_select as MentionableSelect,
    create_role_select as RoleSelect, create_row as Row, create_string_select as Select,
    create_string_select as StringSelect, create_text_input as TextInput, create_user_select as UserSelect
)
from ...discord.core import APPLICATION_ID_TO_CLIENT
from ...discord.exceptions import DiscordException, ERROR_CODES


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
    except GeneratorExit:
        raise
    
    except BaseException as err:
        if isinstance(err, ConnectionError):
            # No Internet connection
            return
        
        if isinstance(err, DiscordException) and (err.code == ERROR_CODES.unknown_interaction):
            # We timed out, bad connection.
            return
        
        await client.events.error(client, f'acknowledge_component_interaction', err)
