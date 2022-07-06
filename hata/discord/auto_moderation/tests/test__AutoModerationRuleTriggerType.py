import vampytest

from .. import AutoModerationRuleTriggerType, AutoModerationRuleTriggerMetadata


def test__AutoModerationRuleTriggerType__name():
    for instance in AutoModerationRuleTriggerType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__AutoModerationRuleTriggerType__value():
    for instance in AutoModerationRuleTriggerType.INSTANCES.values():
        vampytest.assert_instance(instance.value, AutoModerationRuleTriggerType.VALUE_TYPE)


def test__AutoModerationRuleTriggerType__max_per_guild():
    for instance in AutoModerationRuleTriggerType.INSTANCES.values():
        vampytest.assert_instance(instance.max_per_guild, int)


def test__AutoModerationRuleTriggerType__metadata_type():
    for instance in AutoModerationRuleTriggerType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, AutoModerationRuleTriggerMetadata, nullable=True)
