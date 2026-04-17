import vampytest

from ..preinstanced import ApplicationInteractionEventType


@vampytest.call_from(ApplicationInteractionEventType.INSTANCES.values())
def test__ApplicationInteractionEventType__instances(instance):
    """
    Tests whether ``ApplicationInteractionEventType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationInteractionEventType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationInteractionEventType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationInteractionEventType.VALUE_TYPE)
