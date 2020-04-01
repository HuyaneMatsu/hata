# -*- coding: utf-8 -*-
from .command import *
from .compiler import *
from .utils import *

__all__ = (
    'setup_ext_commands',
    *command.__all__,
    *compiler.__all__,
    *utils.__all__,
        )

# Add the setup extension function

from ...discord.client import Client
from ...discord.parsers import DEFAULT_EVENT, asynclist, EventWaitforBase

def setup_ext_commands(client, prefix, **kwargs):
    if type(client) is not Client:
        raise TypeError(f'Expected type `{Client.__name__}` as client, meanwhile got `{client!r}`.')
    
    if hasattr(client,'command_processer'):
        raise RuntimeError(f'The client already has an attribute named as `{"command_processer"!r}`.')
    
    if hasattr(client,'commands'):
        raise RuntimeError(f'The client already has an attribute named s `{"commands"!r}`.')
    
    event_message_create=client.events.message_create
    while True:
        if event_message_create is DEFAULT_EVENT:
            break
        
        if type(event_message_create) is asynclist:
            for event in event_message_create:
                if isinstance(event,CommandProcesser):
                    raise RuntimeError(f'The client already has a `{CommandProcesser.__name__}` instance added as event.')
            break
        
        if isinstance(event_message_create,CommandProcesser):
            raise RuntimeError(f'The client already has a `{CommandProcesser.__name__}` instance added as event.')
        
        break
    
    command_processer = client.events(CommandProcesser(prefix,**kwargs))
    client.command_processer=command_processer
    client.commands=command_processer.shortcut
    
    event_reaction_add = client.events.reaction_add
    while True:
        if event_reaction_add is DEFAULT_EVENT:
            client.events(ReactionAddWaitfor)
            break
        
        if type(event_reaction_add) is asynclist:
            for event in event_reaction_add:
                if isinstance(event,EventWaitforBase):
                    break
            else:
                client.events(ReactionAddWaitfor)
            
            break
        
        if isinstance(event_reaction_add,EventWaitforBase):
            break
        
        client.events(ReactionAddWaitfor)
        break
    
    event_reaction_delete = client.events.reaction_delete
    while True:
        if event_reaction_delete is DEFAULT_EVENT:
            client.events(ReactionDeleteWaitfor)
            break
        
        if type(event_reaction_delete) is asynclist:
            for event in event_reaction_add:
                if isinstance(event,EventWaitforBase):
                    break
            else:
                client.events(ReactionDeleteWaitfor)
            
            break
        
        if isinstance(event_reaction_delete,EventWaitforBase):
            break
        
        client.events(ReactionDeleteWaitfor)
        break
    
    return command_processer
