import vampytest

from ..preinstanced import MessageSearchAuthorType


@vampytest.call_from(MessageSearchAuthorType.INSTANCES.values())
def test__MessageSearchAuthorType__instances(instance):
    """
    Tests whether ``MessageSearchAuthorType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageSearchAuthorType``
        The instance to test.
    """
    vampytest.assert_instance(instance, MessageSearchAuthorType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MessageSearchAuthorType.VALUE_TYPE)
