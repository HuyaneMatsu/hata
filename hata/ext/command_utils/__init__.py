from ...discord.client import Client
from ...discord.events.core import DEFAULT_EVENT_HANDLER
from ...discord.events.handling_helpers import EventWaitforBase, asynclist

from .bases import *
from .choose_menu import *
from .closer import *
from .io import *
from .pagination import *
from .user_menu import *
from .utils import *
from .waiters import *

__all__ = (
    'setup_ext_command_utils',
    *bases.__all__,
    *choose_menu.__all__,
    *closer.__all__,
    *io.__all__,
    *pagination.__all__,
    *utils.__all__,
    *waiters.__all__,
    *user_menu.__all__,
)

from .. import register_library_extension, register_setup_function

def setup_ext_command_utils(client):
    """
    Setups the `command_utils` extension on the given client by adding ``ReactionAddWaitfor``, ``ReactionDeleteWaitfor``
    and ``MessageCreateWaitfor`` to it.
    
    Parameters
    ----------
    client : ``Client``
        The client to setup the extension on.
    """
    if not isinstance(client, Client):
        raise TypeError(
            f'Expected type `{Client.__name__}` as client, got {client.__class__.__name__}; {client!r}.'
        )
    
    event_reaction_add = client.events.reaction_add
    while True:
        if event_reaction_add is DEFAULT_EVENT_HANDLER:
            client.events(ReactionAddWaitfor)
            break
        
        if type(event_reaction_add) is asynclist:
            for event in list.__iter__(event_reaction_add):
                if isinstance(event, EventWaitforBase):
                    break
            else:
                client.events(ReactionAddWaitfor)
            
            break
        
        if isinstance(event_reaction_add, EventWaitforBase):
            break
        
        client.events(ReactionAddWaitfor)
        break
    
    event_reaction_delete = client.events.reaction_delete
    while True:
        if event_reaction_delete is DEFAULT_EVENT_HANDLER:
            client.events(ReactionDeleteWaitfor)
            break
        
        if type(event_reaction_delete) is asynclist:
            for event in list.__iter__(event_reaction_add):
                if isinstance(event, EventWaitforBase):
                    break
            else:
                client.events(ReactionDeleteWaitfor)
            
            break
        
        if isinstance(event_reaction_delete, EventWaitforBase):
            break
        
        client.events(ReactionDeleteWaitfor)
        break
    
    event_message_create = client.events.message_create
    while True:
        if event_message_create is DEFAULT_EVENT_HANDLER:
            client.events(MessageCreateWaitfor)
            break
        
        if type(event_message_create) is asynclist:
            for event in list.__iter__(event_message_create):
                if isinstance(event, EventWaitforBase):
                    break
            else:
                client.events(MessageCreateWaitfor)
            
            break
        
        if isinstance(event_message_create, EventWaitforBase):
            break
        
        client.events(MessageCreateWaitfor)
        break


register_library_extension('HuyaneMatsu.command_utils')

register_setup_function(
    'HuyaneMatsu.command_utils',
    setup_ext_command_utils,
    None,
    None,
)
