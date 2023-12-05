import vampytest

from ...trigger_metadata import AutoModerationRuleTriggerMetadataBase

from ..preinstanced import AutoModerationRuleTriggerType


@vampytest.call_from(AutoModerationRuleTriggerType.INSTANCES.values())
def test__AutoModerationRuleTriggerType__instances(instance):
    """
    Tests whether ``AutoModerationRuleTriggerType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AutoModerationRuleTriggerType``
        The instance to test.
    """
    vampytest.assert_instance(instance, AutoModerationRuleTriggerType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, AutoModerationRuleTriggerType.VALUE_TYPE)
    vampytest.assert_instance(instance.max_per_guild, int)
    vampytest.assert_subtype(instance.metadata_type, AutoModerationRuleTriggerMetadataBase)
