__all__ = ()

from .preinstanced import ActivityType

ACTIVITY_CUSTOM_ID_DEFAULT = 'UNKNOWN'

ACTIVITY_CUSTOM_IDS = {
    ActivityType.spotify: 'spotify:1',
    ActivityType.custom: 'custom',
}

ACTIVITY_DEFAULT_NAME = 'Unknown'
