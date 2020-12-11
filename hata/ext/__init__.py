# -*- coding: utf-8 -*-
"""
Hata extensions come into this folder.

If a hata library extension is imported, it should register itself with the ``register_library_extension``, so if an
other library extension is imported, it can register a hook to run only if both are imported.

Hook registrations can be done with the ``add_library_extension_hook`` function.
"""
import warnings
from ..discord.client_core import KOKORO

HOOKS = []

LOADED_EXTENSIONS = set()

def register_library_extension(extension_name):
    """
    Registers a library extension, calling respective hooks if applicable.
    
    Parameters
    ----------
    extension_name : `str`
        The library extension's name.
    """
    if extension_name in LOADED_EXTENSIONS:
        warnings.warn(f'A library extension with name {extension_name!r} is already loaded.')
        return
    
    LOADED_EXTENSIONS.add(extension_name)
    
    for index in reversed(range(len(HOOKS))):
        requirements, hook = HOOKS[index]
        try:
            requirements.discard(extension_name)
        except KeyError:
            continue
        
        if requirements:
            continue
        
        del HOOKS[index]
        
        try:
            hook()
        except BaseException as err:
            KOKORO.render_exc_maybe_async(err, [
                'register_library_extension(', repr(extension_name), ') ignores occured extesnion meanwhile calling ',
                repr(hook), ' satisfied library extension hook.\n.'
                    ])


def add_library_extension_hook(hook, requirements):
    """
    Adds a library extension hook, what is called, when the ginve `requirements` are satisfied.
    
    Parameters
    ----------
    hook : `callable`
        Library extension hook called when all the required extensions are loaded as well.
    requirements : `iterable` of `str`
        An iterable of library extension names, which need to be resolved before calling the respective hook.
    """
    requirements_set = set(requirements)
    requirements_set.difference_update(LOADED_EXTENSIONS)
    
    if requirements_set:
        HOOKS.append((requirements_set, hook))
        return
    
    try:
        hook()
    except BaseException as err:
        KOKORO.render_exc_maybe_async(err, [
            'add_library_extension_hook(', repr(hook), ', ', repr(requirements), ') ignores occured extesnion '
            'meanwhile calling ', repr(hook), ' satisfied library extension hook.\n.'
                ])
