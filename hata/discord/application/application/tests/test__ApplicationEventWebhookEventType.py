import vampytest

from ..preinstanced import ApplicationEventWebhookEventType


@vampytest.call_from(ApplicationEventWebhookEventType.INSTANCES.values())
def test__ApplicationEventWebhookEventType__instances(instance):
    """
    Tests whether ``ApplicationEventWebhookEventType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationEventWebhookEventType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationEventWebhookEventType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationEventWebhookEventType.VALUE_TYPE)
