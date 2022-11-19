import vampytest

from ...trigger_metadata import AutoModerationRuleTriggerMetadataBase

from ..preinstanced import AutoModerationRuleTriggerType


def test__AutoModerationRuleTriggerType__name():
    """
    Tests whether ``AutoModerationRuleTriggerType`` instance names are all strings.
    """
    for instance in AutoModerationRuleTriggerType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationRuleTriggerType__value():
    """
    Tests whether ``AutoModerationRuleTriggerType`` instance values are all the expected value type.
    """
    for instance in AutoModerationRuleTriggerType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationRuleTriggerType.VALUE_TYPE)


def test__AutoModerationRuleTriggerType__max_per_guild():
    """
    Tests whether ``AutoModerationRuleTriggerType`` instance `.max_per_guild`-s are all ints.
    """
    for instance in AutoModerationRuleTriggerType.INSTANCES.values():
        vampytest.assert_instance(instance.max_per_guild, int)


def test__AutoModerationRuleTriggerType__metadata_type():
    """
    Tests whether ``AutoModerationRuleTriggerType`` instance `.metadata_type`-s are all set correctly.
    """
    for instance in AutoModerationRuleTriggerType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, AutoModerationRuleTriggerMetadataBase)
