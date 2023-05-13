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

from .getters import *
from .loading import *
from .parsing import *
from .variables import *


__all__ = (
    *getters.__all__,
    *loading.__all__,
    *parsing.__all__,
    *variables.__all__,
)
