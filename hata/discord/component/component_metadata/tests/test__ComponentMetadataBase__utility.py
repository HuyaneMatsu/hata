import vampytest

from ..base import ComponentMetadataBase

from .test__ComponentMetadataBase__constructor import _assert_fields_set


def test__ComponentMetadataBase__copy():
    """
    Tests whether ``ComponentMetadataBase.copy`` works as intended.
    """
    component_metadata = ComponentMetadataBase()
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    

def test__ComponentMetadataBase__copy_with__0():
    """
    Tests whether ``ComponentMetadataBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    component_metadata = ComponentMetadataBase()
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)


def test__ComponentMetadataBase__copy_with_keyword_parameters__0():
    """
    Tests whether ``ComponentMetadataBase.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    component_metadata = ComponentMetadataBase()
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
