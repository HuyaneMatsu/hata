import warnings

from ...backend.export import export

from .activity_base import *
from .activity_custom import *
from .activity_rich import *
from .activity_types import *
from .activity_unknown import *
from .flags import *
from .utils import *

from . import activity_types as ACTIVITY_TYPES

export(ACTIVITY_TYPES, 'ACTIVITY_TYPES')

__all__ = (
    'ACTIVITY_TYPES',
    'ActivityTypes',
    *activity_base.__all__,
    *activity_custom.__all__,
    *activity_rich.__all__,
    *activity_types.__all__,
    *activity_unknown.__all__,
    *flags.__all__,
    *utils.__all__,
)


class ActivityTypesType:
    """
    `ActivityTypes` is deprecated, please use ``ACTIVITY_TYPES`` instead.
    """
    def __getattr__(self, attribute_name):
        attribute_value = getattr(ACTIVITY_TYPES, attribute_name)
        
        warnings.warn(
            f'`ActivityTypes` is deprecated, and will be removed in 2021 September. Please use `ACTIVITY_TYPES` '
            'instead.',
            FutureWarning)
        
        return attribute_value

ActivityTypes = ActivityTypesType()
