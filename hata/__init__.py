# -*- coding: utf-8 -*-
__version__ = '20200223.1'

import sys
ASYNC_ONLY = ('async_only' in sys.argv) or ('async-only' in sys.argv)
del sys

# import general purpose
from .dereaddons_local import *

# import Async
from .eventloop import *
from .executor import *
from .futures import *
from .ios import *
# import http and ws
from .py_formdata import *
from .py_http import *
from .py_websocket import *


if ASYNC_ONLY:
    __all__ = (
        *dereaddons_local.__all__   ,
        *eventloop.__all__          ,
        *executor.__all__           ,
        *futures.__all__            ,
        *ios.__all__                ,
        *py_formdata.__all__        ,
        *py_http.__all__            ,
        *py_websocket.__all__       ,
            )

else:
    # import Discord
    from .activity import *
    from .application import *
    from .audit_logs import *
    from .channel import *
    from .client import *
    from .client_core import *
    from .color import *
    from .embed import *
    from .emoji import *
    from .exceptions import *
    from .guild import *
    from .http import *
    from .integration import *
    from .invite import *
    from .message import *
    from .oauth2 import *
    from .opus import *
    from .others import *
    from .parsers import *
    from .permission import *
    from .player import *
    from .role import *
    from .user import *
    from .voice_client import *
    from .webhook import *
    
#    # - import events - #
#    from .events import *
    
    __all__ = (
        *dereaddons_local.__all__   ,
        *eventloop.__all__          ,
        *executor.__all__           ,
        *futures.__all__            ,
        *ios.__all__                ,
        *py_formdata.__all__        ,
        *py_http.__all__            ,
        *py_websocket.__all__       ,
        *activity.__all__           ,
        *application.__all__        ,
        *audit_logs.__all__         ,
        *channel.__all__            ,
        *client.__all__             ,
        *client_core.__all__        ,
        *color.__all__              ,
        *embed.__all__              ,
        *emoji.__all__              ,
        *exceptions.__all__         ,
        *guild.__all__              ,
        *http.__all__               ,
        *integration.__all__        ,
        *invite.__all__             ,
        *message.__all__            ,
        *oauth2.__all__             ,
        *opus.__all__               ,
        *others.__all__             ,
        *parsers.__all__            ,
        *permission.__all__         ,
        *player.__all__             ,
        *role.__all__               ,
        *user.__all__               ,
        *voice_client.__all__       ,
        *webhook.__all__            ,
            )
