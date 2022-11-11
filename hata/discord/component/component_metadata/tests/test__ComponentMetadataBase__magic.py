import vampytest

from ..base import ComponentMetadataBase


def test__ComponentMetadataBase__repr():
    """
    Tests whether ``ComponentMetadataBase.__repr__`` works as intended.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataBase(keyword_parameters)
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataBase__hash():
    """
    Tests whether ``ComponentMetadataBase.__hash__`` works as intended.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataBase(keyword_parameters)
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataBase__eq():
    """
    Tests whether ``ComponentMetadataBase.__eq__`` works as intended.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataBase(keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())

    for field_name, field_value in ():
        test_component_metadata = ComponentMetadataBase({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
