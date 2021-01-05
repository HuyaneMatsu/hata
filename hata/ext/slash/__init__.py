# -*- coding: utf-8 -*-
"""
Hata extension for controlling slash commands.

Work in progress.
"""
from ...backend.futures import Task
from ...discord.client_core import KOKORO

from .command import Slasher
from .utils import _do_initial_sync, _application_command_create_watcher, _application_command_delete_watcher, \
    delay_immediate_start_initial_sync
from .client_wrapper_extension import *

__all__ = command.__all__

def setup_ext_slash(client, *, immediate_sync=False):
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
    
    Returns
    -------
    slasher : ``Slasher``
        Slash command processor.
    
    Raises
    ------
    RuntimeError
        If the client has an attribute set what the slasher would use.
    """
    for attr_name in ('slasher', 'interactions'):
        if hasattr(client, attr_name):
            raise RuntimeError(f'The client already has an attribute named as `{attr_name}`.')
    
    slasher = Slasher()
    
    client.events(slasher)
    client.slasher = slasher
    client.interactions = slasher.shortcut
    client.events(_do_initial_sync, name='ready')
    client.events(_application_command_create_watcher, name='application_command_create')
    client.events(_application_command_delete_watcher, name='application_command_delete')
    
    if immediate_sync:
        Task(delay_immediate_start_initial_sync(client, slasher), KOKORO)
    
    return slasher


def snapshot_hook():
    from . import snapshot
    

from .. import register_library_extension, add_library_extension_hook
register_library_extension('HuyaneMatsu.slash')
add_library_extension_hook(snapshot_hook, ['HuyaneMatsu.extension_loader'])
del register_library_extension, add_library_extension_hook, snapshot_hook
