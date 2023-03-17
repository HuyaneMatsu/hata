__all__ = ()

from .base import AutoModerationRuleTriggerMetadataBase
from .keyword import AutoModerationRuleTriggerMetadataKeyword
from .keyword_preset import AutoModerationRuleTriggerMetadataKeywordPreset
from .mention_spam import AutoModerationRuleTriggerMetadataMentionSpam


def try_get_auto_moderation_trigger_metadata_type_from_data(data):
    """
    Tries to detect what type of auto moderation trigger metadata the given data is.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Auto moderation trigger metadata data.
    
    Returns
    -------
    metadata_type : `type<AutoModerationRuleTriggerMetadataBase>`
    """
    if ('keyword_filter' in data) or ('regex_patterns' in data):
        metadata_type = AutoModerationRuleTriggerMetadataKeyword
    elif ('presets' in data):
        metadata_type = AutoModerationRuleTriggerMetadataKeywordPreset
    elif ('mention_limit' in data):
        metadata_type = AutoModerationRuleTriggerMetadataMentionSpam
    else:
        metadata_type = AutoModerationRuleTriggerMetadataBase
    
    return metadata_type

