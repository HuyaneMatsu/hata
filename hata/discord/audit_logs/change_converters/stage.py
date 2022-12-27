__all__ = ()

from .scheduled_event import convert_privacy_level
from .shared import convert_nothing


STAGE_CONVERTERS = {
    'name': convert_nothing,
    'privacy_level': convert_privacy_level,
    'topic': convert_nothing,
}
