__all__ = ()

from .application_command import APPLICATION_COMMAND_CONVERTERS
from .auto_moderation_rule import AUTO_MODERATION_RULE_CONVERTERS
from .channel import CHANNEL_CONVERTERS
from .channel_permission_overwrite import CHANNEL_PERMISSION_OVERWRITE_CONVERTERS
from .emoji import EMOJI_CONVERTERS
from .guild import GUILD_CONVERTERS
from .integration import INTEGRATION_CONVERTERS
from .invite import INVITE_CONVERTERS
from .role import ROLE_CONVERTERS
from .scheduled_event import SCHEDULED_EVENT_CONVERTERS
from .stage import STAGE_CONVERTERS
from .sticker import STICKER_CONVERTERS
from .user import USER_CONVERTERS
from .webhook import WEBHOOK_CONVERTERS


def merge_converters(*converters_to_merge):
    """
    Merges the given converter groups.
    
    Parameters
    ----------
    converters_to_merge : `dict` of (`str`, `FunctionType`) items
        Audit log change converters.
    
    Returns
    -------
    merged_converters : `dict` of (`str`, `FunctionType`) items
    """
    multi_type_converters = set()
    merged_converters = {}
    
    for converters in converters_to_merge:
        for key, converter in converters.items():
            if key in multi_type_converters:
                continue
            
            try:
                actual_converter = merged_converters[key]
            except KeyError:
                merged_converters[key] = converter
                continue
            
            if actual_converter is converter:
                continue
            
            del merged_converters[key]
            multi_type_converters.add(key)
            continue
    
    return merged_converters


MERGED_CONVERTERS = merge_converters(
    APPLICATION_COMMAND_CONVERTERS,
    CHANNEL_CONVERTERS,
    AUTO_MODERATION_RULE_CONVERTERS,
    CHANNEL_PERMISSION_OVERWRITE_CONVERTERS,
    EMOJI_CONVERTERS,
    GUILD_CONVERTERS,
    INTEGRATION_CONVERTERS,
    INVITE_CONVERTERS,
    ROLE_CONVERTERS,
    SCHEDULED_EVENT_CONVERTERS,
    STAGE_CONVERTERS,
    STICKER_CONVERTERS,
    USER_CONVERTERS,
    WEBHOOK_CONVERTERS,
)
