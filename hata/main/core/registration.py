__all__ = ('register',)

from functools import partial as partial_func

from .command import Command
from .command.helpers import get_function_description, get_function_name


def register(func=..., *, alters=None, description=None, name=None):
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
    name : `None`, `str` = `None`, Optional (Keyword only)
        Alternative name to use instead of the function's.
    
    Returns
    -------
    command / decorator : ``Command`` / `functools.partial`
        The registered command or a partial function to add it.
    """
    if func is ...:
        return partial_func(register, alters=alters, description=description, name=name)
    
    name = get_function_name(func, name)
    description = get_function_description(func, description)
    
    command = Command(name, description, alters)
    
    if (func is not None):
        command.register_command_function(func, name, description)
    
    return command
