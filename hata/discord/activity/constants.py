__all__ = ()

from ..color import Color

from .preinstanced import ActivityType


ACTIVITY_CUSTOM_ID_DEFAULT = 'UNKNOWN'

ACTIVITY_CUSTOM_IDS = {
    ActivityType.spotify: 'spotify:1',
    ActivityType.custom: 'custom',
}

ACTIVITY_DEFAULT_NAME = 'Unknown'


ACTIVITY_COLOR_GAME = Color(0x7289da)
ACTIVITY_COLOR_STREAM = Color(0x593695)
ACTIVITY_COLOR_SPOTIFY = Color(0x1db954)
ACTIVITY_COLOR_NONE = Color()
