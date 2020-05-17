# -*- coding: utf-8 -*-
__version__ = '1.0.9'

import sys
BACKEND_ONLY = ('backend_only' in sys.argv) or ('backend-only' in sys.argv)
del sys

if BACKEND_ONLY:
    from .backend import *
    __all__ = backend.__all__

else:
    from .backend import *
    from .discord import *
    
    __all__ = (
        *backend.__all__,
        *discord.__all__,
            )
