# -*- coding: utf-8 -*-
__version__ = '1.0.37'

from .env import BACKEND_ONLY

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
