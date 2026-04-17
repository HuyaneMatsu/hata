import vampytest

from ..preinstanced import ApplicationEventWebhookState


@vampytest.call_from(ApplicationEventWebhookState.INSTANCES.values())
def test__ApplicationEventWebhookState__instances(instance):
    """
    Tests whether ``ApplicationEventWebhookState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationEventWebhookState``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationEventWebhookState)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationEventWebhookState.VALUE_TYPE)
