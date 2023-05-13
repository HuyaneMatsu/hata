__all__ = ('get_bool_env', 'get_int_env', 'get_str_env',)


import warnings
from os import getenv as get_environmental_variable


ERROR_MESSAGE_APPENDIX = 'Please update your `.env` file.'


def get_bool_env(name, default = False, *, warn_if_empty = True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or not present as a boolean's representation returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `bool` = `False`, Optional
        The default value of the respective variable.
    warn_if_empty : `bool` = `True`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    env_variable : `bool`
    """
    env_variable = get_environmental_variable(name)
    if env_variable is None:
        return default
    
    env_variable = env_variable.casefold()
    if env_variable in ('true', '0'):
        return True
    
    if env_variable in ('false', '0'):
        return False
    
    if warn_if_empty:
        warnings.warn(
            f'{name!r} is specified as non bool: {env_variable!r}, defaulting to {default!r}!',
        )
    
    return default


def get_str_env(name, default = None, *, raise_if_missing_or_empty = False, warn_if_empty = True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or present as an empty string returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `None` | `str` = `None`, Optional
        The default value of the respective variable. Defaults to `None`.
    raise_if_missing_or_empty : `bool` = `False`, Optional (Keyword only)
        Whether exception should be thrown if the environmental variable is missing or empty.
        Has priority over `default` and `warn_if_empty`.
    warn_if_empty : `bool` = `True`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    variable : `None` | `str`
    
    Raises
    ------
    RuntimeError
    """
    env_variable = get_environmental_variable(name)
    if env_variable is None:
        if raise_if_missing_or_empty:
            raise RuntimeError(
                f'Environmental variable {name!r} is missing. {ERROR_MESSAGE_APPENDIX}'
            )
        
        return default
    
    if env_variable:
        return env_variable
    
    if raise_if_missing_or_empty:
        raise RuntimeError(
            f'Environmental variable {name!r} is specified as empty string. {ERROR_MESSAGE_APPENDIX}'
        )
    
    if warn_if_empty:
        warnings.warn(
            f'{name!r} is specified as empty string, defaulting to {default!r}!',
        )
    
    return default


def get_int_env(name, default = 0, *, warn_if_empty = True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or present as non `int`, will return `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `int` = `0`, Optional
        The default value of the respective variable.
    warn_if_empty : `bool` = `True`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    variable : `int`
    """
    env_variable = get_environmental_variable(name)
    if env_variable is None:
        return default
    
    if not env_variable:
        return default
    
    try:
        variable = int(env_variable)
    except ValueError:
        pass
    else:
        return variable
    
    if warn_if_empty:
        warnings.warn(
            f'{name!r} is specified as non `int`: {env_variable!r}, defaulting to {default!r}!',
        )
    
    return default

