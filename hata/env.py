# -*- coding: utf-8 -*-
"""
Before loading hata, it checks for related envirnormental variables, which are:

HATA_BACKEND_ONLY : `bool` = `False`
    whether `hata.discord` should be imported as well.

HATA_ALLOW_DEAD_EVENTS : `bool` = `False`
    Whether events of non cached entities should be handled. Affetcs the following events right now:
    
    - `client.events.message_edit`
    - `client.events.message_delete`
    - `client.events.reaction_add`
    - `client.events.reaction_clear`
    - `client.events.reaction_delete`
    - `client.events.reaction_delete_emoji`

HATA_CACHE_PRESENCE : `bool` = `True`
    Whether hata should enable and dispatch users prezence related events. By disabling it, `user.status`,
    `user.statuses`, `user.platform`, `user.activtiies`, `user.activity` will be disabled. And each will be replaced
    by a dummy property.
    
    If `HATA_CACHE_USERS` is defined as `False`, `HATA_CACHE_PRESENCE` will be set as `False` as well.

HATA_CACHE_USERS : `bool` = `True`
    Whether hata should cache users. Disabling it can cause many hata features to disappear.

HATA_API_ENDPOINT : `None`, `str` = `None`
    The api endpoint to use instead of the Discord's default.

HATA_CDN_ENDPOINT : `None`, `str` = `None`
    The cdn (content delivery network) endpoint to use instead of the Discord's default.

HATA_DIS_ENDPOINT : `None`, `str` = `None`
    The endpoint of Discord, to use instead of it's own.
"""
import os, warnings

def get_bool_env(name, default):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or not present as a bool's representation returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an enviromental variable.
    default : `bool`
        The default value of the respective variable.
    
    Returns
    -------
    env_variable : `bool`
    """
    env_variable = os.getenv(name)
    if env_variable is None:
        return default
    
    if env_variable == 'True':
        return True
    
    if env_variable == 'False':
        return False
    
    warnings.warn(f'{name!r} is specified as non bool: {env_variable!r}, defaulting to {default!r}!')
    return default

def get_str_env(name, default=None):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or present as an empty string returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an enviromental variable.
    default : `Any`, Optional
        The default value of the respective variable. Defaults to `None`
    
    Returns
    -------
    variable : `str` or `default`
    """
    env_variable = os.getenv(name)
    if env_variable is None:
        return default
    
    if env_variable:
        return env_variable
    
    warnings.warn(f'{name!r} is specified as empty string: {env_variable!r}, defaulting to {default!r}!')
    return default


BACKEND_ONLY = get_bool_env('HATA_BACKEND_ONLY', False)
CACHE_PRESENCE = get_bool_env('HATA_CACHE_PRESENCE', True)
CACHE_USER = get_bool_env('HATA_CACHE_USERS', True)

# You cannot store presences of not loaded users.
if (not CACHE_USER):
    CACHE_PRESENCE = False

ALLOW_DEAD_EVENTS = get_bool_env('HATA_ALLOW_DEAD_EVENTS', False)

CUSTOM_API_ENDPOINT = get_str_env('HATA_API_ENDPOINT')
CUSTOM_CDN_ENDPOINT = get_str_env('HATA_CDN_ENDPOINT')
CUSTOM_DIS_ENDPOINT = get_str_env('HATA_DIS_ENDPOINT')
