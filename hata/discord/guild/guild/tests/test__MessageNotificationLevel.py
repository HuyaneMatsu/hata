import vampytest

from ..preinstanced import MessageNotificationLevel


def test__MessageNotificationLevel__name():
    """
    Tests whether ``MessageNotificationLevel`` instance names are all strings.
    """
    for instance in MessageNotificationLevel.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__MessageNotificationLevel__value():
    """
    Tests whether ``MessageNotificationLevel`` instance values are all the expected value type.
    """
    for instance in MessageNotificationLevel.INSTANCES.values():
        vampytest.assert_instance(instance.value, MessageNotificationLevel.VALUE_TYPE)
