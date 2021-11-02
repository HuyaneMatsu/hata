import warnings

warnings.warn(
    '`commands` extension is deprecated and will be removed in 2022',
    FutureWarning,
)

from . import checks
from .command import *
from .content_parser import *
from .utils import *
from .client_wrapper_extension import *
from ...ext.command_utils import *
from ...ext import command_utils as module_command_utils
__all__ = (
    'checks',
    'setup_ext_commands',
    *client_wrapper_extension.__all__,
    *command.__all__,
    *content_parser.__all__,
    *utils.__all__,
    *module_command_utils.__all__,
)

del module_command_utils

# Add the setup extension function

from .. import register_library_extension, add_library_extension_hook, register_setup_function

from ...discord.client import Client
from ...discord.events.core import DEFAULT_EVENT_HANDLER
from ...discord.events.handling_helpers import asynclist
from ...ext.command_utils import setup_ext_command_utils, MessageCreateWaitfor

def setup_ext_commands(client, prefix=None, lite=False, **kwargs):
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
    client : ``Client`
        The client on what the extension will be setuped.
    prefix : `str`, (`tuple`, `list`, `deque`) of `str`, or `callable` -> `str`, Optional
        The prefix of the client's command processer.
        
        Can be given as `str`, as `tuple`, `list` or `deque` of `str`, or as a `callable`, what accepts `1` parameter,
        the respective ``Message`` instance and returns `str`.
    lite : `bool`, Optional
        Whether only the extensions utility feature should be setup. May be useful for example when the client uses
        only slash commands. Defaults to `False`.
    **kwargs : Keyword parameters
        Additional keyword parameters to be passed to the created ``CommandProcesser``.
    
    Other Parameters
    ----------------
    ignorecase : `bool`, Optional (Keyword only)
        Whether the prefix should be case insensitive. Defaults to `True`.
    mention_prefix : `bool`, Optional (Keyword only)
        Whether user mentioning the client as first word in a message's content should be interpreted as a prefix.
        Defaults to `true`
    default_category_name : `None` or `str`, Optional (Keyword only)
        The command processer's default category's name. Defaults to `None`.
    category_name_rule : `None` or `function`, Optional (Keyword only)
        Function to generate display names for categories.
        Should accept only 1 parameter, what can be `str`  or `None` and should return a `str` instance as well.
    command_name_rule : `None` or `function`, Optional (Keyword only)
        Function to generate display names for commands.
        Should accept only 1 parameter, what is `str` instance and should return a `str` instance as well.
    precheck : `None` or `callable`, Optional (Keyword only)
        Function, which decides whether a received message should be processed
        
        The default one filters out every message what's author is a bot account and the channels where the client
        cannot send messages.
        
        The following parameters are passed to it:
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | client    | ``Client``    |
        +-----------+---------------+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Should return the following values:
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | should_process    | `bool`    |
        +-------------------+-----------+
        
    Returns
    -------
    command_processer : ``CommandProcesser`` or `None`
        The created command processer. Returns `None` if `lite` is given as `True`.
    
    Raises
    ------
    TypeError
        - If `client` was not given as ``Client`` instance.
        - If `prefix` was not given meanwhile `lite` is `False`.
    RuntimeError
        - If the given `client` already has `command_processer` or `commands` attribute.
        - If the given `client` has a ``CommandProcesser`` instance added as `message_create` event,
    """
    if not isinstance(client, Client):
        raise TypeError(f'Expected type `{Client.__name__}` as client, meanwhile got `{client.__class__.__name__}`.')
    
    for attr_name in ('command_processer', 'command_processor', 'commands'):
        if hasattr(client, attr_name):
            raise RuntimeError(f'The client already has an attribute named as `{attr_name}`.')
    
    if (not lite) and (prefix is None):
        raise TypeError(f'`prefix` parameter is required if `lite` is given as `False`.')
    
    if lite:
        command_processer = None
    else:
        event_message_create = client.events.message_create
        while True:
            if event_message_create is DEFAULT_EVENT_HANDLER:
                replace_index = -3
                break
            
            if type(event_message_create) is asynclist:
                for index in range(list.__len__(event_message_create)):
                    event = list.__getitem__(event_message_create, index)
                    if isinstance(event, CommandProcesser):
                        raise RuntimeError(f'The client already has a `{CommandProcesser.__name__}` instance added as '
                            f'event.')
                    
                    if isinstance(event, MessageCreateWaitfor):
                        replace_index = index
                        break
                else:
                    replace_index = -1
                
                break
            
            if isinstance(event_message_create, CommandProcesser):
                raise RuntimeError(f'The client already has a `{CommandProcesser.__name__}` instance added as event.')
            
            if isinstance(event_message_create, MessageCreateWaitfor):
                replace_index = -2
                break
            
            replace_index = -4
            break
        
        command_processer = CommandProcesser(prefix, **kwargs)
        if (replace_index == -3) or (replace_index == -1) or (replace_index == -4):
            client.events(command_processer)
        else:
            command_processer.waitfors.update(event_message_create.waitfors)
            event_message_create.waitfors.clear()
            
            if replace_index == -2:
                client.events(command_processer, overwrite=True)
            else:
                client.events.message_create[replace_index] = command_processer
        
        client.command_processer = command_processer
        client.command_processor = command_processer
        client.commands = command_processer.shortcut
    
    setup_ext_command_utils(client)
    
    return command_processer


def snapshot_hook():
    from . import snapshot


register_library_extension('HuyaneMatsu.commands')
add_library_extension_hook(snapshot_hook, ['HuyaneMatsu.extension_loader'])


register_setup_function(
    'HuyaneMatsu.commands',
    setup_ext_commands,
    None,
    (
        'prefix',
        'lite',
        'ignorecase',
        'mention_prefix',
        'default_category_name',
        'category_name_rule',
        'command_name_rule',
        'precheck',
    ),
)
