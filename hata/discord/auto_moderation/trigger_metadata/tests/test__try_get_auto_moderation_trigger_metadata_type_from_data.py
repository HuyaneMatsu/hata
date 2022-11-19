import vampytest

from ..base import AutoModerationRuleTriggerMetadataBase
from ..keyword import AutoModerationRuleTriggerMetadataKeyword
from ..keyword_preset import AutoModerationRuleTriggerMetadataKeywordPreset

from ..utils import try_get_auto_moderation_trigger_metadata_type_from_data


def test__try_get_auto_moderation_trigger_metadata_type_from_data():
    """
    Tests whether ``try_get_auto_moderation_trigger_metadata_type_from_data`` works as intended.
    """
    for data, expected_value in (
        ({}, AutoModerationRuleTriggerMetadataBase,),
        ({'keyword_filter': None}, AutoModerationRuleTriggerMetadataKeyword),
        ({'presets': None}, AutoModerationRuleTriggerMetadataKeywordPreset),
    ):
        type_ = try_get_auto_moderation_trigger_metadata_type_from_data(data)
        
        vampytest.assert_is(type_, expected_value)
