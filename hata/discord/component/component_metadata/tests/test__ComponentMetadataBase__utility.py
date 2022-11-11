import vampytest

from ..base import ComponentMetadataBase

from .test__ComponentMetadataBase__constructor import _check_is_all_attribute_set


def test__ComponentMetadataBase__copy():
    """
    Tests whether ``ComponentMetadataBase.copy`` works as intended.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataBase(keyword_parameters)
    copy = component_metadata.copy()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    

def test__ComponentMetadataBase__copy_with():
    """
    Tests whether ``ComponentMetadataBase.copy_with`` works as intended.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataBase(keyword_parameters)
    copy = component_metadata.copy_with({})
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
