from .fields import *
from .metadata import *

from .activity import *
from .constants import *
from .flags import *
from .preinstanced import *

__all__ = (
    *fields.__all__,
    *metadata.__all__,
        
    *activity.__all__,
    *constants.__all__,
    *flags.__all__,
    *preinstanced.__all__,
)

# Construct deprecations

from scarletio import modulize

from ...utils.module_deprecation import deprecated_import


@deprecated_import
@modulize
class ACTIVITY_TYPES:
    """
    Deprecated. Please use ``ActivityType`` instead.
    """
    game = 0
    stream = 1
    spotify = 2
    watching = 3
    custom = 4
    competing = 5


deprecated_import(Activity, 'ActivityRich')
