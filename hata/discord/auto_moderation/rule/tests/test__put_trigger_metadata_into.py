import vampytest

from ...trigger_metadata import AutoModerationRuleTriggerMetadataBase, AutoModerationRuleTriggerMetadataMentionSpam

from ..fields import put_trigger_metadata_into


def test__put_trigger_metadata_into():
    """
    Tests whether ``put_trigger_metadata_into`` is working as intended.
    """
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = 20)
    
    for input_value, defaults, expected_output in (
        (AutoModerationRuleTriggerMetadataBase(), False, {}),
        (AutoModerationRuleTriggerMetadataBase(), True, {'trigger_metadata': {}}),
        (metadata, False, {'trigger_metadata': metadata.to_data(defaults = False)}),
    ):
        data = put_trigger_metadata_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
