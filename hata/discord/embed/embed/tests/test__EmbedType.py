import vampytest

from ..preinstanced import EmbedType


@vampytest.call_from(EmbedType.INSTANCES.values())
def test__EmbedType__instances(instance):
    """
    Tests whether ``EmbedType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``EmbedType``
        The instance to test.
    """
    vampytest.assert_instance(instance, EmbedType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, EmbedType.VALUE_TYPE)
