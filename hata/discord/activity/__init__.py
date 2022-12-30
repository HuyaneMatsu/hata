from .activity import *
from .activity_assets import *
from .activity_field_base import *
from .activity_metadata import *
from .activity_party import *
from .activity_timestamps import *


__all__ = (
    *activity.__all__,
    *activity_assets.__all__,
    *activity_field_base.__all__,
    *activity_metadata.__all__,
    *activity_party.__all__,
    *activity_timestamps.__all__,
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
