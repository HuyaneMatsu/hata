from .embedded_activity import *
from .embedded_activity_location import *
from .embedded_activity_user_state import *


__all__ = (
    *embedded_activity.__all__,
    *embedded_activity_location.__all__,
    *embedded_activity_user_state.__all__,
)

# remove on 2025 February
from ...utils.module_deprecation import deprecated_import
deprecated_import(EmbeddedActivity, 'EmbeddedActivityState')
