from .api_client import *
from .connector_cache import *
from .headers import *
from .rate_limit import *
from .rate_limit_groups import *
from .rate_limit_proxy import *
from .urls import *

from . import rate_limit_groups as RATE_LIMIT_GROUPS


__all__ = (
    'RATE_LIMIT_GROUPS',
    
    *api_client.__all__,
    *connector_cache.__all__,
    *headers.__all__,
    *rate_limit.__all__,
    *rate_limit_groups.__all__,
    *rate_limit_proxy.__all__,
    *urls.__all__,
)


# Deprecate imports

from scarletio.http_client import HTTPClient

from ...utils.module_deprecation import deprecated_import

# Deprecated at 2024 Jan 1
deprecated_import(HTTPClient, 'DiscordHTTPClient')
