"""
Before loading hata, it checks for related environmental variables, which are:

HATA_ALLOW_DEBUG_MESSAGES : `bool` = `False`
    Whether debug messages should be show (experimental).

HATA_API_ENDPOINT : `None`, `str` = `None`
    The api endpoint to use instead of the Discord's default.

HATA_API_VERSION : `int` = `10`
    The Discord api version used by hata. The accepted values are `6`, `7`, `8`, `9` and `10`.
    
    If given as any other value, a warning message will show up. Tho, if given `6` a deprecation warning will be still
    present.

HATA_CACHE_PRESENCE : `bool` = `True`
    Whether hata should enable presence related attributes and dispatch users presence related events. By disabling it,
    ``User.status``, ``User.statuses``, ``User.platform``, ``User.activities``, ``User.activity`` will be disabled. And
    each will be replaced by a dummy property.
    
    If `HATA_CACHE_USERS` is defined as `False`, `HATA_CACHE_PRESENCE` will be set as `False` as well.

HATA_CACHE_USERS : `bool` = `True`
    Whether hata should cache users. Disabling it can cause many hata features to disappear.

HATA_CDN_ENDPOINT : `None`, `str` = `None`
    The cdn (content delivery network) endpoint to use instead of the Discord's default.

HATA_DISCORD_ENDPOINT : `None`, `str` = `None`
    The endpoint of Discord, to use instead of it's own.

HATA_DOCS_ENABLED : `bool` = `True`
    Whether hata should be loaded with docstrings.
    
    > Experimental, not the full wrappers supports it yet.
    
    If python is run with `-OO`, then this always defaults to `False`.

HATA_LIBRARY_AGENT_APPENDIX : `str` = `None`
    Library agent appendix used instead of the default generated one.

HATA_LIBRARY_NAME : `str` = `'hata'`
    Library name used when identifying.

HATA_LIBRARY_URL : `str` = `'https://github.com/HuyaneMatsu/hata'`
    Library url used at user agents.

HATA_LIBRARY_VERSION : `str` = `None`
    Library version used in user agents.

HATA_MESSAGE_CACHE_SIZE : `int` = `10`
    The default message cache size per channel.

HATA_RICH_DISCORD_EXCEPTION : `bool` = `False`
    Whether ``DiscordException``-s should show the request data as well.

HATA_STATUS_ENDPOINT : `None`, `str` = `None`
    Discord status endpoint.
"""
import warnings
from os import getenv as get_environmental_variable


try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    pass
else:
    load_dotenv()


__all__ = (
    'API_VERSION', 'CACHE_PRESENCE', 'CACHE_USER', 'CUSTOM_API_ENDPOINT', 'CUSTOM_CDN_ENDPOINT',
    'CUSTOM_DISCORD_ENDPOINT', 'CUSTOM_STATUS_ENDPOINT', 'DOCS_ENABLED', 'LIBRARY_URL', 'MESSAGE_CACHE_SIZE',
    'RICH_DISCORD_EXCEPTION'
)

def get_bool_env(name, default, *, warn_if_empty = True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or not present as a boolean's representation returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `bool`
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
    
    if env_variable == 'True':
        return True
    
    if env_variable == 'False':
        return False
    
    if warn_if_empty:
        warnings.warn(
            f'{name!r} is specified as non bool: {env_variable!r}, defaulting to {default!r}!',
        )
    
    return default


def get_str_env(name, default = None, *, warn_if_empty = True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or present as an empty string returns `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `Any` = `None`, Optional
        The default value of the respective variable. Defaults to `None`.
    warn_if_empty : `bool` = `True`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    variable : `str`, `default`
    """
    env_variable = get_environmental_variable(name)
    if env_variable is None:
        return default
    
    if env_variable:
        return env_variable
    
    if warn_if_empty:
        warnings.warn(
            f'{name!r} is specified as empty string: {env_variable!r}, defaulting to {default!r}!',
        )
    
    return default


def get_int_env(name, default, *, warn_if_empty = True):
    """
    Gets the given environmental variable.
    
    If the environmental variable is not present or present as non `int`, will return `default` instead.
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `int`
        The default value of the respective variable.
    warn_if_empty : `bool` = `True`, Optional (Keyword only)
        Whether warning should be dropped if empty environmental variable is received.
    
    Returns
    -------
    variable : `int`, `default`
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

ALLOW_DEBUG_MESSAGES = get_bool_env('HATA_ALLOW_DEBUG_MESSAGES', False)

CUSTOM_API_ENDPOINT = get_str_env('HATA_API_ENDPOINT')
CUSTOM_CDN_ENDPOINT = get_str_env('HATA_CDN_ENDPOINT')
CUSTOM_DISCORD_ENDPOINT = get_str_env('HATA_DISCORD_ENDPOINT')
CUSTOM_STATUS_ENDPOINT = get_str_env('HATA_STATUS_ENDPOINT')

DEFAULT_API_VERSION = 10
API_VERSION = get_int_env('HATA_API_VERSION', DEFAULT_API_VERSION)

if API_VERSION != DEFAULT_API_VERSION:
    if API_VERSION < 6:
        warnings.warn(
            f'`HATA_API_VERSION` given with a value less than `6`, got {API_VERSION!r}, defaulting to '
            f'{DEFAULT_API_VERSION!r}!'
        )
        API_VERSION = DEFAULT_API_VERSION
    
    elif API_VERSION > 10:
        warnings.warn(
            f'`API_VERSION` given with a value greater than `10`, got {API_VERSION!r}, defaulting to '
            f'{DEFAULT_API_VERSION!r}!'
        )
        API_VERSION = DEFAULT_API_VERSION
    
    elif API_VERSION < 9:
        warnings.warn(
            (
                f'`API_VERSION` given either as `6`, `7`, `8`, got {API_VERSION!r}, please use version '
                f'`{DEFAULT_API_VERSION!r}` instead',
            ),
            FutureWarning,
        )


LIBRARY_AGENT_APPENDIX = get_str_env('HATA_LIBRARY_AGENT_APPENDIX', None)
LIBRARY_NAME = get_str_env('HATA_LIBRARY_NAME', 'hata')
LIBRARY_URL = get_str_env('HATA_LIBRARY_URL', 'https://github.com/HuyaneMatsu/hata')
LIBRARY_VERSION = get_str_env('HATA_LIBRARY_VERSION', None)


RICH_DISCORD_EXCEPTION = get_bool_env('HATA_RICH_DISCORD_EXCEPTION', False)
