from ..extension_loader.snapshot import SNAPSHOT_TAKERS
from .command_processor import CommandProcessor

def take_command_processor_snapshot(client):
    """
    Collects all the commands and categories of a client's command processor.
    
    Parameters
    ----------
    client : ``Client``
        The client, who will be snapshotted.
    
    Returns
    -------
    collected : `None` or `tuple` of (`None` or `set` of ``Category``, `None` or `set` of ``Command``)
    """
    command_processor = getattr(client, 'command_processor', None)
    if (command_processor is None) or (not isinstance(command_processor, CommandProcessor)):
        collected = None
    else:
        category_name_to_category = command_processor.category_name_to_category
        if category_name_to_category:
            categories = set(category_name_to_category.values())
        else:
            categories = None
        
        commands = command_processor.commands
        if commands:
            commands = commands.copy()
        else:
            commands = None
        
        if (categories is None) and (commands is None):
            collected = None
        else:
            collected = (commands, categories)
    
    return collected


def calculate_command_processor_snapshot_difference(client, snapshot_old, snapshot_new):
    """
    Calculates the difference between two command processor snapshots.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    snapshot_old : `None` or `tuple` of (`None` or `set` of ``Category``, `None` or `set` of ``Command``)
        An old snapshot taken.
    snapshot_new : `None` or `tuple` of (`None` or `set` of ``Category``, `None` or `set` of ``Command``)
        A new snapshot.
    
    Returns
    -------
    snapshot_difference : `None` or `tuple` (`tuple` (`None` or `set`, `None` or `set`), \
            `tuple` (`None` or `set`, `None` or `set`))
        The difference between the two snapshots.
    """
    if (snapshot_old is None) or (snapshot_new is None):
        return None
    
    if snapshot_old is None:
        old_categories = None
        old_commands = None
    else:
        old_commands, old_categories = snapshot_old
    
    if snapshot_new is None:
        new_categories = None
        new_commands = None
    else:
        new_commands, new_categories = snapshot_new
    
    
    if (new_commands is None) or (old_commands is None):
        command_interception = None
    else:
        command_interception = old_commands&new_commands
    
    if command_interception is None:
        old_commands = None
        new_commands = None
    else:
        old_commands = old_commands-command_interception
        new_commands = new_commands-command_interception
        
        if not old_commands:
            old_commands = None
        
        if not new_commands:
            new_commands = None
    
    if (old_commands is None) and (new_commands is None):
        command_difference = None
    else:
        command_difference = (old_commands, new_commands)
    
    
    if (old_categories is None) or (new_categories is None):
        category_interception = None
    else:
        category_interception = old_categories&new_categories
    
    if category_interception is None:
        old_categories = None
        new_categories = None
    else:
        old_categories = old_categories-category_interception
        new_categories = new_categories-category_interception
        
        if not old_categories:
            old_categories = None
        
        if not new_categories:
            new_categories = None
    
    if (old_categories is None) and (new_categories is None):
        category_difference = None
    else:
        category_difference = (old_categories, new_categories)
    
    if (command_difference is None) and (category_difference is None):
        snapshot_difference = None
    else:
        snapshot_difference = (command_difference, category_difference)
    
    return snapshot_difference


def revert_command_processor_snapshot(client, snapshot_difference):
    """
    Reverts a snapshot taken from a command processor.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    snapshot_difference : `tuple` (`tuple` (`None` or `set`, `None` or `set`), \
            `tuple` (`None` or `set`, `None` or `set`))
        The taken snapshot.
    """
    command_processor = getattr(client, 'command_processor', None)
    if (command_processor is None) or (not isinstance(command_processor, CommandProcessor)):
        return
    
    command_difference, category_difference = snapshot_difference
    
    if (command_difference is not None):
        old_commands, new_commands = command_difference
        if (new_commands is not None):
            for command in new_commands:
                command_processor._remove_command(command)
        
        if (old_commands is not None):
            for command in old_commands:
                command_processor._add_command(command)
    
    if (category_difference is not None):
        old_categories, new_categories = category_difference
        if (new_categories is not None):
            for category in new_categories:
                command_processor._remove_category(category)
        
        if (old_categories is not None):
            for category in old_categories:
                command_processor._add_category(category)


SNAPSHOT_TAKERS['client.command_processor'] = (
    take_command_processor_snapshot,
    calculate_command_processor_snapshot_difference,
    revert_command_processor_snapshot,
)
