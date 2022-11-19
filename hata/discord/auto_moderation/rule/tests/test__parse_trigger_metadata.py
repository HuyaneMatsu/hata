import vampytest

from ...trigger_metadata import AutoModerationRuleTriggerMetadataBase, AutoModerationRuleTriggerMetadataMentionSpam

from ..fields import parse_trigger_metadata
from ..preinstanced import AutoModerationRuleTriggerType


def test__parse_trigger_metadata():
    """
    Tests whether ``parse_trigger_metadata`` is working as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = 20)
    
    for input_data, metadata_type, expected_output in (
        ({}, AutoModerationRuleTriggerType.none, AutoModerationRuleTriggerMetadataBase()),
        ({'trigger_metadata': None}, AutoModerationRuleTriggerType.mention_spam, AutoModerationRuleTriggerMetadataMentionSpam()),
        ({'trigger_metadata': metadata.to_data(defaults = True)}, AutoModerationRuleTriggerType.mention_spam, metadata),
    ):
        output = parse_trigger_metadata(input_data, metadata_type)
        vampytest.assert_eq(output, expected_output)
