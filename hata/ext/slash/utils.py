__all__ = ()

from ...discord.client import Client


UNLOADING_BEHAVIOUR_DELETE = 0
UNLOADING_BEHAVIOUR_KEEP = 1
UNLOADING_BEHAVIOUR_INHERIT = 2


SYNC_ID_GLOBAL = 0
SYNC_ID_MAIN = 1
SYNC_ID_NON_GLOBAL = 2


def raw_name_to_display(raw_name):
    """
    Converts the given raw application command name to it's display name.
    
    Parameters
    ----------
    raw_name : `str`
        The name to convert.
    
    Returns
    -------
    display_name : `str`
        The converted name.
    """
    return '-'.join([w for w in raw_name.strip('_ ').lower().replace(' ', '-').replace('_', '-').split('-') if w])


def normalize_description(description):
    """
    Normalizes a docstrings.
    
    Parameters
    ----------
    description : `None`, `str`
        The docstring to clear.
    
    Returns
    -------
    cleared : `None`, `str`
        The cleared docstring. If `docstring` was given as `None` or is detected as empty, will return `None`.
    """
    if description is None:
        return None
    
    lines = description.splitlines()
    
    # strip
    for index in range(len(lines)):
        lines[index] = lines[index].strip()
    
    # Remove empty lines from the start~
    while lines and not lines[0]:
        del lines[0]
    
    # Remove everything after the first empty line.
    try:
        pop_since_index = lines.index('')
    except ValueError:
        pop_since_index = -1
    
    if pop_since_index != -1:
        del lines[pop_since_index:]
    
    # Build response :KoishiSpam:
    if lines:
        return ' '.join(lines)


RUNTIME_SYNC_HOOKS = []

def runtime_sync_hook_is_client_running(client):
    """
    Runtime sync hook to check whether a slash command should be registered and synced instantly when added or removed.
    
    Parameters
    ----------
    client : ``Client``
        The respective client of the ``Slasher``.
    """
    return client.running

RUNTIME_SYNC_HOOKS.append(runtime_sync_hook_is_client_running)


