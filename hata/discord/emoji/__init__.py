from .emoji import *
from .parsing import *
from .reaction import *
from .reaction_events import *
from .unicode import *


__all__ = (
    *emoji.__all__,
    *parsing.__all__,
    *reaction.__all__,
    *reaction_events.__all__,
    *unicode.__all__,
)

# Deprecations

from ...utils.module_deprecation import deprecated_import

deprecated_import(ReactionMapping, 'reaction_mapping')
deprecated_import(ReactionMappingLine, 'reaction_mapping_line')
