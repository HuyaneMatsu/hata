from .category import *
from .checks import *
from .client_wrapper_extension import *
from .command import *
from .command_helpers import *
from .command_processor import *
from .content_parser import *
from .context import *
from .cooldown import *
from .exceptions import *
from .responding import *
from .utils import *
from .wrappers import *


__all__ = (
    'checks',
    'cooldown',
    'configure_converter',
    'setup_ext_commands_v2',
    
    *category.__all__,
    *checks.__all__,
    *client_wrapper_extension.__all__,
    *command.__all__,
    *command_helpers.__all__,
    *command_processor.__all__,
    *content_parser.__all__,
    *context.__all__,
    *cooldown.__all__,
    *exceptions.__all__,
    *responding.__all__,
    *utils.__all__,
    *wrappers.__all__,
)


from ...discord.client import Client

from .. import register_library_extension, add_library_extension_hook, register_setup_function

from . import checks


configure_converter = CommandConverterConfigurerWrapper
cooldown = CommandCooldownWrapper


EXTENSION_SETUP_HOOKS = []

def setup_ext_commands_v2(client, prefix, **kwargs):
    """
    Setups the commands extension of hata on the given client with the given parameters.
    
    Note that this function can be called on a client only once.
    
    The function adds the following attributes to the client:
    - `.command_processor` : ``CommandProcessor``
    - `.commands` : ``_EventHandlerManager``
    
    And the following event handlers are added as well:
    - `message_create` : ``CommandProcessor``
    - `reaction_add` : ``ReactionAddWaitfor`` (Except if other ``EventWaitforBase`` is already added.)
    - `reaction_delete` : ``ReactionDeleteWaitfor`` (Except if other ``EventWaitforBase`` is already added.)
    
    Parameters
    ----------
    client : ``Client`
        The client on what the extension will be setuped.
    prefix : `str`, (`tuple`, `list`, `deque`) of `str`, `callable` -> `str`, Optional
        The prefix of the client's command processor.
        
        Can be given as `str`, as `tuple`, `list`, `deque` of `str`, or as a `callable`, what accepts `1` parameter,
        the respective ``Message`` and returns `str`.
    **kwargs : Keyword parameters
        Additional keyword parameters to be passed to the created ``CommandProcessor``.
    
    Returns
    -------
    command_processor : ``CommandProcessor``
        The created command processor. Returns `None` if `lite` is given as `True`.
    
    Raises
    ------
    TypeError
        - If `client` was not given as ``Client``.
        - If `prefix` was not given meanwhile `lite` is `False`.
    RuntimeError
        - If the given `client` already has `command_processor` / `commands` attribute.
        - If the given `client` has a ``CommandProcessor`` added as `message_create` event,
    """
    if not isinstance(client, Client):
        raise TypeError(f'Expected type `{Client.__name__}` as client, meanwhile got `{client.__class__.__name__}`.')
    
    for attr_name in ('command_processor', 'commands'):
        if hasattr(client, attr_name):
            raise RuntimeError(f'The client already has an attribute named as `{attr_name}`.')
    
    command_processor = CommandProcessor(prefix, **kwargs)
    for hook in EXTENSION_SETUP_HOOKS:
        hook(client, command_processor)
    
    client.events(command_processor)
    
    client.command_processor = command_processor
    client.commands = command_processor.shortcut
    
    return command_processor


def snapshot_hook():
    from . import snapshot


register_library_extension('HuyaneMatsu.commands_v2')
add_library_extension_hook(snapshot_hook, ['HuyaneMatsu.plugin_loader'])

def command_utils_hook():
    from . import extension_hook_command_utils

add_library_extension_hook(command_utils_hook, ['HuyaneMatsu.command_utils'])

register_setup_function(
    'HuyaneMatsu.commands_v2',
    setup_ext_commands_v2,
    (
        'prefix',
    ),(
        'precheck',
        'mention_prefix_enabled',
        'category_name_rule',
        'command_name_rule',
        'default_category_name',
        'prefix_ignore_case',
    ),
)
