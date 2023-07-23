__all__ = ('get_bool_env', 'get_int_env', 'get_str_env',)

from os import getenv as get_environmental_variable
from warnings import warn


ERROR_MESSAGE_APPENDIX = 'Please update your `.env` file.'


RETURN_TYPE_VALUE = 0
RETURN_TYPE_WARNING = 1
RETURN_TYPE_EXCEPTION = 2


def _process_bool_env(env_variable):
    """
    Processes the given `bool` environmental variable.
    
    Parameters
    ----------
    env_variable : `str`
        The variable to process.
    
    Returns
    -------
    accepted : `bool`
    value : `bool`
    """
    env_variable = env_variable.casefold()
    if env_variable in ('true', '1'):
        accepted = True
        value = True
    
    elif env_variable in ('false', '0'):
        accepted = True
        value = False
    
    else:
        accepted = False
        value = False
    
    return accepted, value


def _process_str_env(env_variable):
    """
    Processes a `str` environmental variable.
    
    Parameters
    ----------
    env_variable : `str`
        The variable to process.
    
    Returns
    -------
    accepted : `bool`
    value : `str`
    """
    return (True if env_variable else False), env_variable


def _process_int_env(env_variable):
    """
    Processes a `int` environmental variable.
    
    Parameters
    ----------
    env_variable : `str`
        The variable to process.
    
    Returns
    -------
    accepted : `bool`
    value : `int`
    """
    try:
        variable = int(env_variable)
    except ValueError:
        accepted = False
        variable = 0
        
    else:
        accepted = True
    
    return accepted, variable


def _get_env(name, default, accepted_type_name, accepted_processor, raise_if_missing_or_empty, warn_if_empty):
    """
    Gets the environmental variable for the given name. Processes and validates it.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `object`
        Default value to return.
    accepted_type_name : `str`
        The accepted type's name.
    accepted_type_processor : `(str) -> (bool, object)`
        Processor to process the environmental variable's value.
    raise_if_missing_or_empty : `bool`
        Whether exception should be thrown if the environmental variable is missing or empty.
    warn_if_empty : `bool`
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    return_type : `int`
    return_value / error_message : `object` / `str`
        Returns the returns' type and its value.
    """
    env_variable = get_environmental_variable(name)
    if env_variable is None:
        if raise_if_missing_or_empty:
            yield RETURN_TYPE_EXCEPTION, f'Environmental variable {name!r} is missing. {ERROR_MESSAGE_APPENDIX}'
            return
        
        yield RETURN_TYPE_VALUE, default
        return
    
    accepted, value = accepted_processor(env_variable)
    if accepted:
        yield RETURN_TYPE_VALUE, value
        return
    
    if env_variable:
        yield (
            RETURN_TYPE_WARNING,
            f'{name!r} is specified as non {accepted_type_name}: {env_variable!r}, defaulting to {default!r}!'
        )
    else:
        if raise_if_missing_or_empty:
            yield (
                RETURN_TYPE_EXCEPTION,
                f'Environmental variable {name!r} is specified as empty string. {ERROR_MESSAGE_APPENDIX}'
            )
            return
        
        if warn_if_empty:
            yield (
                RETURN_TYPE_WARNING,
                f'Environmental variable {name!r} is specified as empty string. Defaulting to {default!r}!',
            )
    
    yield RETURN_TYPE_VALUE, default


def _handle_get_env_generator(generator):
    """
    Handles a ``_get_env`` generator.
    
    Parameters
    ----------
    generator : `iterable<(int, object)>`
        Generator to iterate over.
    
    Returns
    -------
    value : `object`
    
    Raises
    ------
    RuntimeError
    """
    for return_type, return_value in generator:
        if return_type == RETURN_TYPE_VALUE:
            return return_value
        
        if return_type == RETURN_TYPE_WARNING:
            warn(return_value, stacklevel = 3)
            continue
        
        if return_type == RETURN_TYPE_EXCEPTION:
            raise RuntimeError(return_value)


def get_bool_env(name, default = False, *, raise_if_missing_or_empty = False, warn_if_empty = True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or not present as a boolean's representation returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `bool` = `False`, Optional
        The default value of the respective variable.
    raise_if_missing_or_empty : `bool` = `False`, Optional (Keyword only)
        Whether exception should be thrown if the environmental variable is missing or empty.
        Has priority over `default` and `warn_if_empty`.
    warn_if_empty : `bool` = `True`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    variable : `bool`
    
    Raises
    ------
    RuntimeError
    """
    return _handle_get_env_generator(
        _get_env(name, default, 'bool', _process_bool_env, raise_if_missing_or_empty, warn_if_empty)
    )


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
    return _handle_get_env_generator(
        _get_env(name, default, 'str', _process_str_env, raise_if_missing_or_empty, warn_if_empty)
    )


def get_int_env(name, default = 0, *, raise_if_missing_or_empty = False, warn_if_empty = True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or present as non `int`, will return `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `int` = `0`, Optional
        The default value of the respective variable.
    raise_if_missing_or_empty : `bool` = `False`, Optional (Keyword only)
        Whether exception should be thrown if the environmental variable is missing or empty.
        Has priority over `default` and `warn_if_empty`.
    warn_if_empty : `bool` = `True`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    variable : `int`
    
    Raises
    ------
    RuntimeError
    """
    return _handle_get_env_generator(
        _get_env(name, default, 'int', _process_int_env, raise_if_missing_or_empty, warn_if_empty)
    )
