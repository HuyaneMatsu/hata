__all__ = ()

from ...utils import seconds_to_id_difference

from ..interaction_metadata import InteractionMetadataBase


INTERACTION_EVENT_EXPIRE_AFTER = 900 # 15 min
INTERACTION_EVENT_EXPIRE_AFTER_ID_DIFFERENCE = seconds_to_id_difference(INTERACTION_EVENT_EXPIRE_AFTER)

DEFAULT_INTERACTION_METADATA = InteractionMetadataBase()
