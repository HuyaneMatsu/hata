# -*- coding: utf-8 -*-
"""
Hata extensions for supporting interactions.
"""
from ...backend.futures import Task
from ...discord.client_core import KOKORO

from .command import *

import warnings

from .utils import _do_initial_sync, _application_command_create_watcher, _application_command_delete_watcher, \
    _application_command_permission_update_watcher
from .client_wrapper_extension import *

__all__ = (
    'set_permission',
    'setup_ext_slash',
    *command.__all__,
        )

set_permission = SlashCommandPermissionOverwriteWrapper

def setup_ext_slash(client, *, immediate_sync=None, **kwargs):
    """
    Setups the slash extension on client.
    
    Note, that this function can be called on a client only once.
    
    Parameters
    ----------
    client : ``Client``
        The client to setup the extension on.
    immediate_sync : `bool`, Optional
        Whether application command sync task should be started immediately as it is detected that no more features
        are added to the slasher. Defaults to `False`.
    **kwargs : Keyword parameters
        Additional keyword parameter to be passed to the created ``Slasher``.
    
    Other Parameters
    ----------------
    delete_commands_on_unload: `bool`, Optional
        Whether commands should be deleted when unloaded.
    
    Returns
    -------
    slasher : ``Slasher``
        Slash command processor.
    
    Raises
    ------
    RuntimeError
        If the client has an attribute set what the slasher would use.
    
    TypeError
        If `delete_commands_on_unload` was not given as `bool` instance.
    """
    for attr_name in ('slasher', 'interactions'):
        if hasattr(client, attr_name):
            raise RuntimeError(f'The client already has an attribute named as `{attr_name}`.')
    
    if (immediate_sync is not None):
        warnings.warn(
            f'`setup_ext_slash`\'s `immediate_sync` parameter is deprecated, and will be removed in 2021 April.',
            FutureWarning)
    
    slasher = Slasher(**kwargs)
    
    client.events(slasher)
    client.slasher = slasher
    client.interactions = slasher.shortcut
    client.events(_do_initial_sync, name='launch')
    client.events(_application_command_create_watcher, name='application_command_create')
    client.events(_application_command_delete_watcher, name='application_command_delete')
    client.events(_application_command_permission_update_watcher, name='application_command_permission_update')
    
    return slasher


def snapshot_hook():
    from . import snapshot
    

from .. import register_library_extension, add_library_extension_hook
register_library_extension('HuyaneMatsu.slash')
add_library_extension_hook(snapshot_hook, ['HuyaneMatsu.extension_loader'])
del register_library_extension, add_library_extension_hook, snapshot_hook
