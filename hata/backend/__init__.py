import scarletio

from scarletio import *
from scarletio.http_client import *
from scarletio.websocket import *
from scarletio.web_common import *


from scarletio import http_client
from scarletio import websocket
from scarletio import web_common

__all__ = (
    *scarletio.__all__,
    *http_client.__all__,
    *websocket.__all__,
    *web_common.__all__,
)

import warnings

warnings.warn(
    (
        f'Hata\'s backend has been moved out to a separate library.\n'
        f'Please import from `scarletio` instead.'
    ),
    FutureWarning,
    stacklevel = 3,
)
