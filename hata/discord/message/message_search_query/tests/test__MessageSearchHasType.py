import vampytest

from ..preinstanced import MessageSearchHasType


@vampytest.call_from(MessageSearchHasType.INSTANCES.values())
def test__MessageSearchHasType__instances(instance):
    """
    Tests whether ``MessageSearchHasType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageSearchHasType``
        The instance to test.
    """
    vampytest.assert_instance(instance, MessageSearchHasType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MessageSearchHasType.VALUE_TYPE)
