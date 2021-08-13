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
    description : `None` or `str`
        The docstring to clear.
    
    Returns
    -------
    cleared : `None` or `str`
        The cleared docstring. If `docstring` was given as `None` or is detected as empty, will return `None`.
    """
    if description is None:
        return None
    
    lines = description.splitlines()
    for index in reversed(range(len(lines))):
        line = lines[index]
        line = line.strip()
        if line:
            lines[index] = line
        else:
            del lines[index]
    
    if not lines:
        return None
    
    return ' '.join(lines)


def _check_maybe_route(variable_name, variable_value, route_to, validator):
    """
    Helper class of ``SlasherApplicationCommand`` parameter routing.
    
    Parameters
    ----------
    variable_name : `str`
        The name of the respective variable
    variable_value : `str`
        The respective value to route maybe.
    route_to : `int`
        The value how much times the routing should happen. by default should be given as `0` if no routing was
        done yet.
    validator : `callable` or `None`
        A callable, what validates the given `variable_value`'s value and converts it as well if applicable.
    
    Returns
    -------
    processed_value : `str`
        Processed value returned by the `validator`. If routing is happening, then a `tuple` of those values is
        returned.
    route_to : `int`
        The amount of values to route to.
    
    Raises
    ------
    ValueError
        Value is routed but to a bad count amount.
    BaseException
        Any exception raised by `validator`.
    """
    if (variable_value is not None) and isinstance(variable_value, tuple):
        route_count = len(variable_value)
        if route_count == 0:
            processed_value = None
        elif route_count == 1:
            variable_value = variable_value[0]
            if variable_value is ...:
                variable_value = None
            
            if validator is None:
                processed_value = variable_value
            else:
                processed_value = validator(variable_value)
        else:
            if route_to == 0:
                route_to = route_count
            elif route_to == route_count:
                pass
            else:
                raise ValueError(f'`{variable_name}` is routed to `{route_count}`, meanwhile something else is '
                    f'already routed to `{route_to}`.')
            
            if validator is None:
                processed_value = variable_value
            else:
                processed_values = []
                for value in variable_value:
                    if (value is not ...):
                        value = validator(value)
                    
                    processed_values.append(value)
                
                processed_value = tuple(processed_values)
    
    else:
        if validator is None:
            processed_value = variable_value
        else:
            processed_value = validator(variable_value)
    
    return processed_value, route_to


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


