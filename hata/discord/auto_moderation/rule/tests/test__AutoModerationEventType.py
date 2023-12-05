import vampytest

from ..preinstanced import AutoModerationEventType


@vampytest.call_from(AutoModerationEventType.INSTANCES.values())
def test__AutoModerationEventType__instances(instance):
    """
    Tests whether ``AutoModerationEventType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AutoModerationEventType``
        The instance to test.
    """
    vampytest.assert_instance(instance, AutoModerationEventType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, AutoModerationEventType.VALUE_TYPE)
