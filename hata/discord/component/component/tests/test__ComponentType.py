import vampytest

from ...component_metadata import ComponentMetadataBase

from ..flags import ComponentTypeLayoutFlag
from ..preinstanced import COMPONENT_TYPE_LAYOUT_FLAGS_ALL, ComponentType


def _assert_fields_set(component_type):
    """
    Asserts whether every field are set of the given component type.
    
    Parameters
    ----------
    component_type : ``ComponentType``
        The instance to test.
    """
    vampytest.assert_instance(component_type, ComponentType)
    vampytest.assert_instance(component_type.name, str)
    vampytest.assert_instance(component_type.value, ComponentType.VALUE_TYPE)
    vampytest.assert_instance(component_type.layout_flags, ComponentTypeLayoutFlag)
    vampytest.assert_subtype(component_type.metadata_type, ComponentMetadataBase)



@vampytest.call_from(ComponentType.INSTANCES.values())
def test__ComponentType__instances(instance):
    """
    Tests whether ``ComponentType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ComponentType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__ComponentType__new__min_fields():
    """
    Tests whether ``ComponentType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = ComponentType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, ComponentType.NAME_DEFAULT)
        vampytest.assert_eq(output.layout_flags, COMPONENT_TYPE_LAYOUT_FLAGS_ALL)
        vampytest.assert_is(output.metadata_type, ComponentMetadataBase)
        vampytest.assert_is(ComponentType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del ComponentType.INSTANCES[value]
        except KeyError:
            pass
