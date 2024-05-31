import vampytest

from ..preinstanced import MessageReferenceType


@vampytest.call_from(MessageReferenceType.INSTANCES.values())
def test__MessageReferenceType__instances(instance):
    """
    Tests whether ``MessageReferenceType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageReferenceType``
        The instance to test.
    """
    vampytest.assert_instance(instance, MessageReferenceType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MessageReferenceType.VALUE_TYPE)
