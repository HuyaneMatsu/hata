# -*- coding: utf-8 -*-
import os, warnings

def get_bool_env(name, default):
    env_variable = os.getenv(name)
    if env_variable is None:
        return default
    
    if env_variable == 'True':
        return True
    
    if env_variable == 'False':
        return False
    
    warnings.warn(f'{name!r} is specified as non bool: {env_variable!r}, defaulting to {default!r}!')
    return default

BACKEND_ONLY = get_bool_env('HATA_BACKEND_ONLY', False)
CACHE_USER = get_bool_env('HATA_CACHE_USERS', True)
CACHE_PRESENCE = get_bool_env('HATA_CACHE_PRESENCE', True)

# You cannot store presences of not loaded users.
if (not CACHE_USER):
    CACHE_PRESENCE = False
