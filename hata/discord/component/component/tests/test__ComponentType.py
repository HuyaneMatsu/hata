import vampytest

from ...component_metadata import ComponentMetadataBase

from ..preinstanced import ComponentType


@vampytest.call_from(ComponentType.INSTANCES.values())
def test__ComponentType__instances(instance):
    """
    Tests whether ``ComponentType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ComponentType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ComponentType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ComponentType.VALUE_TYPE)
    vampytest.assert_subtype(instance.metadata_type, ComponentMetadataBase)
