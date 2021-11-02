"""
Before loading hata, it checks for related environmental variables, which are:

HATA_BACKEND_ONLY : `bool` = `False`
    Whether `hata.discord` should not be imported as well.

HATA_ALLOW_DEAD_EVENTS : `bool` = `False`
    Whether events of non cached entities should be handled. Affects the following events right now:
    
    - `Client.events.message_edit`
    - `Client.events.message_delete`
    - `Client.events.reaction_add`
    - `Client.events.reaction_clear`
    - `Client.events.reaction_delete`
    - `Client.events.reaction_delete_emoji`

HATA_CACHE_PRESENCE : `bool` = `True`
    Whether hata should enable presence related attributes and dispatch users presence related events. By disabling it,
    ``User.status``, ``User.statuses``, ``User.platform``, ``User.activities``, ``User.activity`` will be disabled. And
    each will be replaced by a dummy property.
    
    If `HATA_CACHE_USERS` is defined as `False`, `HATA_CACHE_PRESENCE` will be set as `False` as well.

HATA_CACHE_USERS : `bool` = `True`
    Whether hata should cache users. Disabling it can cause many hata features to disappear.

HATA_MESSAGE_CACHE_SIZE : `int` = `10`
    The default message cache size per channel.

HATA_API_ENDPOINT : `None`, `str` = `None`
    The api endpoint to use instead of the Discord's default.

HATA_CDN_ENDPOINT : `None`, `str` = `None`
    The cdn (content delivery network) endpoint to use instead of the Discord's default.

HATA_DISCORD_ENDPOINT : `None`, `str` = `None`
    The endpoint of Discord, to use instead of it's own.

HATA_STATUS_ENDPOINT : `None`, `str` = `None`
    Discord status endpoint.

HATA_API_VERSION : `int` = `9`
    The Discord api version used by hata. The accepted values are `6`, `7`, `8` and `9`.
    
    If given as any other value, a warning message will show up. Tho, if given `6` a deprecation warning will be still
    present.

HATA_DOCS_ENABLED : `bool` = `True`
    Whether hata should be loaded with docstrings.
    
    > Experimental, not the full wrappers supports it yet.
    
    If python is run with `-OO`, then this always defaults to `False`.
"""
import warnings
from os import getenv as get_environmental_variable

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    pass
else:
    load_dotenv()


def get_bool_env(name, default, *, warn_if_empty=True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or not present as a bool's representation returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `bool`
        The default value of the respective variable.
    warn_if_empty : `bool`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    env_variable : `bool`
    """
    env_variable = get_environmental_variable(name)
    if env_variable is None:
        return default
    
    if env_variable == 'True':
        return True
    
    if env_variable == 'False':
        return False
    
    if warn_if_empty:
        warnings.warn(f'{name!r} is specified as non bool: {env_variable!r}, defaulting to {default!r}!')
    
    return default


def get_str_env(name, default=None, *, warn_if_empty=True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or present as an empty string returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `Any`, Optional
        The default value of the respective variable. Defaults to `None`.
    warn_if_empty : `bool`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    variable : `str` or `default`
    """
    env_variable = get_environmental_variable(name)
    if env_variable is None:
        return default
    
    if env_variable:
        return env_variable
    
    if warn_if_empty:
        warnings.warn(f'{name!r} is specified as empty string: {env_variable!r}, defaulting to {default!r}!')
    
    return default


def get_int_env(name, default, *, warn_if_empty=True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or present as non `int`, will return `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `int`
        The default value of the respective variable.
    warn_if_empty : `bool`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    variable : `int` or `default`
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
        warnings.warn(f'{name!r} is specified as non `int`: {env_variable!r}, defaulting to {default!r}!')
    
    return default


BACKEND_ONLY = get_bool_env('HATA_BACKEND_ONLY', False)
CACHE_PRESENCE = get_bool_env('HATA_CACHE_PRESENCE', True)
CACHE_USER = get_bool_env('HATA_CACHE_USERS', True)
MESSAGE_CACHE_SIZE = get_int_env('HATA_MESSAGE_CACHE_SIZE', 10)

if (MESSAGE_CACHE_SIZE < 0):
    MESSAGE_CACHE_SIZE = 0

DOCS_ENABLED = get_bool_env('HATA_DOCS_ENABLED', (get_bool_env is not None))
if not DOCS_ENABLED:
    get_bool_env.__doc__ = None
    get_str_env.__doc__ = None
    get_int_env.__doc__ = None

# You cannot store presences of not loaded users.
if (not CACHE_USER):
    CACHE_PRESENCE = False

ALLOW_DEAD_EVENTS = get_bool_env('HATA_ALLOW_DEAD_EVENTS', False)

CUSTOM_API_ENDPOINT = get_str_env('HATA_API_ENDPOINT')
CUSTOM_CDN_ENDPOINT = get_str_env('HATA_CDN_ENDPOINT')
CUSTOM_DISCORD_ENDPOINT = get_str_env('HATA_DISCORD_ENDPOINT')
CUSTOM_STATUS_ENDPOINT = get_str_env('HATA_STATUS_ENDPOINT')

API_VERSION = get_int_env('HATA_API_VERSION', 9)

if API_VERSION not in (7, 8):
    if API_VERSION < 6:
        warnings.warn(f'`API_VERSION` given with a value less than `6`, got {API_VERSION!r}, defaulting to {7!r}!')
        API_VERSION = 7
    elif API_VERSION > 9:
        warnings.warn(f'`API_VERSION` given with a value greater than `9`, got {API_VERSION!r}, defaulting to {9!r}!')
        API_VERSION = 9
    elif API_VERSION == 6:
        warnings.warn('`API_VERSION` given as 6, please use version `7` or `8`.', FutureWarning)
