# -*- coding: utf-8 -*-
from ..extension_loader.snapshot import SNAPSHOT_TAKERS
from .command import Slasher

def take_slasher_snapshot(client):
    """
    Collects all the command changes from the client's slash command processor.
    
    Parameters
    ----------
    client : ``Client``
        The client, who will be snapshotted.
    
    Returns
    -------
    collected : `None` or `set` of ``SlashCommand``
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is None) or (not isinstance(slasher, Slasher)):
        collected = None
    
    else:
        collected = slasher._get_commands()
    
    return collected

def calculate_slasher_snapshot_difference(client, snapshot_old, snapshot_new):
    """
    Calculates the difference between two slasher snapshots
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    snapshot_old : `None` of `set` of ``SlashCommand``
        An old snapshot taken.
    snapshot_new : `None` of `set` of ``SlashCommand``
        A new snapshot.
    
    Returns
    -------
    snapshot_difference : `None` or `tuple` (`set` of ``SlashCommand``, `set` of ``SlashCommand``)
    """
    if (snapshot_old is None) or (snapshot_new is None):
        return None
    
    removed_commands = []
    
    while snapshot_old:
        old_command = snapshot_old.pop()
        
        try:
            snapshot_new.remove(snapshot_new)
        except KeyError:
            removed_commands.append(old_command)
    
    added_commands = snapshot_new-snapshot_old
    removed_commands = snapshot_old-snapshot_new
    
    if (not added_commands) and (not removed_commands):
        return None
    
    if client.running and client.application.id:
        slasher = getattr(client, 'slasher', None)
        if (slasher is not None):
            slasher.do_main_sync(client)
    
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
    
    slasher.do_main_sync(client)

SNAPSHOT_TAKERS['client.slasher'] = (
    take_slasher_snapshot,
    calculate_slasher_snapshot_difference,
    revert_slasher_snapshot,
        )
