import vampytest

from ..base import AutoModerationRuleTriggerMetadataBase
from ..keyword import AutoModerationRuleTriggerMetadataKeyword
from ..keyword_preset import AutoModerationRuleTriggerMetadataKeywordPreset
from ..mention_spam import AutoModerationRuleTriggerMetadataMentionSpam

from ..utils import try_get_auto_moderation_trigger_metadata_type_from_data


def _iter_options():
    yield {}, AutoModerationRuleTriggerMetadataBase
    yield {'keyword_filter': None}, AutoModerationRuleTriggerMetadataKeyword
    yield {'presets': None}, AutoModerationRuleTriggerMetadataKeywordPreset
    yield {'mention_total_limit': None}, AutoModerationRuleTriggerMetadataMentionSpam
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__try_get_auto_moderation_trigger_metadata_type_from_data(input_data):
    """
    Tests whether ``try_get_auto_moderation_trigger_metadata_type_from_data`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to decide on.
    
    Returns
    -------
    metadata_type : `type<AutoModerationRuleTriggerMetadataBase>`
    """
    output = try_get_auto_moderation_trigger_metadata_type_from_data(input_data)
    vampytest.assert_subtype(output, AutoModerationRuleTriggerMetadataBase)
    return output
