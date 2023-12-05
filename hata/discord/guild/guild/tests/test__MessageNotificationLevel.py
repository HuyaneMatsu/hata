import vampytest

from ..preinstanced import MessageNotificationLevel


@vampytest.call_from(MessageNotificationLevel.INSTANCES.values())
def test__MessageNotificationLevel__instances(instance):
    """
    Tests whether ``MessageNotificationLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageNotificationLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, MessageNotificationLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MessageNotificationLevel.VALUE_TYPE)
