import vampytest

from ..preinstanced import WebhookType


def test__WebhookType__name():
    """
    Tests whether ``WebhookType`` instance names are all strings.
    """
    for instance in WebhookType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__WebhookType__value():
    """
    Tests whether ``WebhookType`` instance values are all the expected value type.
    """
    for instance in WebhookType.INSTANCES.values():
        vampytest.assert_instance(instance.value, WebhookType.VALUE_TYPE)
