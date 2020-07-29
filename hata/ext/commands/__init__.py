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
    """
    Setups the commands extension of hata on the given client with the given parameters.
    
    Note that this function can be called on a client only once.
    
    The function adds the following attributes to the client:
    - `.command_processer` : ``CommandProcesser``
    - `.commands` : ``_EventHandlerManager``
    
    And the following event handlers are added as well:
    - `message_create` : ``CommandProcesser``
    - `reaction_add` : ``ReactionAddWaitfor`` (Except if other ``EventWaitforBase`` instance is already added.)
    - `reaction_delete` : ``ReactionDeleteWaitfor`` (Except if other ``EventWaitforBase`` instance is already added.)
    
    Parameters
    ----------
    client : ``Client``
        The client on what the extension will be setuped.
    prefix : `str`, (`tuple`, `list`, `deque`) of `str`, or `callable` -> `str`
        The prefix of the client's command processer.
        
        Can be given as `str`, as `tuple`, `list` or `deque` of `str`, or as a `callable`, what accepts `1` argument,
        the respective ``Message`` instance and returns `str`.
    **kwargs : Keyword arguments
        Additional keyword arguments to be passed to the creater ``CommandProcesser``.
    
    Other Parameters
    ----------------
    ignorecase : `bool`
        Whether the prefix should be case insensitive. Defaults to `True`.
    mention_prefix : `bool`
        Whether user mentioning the client as first word in a message's content should be interpretered as a prefix.
        Defaults to `true`
    default_category_name : `None` or `str`
        The command processer's default category's name. Defaults to `None`.
    
    Returns
    -------
    command_processer : ``CommandProcesser``
        The created command processer.
    
    Raises
    ------
    TypeError
        If `client` was not given as ``Client`` instance.
    RuntimeError
        - If the given `client` already has `command_processer` or `commands` attribute.
        - If the given `client` has a ``CommandProcesser`` instance added as `message_create` event,
    """
    client_type = client.__class__
    if client_type is not Client:
        raise TypeError(f'Expected type `{Client.__name__}` as client, meanwhile got `{client_type.__name__}`.')
    
    if hasattr(client, 'command_processer'):
        raise RuntimeError(f'The client already has an attribute named as `command_processer"`.')
    
    if hasattr(client, 'commands'):
        raise RuntimeError(f'The client already has an attribute named s `commands`.')
    
    event_message_create=client.events.message_create
    while True:
        if event_message_create is DEFAULT_EVENT:
            break
        
        if type(event_message_create) is asynclist:
            for event in event_message_create:
                if isinstance(event,CommandProcesser):
                    raise RuntimeError(f'The client already has a `{CommandProcesser.__name__}` instance added as '
                        f'event.')
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
