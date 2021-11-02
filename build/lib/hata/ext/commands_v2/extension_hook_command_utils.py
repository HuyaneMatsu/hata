__all__ = ()

from ...discord.events.handling_helpers import asynclist
from ...discord.events.core import DEFAULT_EVENT_HANDLER

from ...ext.command_utils import MessageCreateWaitfor

from . import EXTENSION_SETUP_HOOKS
from .command_processor import CommandProcessor


def extension_setup_hook(client, command_processor):
    """
    Hook to merge `command_utils`'s `message_create` event with the command processor.
    
    Attributes
    ----------
    client : ``Client``
        The client the extension is setup.
    command_processor : ``CommandProcessor``
        The create command processor instance.
    
    Raises
    ------
    RuntimeError
        If the client already has a ``CommandProcessor` added to it.
    """
    event_message_create = client.events.message_create
    if (event_message_create is DEFAULT_EVENT_HANDLER):
        event = None
    elif type(event_message_create) is asynclist:
        for event in list.__iter__(event_message_create):
            if isinstance(event, CommandProcessor):
                raise RuntimeError(f'The client already has a `{CommandProcessor.__name__}` instance added as '
                    f'event.')
            
            if isinstance(event, MessageCreateWaitfor):
                break
        else:
            event = None
    else:
        event = event_message_create
        if isinstance(event, CommandProcessor):
            raise RuntimeError(f'The client already has a `{CommandProcessor.__name__}` instance added as '
                f'event.')
        
        if not isinstance(event, MessageCreateWaitfor):
            event = None
    
    if (event is not None):
        client.events.remove(event)
        
        command_processor.waitfors.update(event.waitfors)
        event.waitfors.clear()

EXTENSION_SETUP_HOOKS.append(extension_setup_hook)
