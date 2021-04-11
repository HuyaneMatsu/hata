# -*- coding: utf-8 -*-
from ..extension_loader.snapshot import SNAPSHOT_TAKERS
from ..extension_loader.extension_loader import EXTENSION_LOADER

from .command import SYNC_ID_NON_GLOBAL
from .slasher import Slasher
from .utils import RUNTIME_SYNC_HOOKS

def take_slasher_snapshot(client):
    """
    Collects all the command changes from the client's slash command processor.
    
    Parameters
    ----------
    client : ``Client``
        The client, who will be snapshotted.
    
    Returns
    -------
    collected : `None` or `dict` of (`int`, `list` of `tuple` (`bool`, ``SlashCommand``)) items
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is None) or (not isinstance(slasher, Slasher)):
        collected = None
    
    else:
        command_states = slasher._command_states
        
        collected = None
        for guild_id, command_state in command_states.items():
            if guild_id == SYNC_ID_NON_GLOBAL:
                active_commands = command_state._active
                if (active_commands is None):
                    continue
                
                command_changes = [(True, command) for command in active_commands]
                
            else:
                changes = command_state._changes
                if changes is None:
                    continue
                
                command_changes = [tuple(change) for change in changes]
            
            if collected is None:
                collected = {}
            
            collected[guild_id] = command_changes
    
    return collected

def calculate_slasher_snapshot_difference(client, snapshot_old, snapshot_new):
    """
    Calculates the difference between two slasher snapshots
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    snapshot_old :  `None` or `dict` of (`int`, `list` of `tuple` (`bool`, ``SlashCommand``)) items
        An old snapshot taken.
    snapshot_new :  `None` or `dict` of (`int`, `list` of `tuple` (`bool`, ``SlashCommand``)) items
        A new snapshot.
    
    Returns
    -------
    snapshot_difference : `None` or `tuple` (`set` of ``SlashCommand``, `set` of ``SlashCommand``)
    """
    if (snapshot_old is None) and (snapshot_new is None):
        return None
    
    # Keep the order!
    added_commands = []
    removed_commands = []
    
    guild_ids = set()
    if (snapshot_old is not None):
        guild_ids.update(snapshot_old.keys())
    
    if (snapshot_new is not None):
        guild_ids.update(snapshot_new.keys())
    
    for guild_id in guild_ids:
        local_added_commands = []
        local_removed_commands = []
        
        if (snapshot_new is not None):
            try:
                new_changes = snapshot_new[guild_id]
            except KeyError:
                pass
            else:
                for added, command in new_changes:
                    if added:
                        local_added_commands.append(command)
                    else:
                        local_removed_commands.remove(command)
        
        if (snapshot_old is not None):
            try:
                old_changes = snapshot_old[guild_id]
            except KeyError:
                pass
            else:
                for added, command in old_changes:
                    if added:
                        try:
                            local_added_commands.remove(command)
                        except ValueError:
                            local_removed_commands.append(command)
                    else:
                        try:
                            local_removed_commands.remove(command)
                        except ValueError:
                            local_added_commands.append(command)
        
        added_commands.extend(local_added_commands)
        removed_commands.extend(local_removed_commands)
    
    if (not added_commands) and (not removed_commands):
        return None
    
    if client.running and client.application.id:
        slasher = getattr(client, 'slasher', None)
        if (slasher is not None):
            slasher.sync()
    
    return added_commands, removed_commands

def revert_slasher_snapshot(client, snapshot_difference):
    """
    Reverts a snapshot taken from a slasher.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    snapshot_difference : `tuple` (`set` of ``SlashCommand``, `set` of ``SlashCommand``)
        The taken snapshot.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is None) or (not isinstance(slasher, Slasher)):
        return
    
    added_commands, removed_commands = snapshot_difference
    for command in added_commands:
        slasher._remove_command(command)
    
    for command in removed_commands:
        slasher._add_command(command)
    
    if client.running and client.application.id:
        slasher.sync()

SNAPSHOT_TAKERS['client.slasher'] = (
    take_slasher_snapshot,
    calculate_slasher_snapshot_difference,
    revert_slasher_snapshot,
        )


def runtime_sync_hook_is_executing_extension(client):
    """
    Runtime sync hook to check whether a slash command should be registered and synced instantly when added or removed.
    
    Parameters
    ----------
    client : ``Client``
        The respective client of the ``Slasher``.
    """
    return not EXTENSION_LOADER.is_processing_extension()

RUNTIME_SYNC_HOOKS.append(runtime_sync_hook_is_executing_extension)
