import vampytest

from ...trigger_metadata import AutoModerationRuleTriggerMetadataBase

from ..preinstanced import AutoModerationRuleTriggerType


def _assert_fields_set(auto_moderation_rule_trigger_type):
    """
    Asserts whether every field are set of the given auto moderation rule trigger type.
    
    Parameters
    ----------
    auto_moderation_rule_trigger_type : ``AutoModerationRuleTriggerType``
        The instance to test.
    """
    vampytest.assert_instance(auto_moderation_rule_trigger_type, AutoModerationRuleTriggerType)
    vampytest.assert_instance(auto_moderation_rule_trigger_type.name, str)
    vampytest.assert_instance(auto_moderation_rule_trigger_type.value, AutoModerationRuleTriggerType.VALUE_TYPE)
    vampytest.assert_instance(auto_moderation_rule_trigger_type.max_per_guild, int)
    vampytest.assert_subtype(auto_moderation_rule_trigger_type.metadata_type, AutoModerationRuleTriggerMetadataBase)


@vampytest.call_from(AutoModerationRuleTriggerType.INSTANCES.values())
def test__AutoModerationRuleTriggerType__instances(instance):
    """
    Tests whether ``AutoModerationRuleTriggerType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AutoModerationRuleTriggerType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__AutoModerationRuleTriggerType__new__min_fields():
    """
    Tests whether ``AutoModerationRuleTriggerType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = AutoModerationRuleTriggerType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, AutoModerationRuleTriggerType.NAME_DEFAULT)
        vampytest.assert_is(output.metadata_type, AutoModerationRuleTriggerMetadataBase)
        vampytest.assert_is(AutoModerationRuleTriggerType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del AutoModerationRuleTriggerType.INSTANCES[value]
        except KeyError:
            pass
