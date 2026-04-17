import vampytest

from ..preinstanced import MessageActivityType


@vampytest.call_from(MessageActivityType.INSTANCES.values())
def test__MessageActivityType__instances(instance):
    """
    Tests whether ``MessageActivityType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageActivityType``
        The instance to test.
    """
    vampytest.assert_instance(instance, MessageActivityType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MessageActivityType.VALUE_TYPE)
