import vampytest

from ..preinstanced import WebhookType


@vampytest.call_from(WebhookType.INSTANCES.values())
def test__WebhookType__instances(instance):
    """
    Tests whether ``WebhookType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``WebhookType``
        The instance to test.
    """
    vampytest.assert_instance(instance, WebhookType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, WebhookType.VALUE_TYPE)
