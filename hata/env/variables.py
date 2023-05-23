__all__ = (
    'ALLOW_DEBUG_MESSAGES', 'API_VERSION', 'CACHE_PRESENCE', 'CACHE_USER', 'CUSTOM_API_ENDPOINT', 'CUSTOM_CDN_ENDPOINT',
    'CUSTOM_DISCORD_ENDPOINT', 'CUSTOM_STATUS_ENDPOINT', 'DOCS_ENABLED', 'LIBRARY_AGENT_APPENDIX', 'LIBRARY_NAME',
    'LIBRARY_URL', 'LIBRARY_VERSION', 'MESSAGE_CACHE_SIZE', 'RICH_DISCORD_EXCEPTION'
)

import warnings

from .getters import get_bool_env, get_int_env, get_str_env
from .loading import find_dot_env_file, load_dot_env_from_file

# Load dotenv

dot_env_file_path = find_dot_env_file()
if (dot_env_file_path is not None):
    load_dot_env_from_file(dot_env_file_path).insert_to_environmental_variables().raise_if_failed()
del dot_env_file_path

# Get variables

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
    
    elif API_VERSION > 11:
        warnings.warn(
            f'`API_VERSION` given with a value greater than `11`, got {API_VERSION!r}, defaulting to '
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
