__all__ = ('register',)

from functools import partial as partial_func

from .command import Command, CommandCategory, CommandFunction
from .command.helpers import get_function_description, get_function_name


def register(func = ..., *, alters = None, description = None, into = None, name = None):
    """
    Registers the given command.
    
    Parameters
    ----------
    func : `None`, `FunctionType`
        The function to register.
    alters : `None`, `str`, `iterable` of `str` = `None`, Optional (Keyword only)
        Alternative names for the command.
    description : `None`, `str` = `None`, Optional (Keyword only)
        Alternative description to use instead of the function's.
    into : `None`, ``Command``, ``CommandCategory``, ``CommandFunction`` = `None`, Optional (Keyword only)
        The command to register currently added one into.
    name : `None`, `str` = `None`, Optional (Keyword only)
        Alternative name to use instead of the function's.
    
    Returns
    -------
    command / decorator : ``Command``, ``CommandFunction`` / `functools.partial`
        The registered command or a partial function to add it.
    
    Raises
    ------
    TypeError
        - Invalid parameter type.
    RuntimeError
        - `into`'s parent command already garbage collected.
    """
    if func is ...:
        return partial_func(register, alters = alters, description = description, into = into, name = name)
    
    name = get_function_name(func, name)
    description = get_function_description(func, description)
    
    if (into is None):
        command = Command(name, alters)
    
    elif isinstance(into, Command):
        command = into
    
    elif isinstance(into, CommandCategory):
        command = into
    
    elif isinstance(into, CommandFunction):
        command = into.get_parent()
        if (command is None):
            raise RuntimeError(
                f'`into`\'s parent already garbage collected, got {into!r}.'
            )
    else:
        raise TypeError(
            f'`into` can be `None`, `{Command.__name__}`, `{CommandCategory.__name__}`, `{CommandFunction.__name__}`,'
            f' got {into.__class__.__name__}; {into!r}.'
        )
    
    if (func is not None):
        command = command.register_command_function(func, name, description)
    elif (into is not None):
        command = command.register_command_category(name)
    
    return command
