import vampytest

from ...component_metadata import ComponentMetadataBase

from ..preinstanced import ComponentType


def test__ComponentType__name():
    """
    Tests whether ``ComponentType`` instance names are all strings.
    """
    for instance in ComponentType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ComponentType__value():
    """
    Tests whether ``ComponentType`` instance values are all the expected value type.
    """
    for instance in ComponentType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ComponentType.VALUE_TYPE)


def test__ComponentType__metadata_type():
    """
    Tests whether ``ComponentType`` instance metadata types are all metadata types.
    """
    for instance in ComponentType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, ComponentMetadataBase)
