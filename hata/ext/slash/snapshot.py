from ..extension_loader.snapshot import SNAPSHOT_TAKERS
from ..extension_loader.extension_loader import EXTENSION_LOADER

from .application_command import SYNC_ID_NON_GLOBAL
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
    collected : `None` or `tuple` of (`dict` of (`int`, `list` of `tuple` \
            (`bool`, ``SlasherApplicationCommand``)) items, `None` or `set` of ``ComponentCommand``)
        The collected commands of the slasher.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is None) or (not isinstance(slasher, Slasher)):
        collected = None
    
    else:
        command_states = slasher._command_states
        
        collected_application_commands = None
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
            
            if collected_application_commands is None:
                collected_application_commands = {}
            
            collected_application_commands[guild_id] = command_changes
        
        collected_component_commands = slasher._component_commands
        if collected_component_commands:
            collected_component_commands = collected_component_commands.copy()
        else:
            collected_component_commands = None
        
        if (collected_application_commands is None) and (collected_component_commands is None):
            collected = None
        else:
            collected = (collected_application_commands, collected_component_commands)
    
    return collected

def calculate_slasher_snapshot_difference(client, snapshot_old, snapshot_new):
    """
    Calculates the difference between two slasher snapshots
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    snapshot_old :  `None` or `tuple` of (`dict` of (`int`, `list` of `tuple` \
            (`bool`, ``SlasherApplicationCommand``)) items, `None` or `set` of ``ComponentCommand``)
        An old snapshot taken.
    snapshot_new :  `None` or `tuple` of (`dict` of (`int`, `list` of `tuple` \
            (`bool`, ``SlasherApplicationCommand``)) items, `None` or `set` of ``ComponentCommand``)
        A new snapshot.
    
    Returns
    -------
    snapshot_difference : `None` or `tuple` (`tuple` (`set` of ``SlasherApplicationCommand``, `set` of \
            ``SlasherApplicationCommand``), `tuple` (`None` or `set` of ``ComponentCommand``, `None` or \
            `set` of ``ComponentCommand``)
        The difference between the two snapshots.
    """
    if (snapshot_old is None) and (snapshot_new is None):
        return None
    
    
    if snapshot_old is None:
        application_command_snapshot_old = None
        component_command_snapshot_old = None
    else:
        application_command_snapshot_old, component_command_snapshot_old = snapshot_old
    
    if snapshot_new is None:
        application_command_snapshot_new = None
        component_command_snapshot_new = None
    else:
        application_command_snapshot_new, component_command_snapshot_new = snapshot_new
        
    
    if (application_command_snapshot_old is not None) or (application_command_snapshot_new is not None):
        added_application_commands = []
        removed_application_commands = []
        
        guild_ids = set()
        if (application_command_snapshot_old is not None):
            guild_ids.update(application_command_snapshot_old.keys())
        
        if (application_command_snapshot_new is not None):
            guild_ids.update(application_command_snapshot_new.keys())
        
        for guild_id in guild_ids:
            local_added_application_commands = []
            local_removed_application_commands = []
            
            if (application_command_snapshot_new is not None):
                try:
                    new_changes = application_command_snapshot_new[guild_id]
                except KeyError:
                    pass
                else:
                    for added, command in new_changes:
                        if added:
                            local_added_application_commands.append(command)
                        else:
                            local_removed_application_commands.remove(command)
            
            if (application_command_snapshot_old is not None):
                try:
                    old_changes = application_command_snapshot_old[guild_id]
                except KeyError:
                    pass
                else:
                    for added, command in old_changes:
                        if added:
                            try:
                                local_added_application_commands.remove(command)
                            except ValueError:
                                local_removed_application_commands.append(command)
                        else:
                            try:
                                local_removed_application_commands.remove(command)
                            except ValueError:
                                local_added_application_commands.append(command)
            
            added_application_commands.extend(local_added_application_commands)
            removed_application_commands.extend(local_removed_application_commands)
        
        if (not added_application_commands):
            added_application_commands = None
        
        if (not removed_application_commands):
            removed_application_commands = None
    
        if (added_application_commands is None) and (removed_application_commands is None):
            application_command_difference = None
        else:
            if client.running and client.application.id:
                slasher = getattr(client, 'slasher', None)
                if (slasher is not None):
                    slasher.sync()
            
            application_command_difference = added_application_commands, removed_application_commands
    else:
        application_command_difference = None
    
    if (component_command_snapshot_old is None) or (component_command_snapshot_new is None):
        removed_component_commands = component_command_snapshot_old
        added_component_commands = component_command_snapshot_new
    else:
        removed_component_commands = component_command_snapshot_old-component_command_snapshot_new
        added_component_commands = component_command_snapshot_new-component_command_snapshot_old
        
        if (not removed_component_commands):
            removed_component_commands = None
        
        if (not added_component_commands):
            added_component_commands = None
    
    if (added_component_commands is None) and (removed_component_commands is None):
        component_command_difference = None
    else:
        component_command_difference = (removed_component_commands, added_component_commands)
    
    if (application_command_difference is None) and (component_command_difference is None):
        snapshot_difference = None
    else:
        snapshot_difference = (application_command_difference, component_command_difference)
    
    return snapshot_difference

def revert_slasher_snapshot(client, snapshot_difference):
    """
    Reverts a snapshot taken from a slasher.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    snapshot_difference : `None` or `tuple` (`tuple` (`set` of ``SlasherApplicationCommand``, `set` of \
            ``SlasherApplicationCommand``), `tuple` (`None` or `set` of ``ComponentCommand``, `None` or \
            `set` of ``ComponentCommand``)
        The taken snapshot.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is None) or (not isinstance(slasher, Slasher)):
        return
    
    if (snapshot_difference is not None):
        application_command_difference, component_command_difference = snapshot_difference
        
        if (application_command_difference is not None):
            added_application_commands, removed_application_commands = application_command_difference
            if (added_application_commands is not None):
                for application_command in added_application_commands:
                    slasher._remove_application_command(application_command)
            
            if (removed_application_commands is not None):
                for application_command in removed_application_commands:
                    slasher._add_application_command(application_command)
            
            if client.running and client.application.id:
                slasher.sync()
        
        if (component_command_difference is not None):
            added_component_commands, removed_component_commands = component_command_difference
            
            if (added_component_commands is not None):
                for component_command in added_component_commands:
                    slasher._remove_component_command(component_command)

            if (removed_component_commands is not None):
                for component_command in removed_component_commands:
                    slasher._add_component_command(component_command)

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
