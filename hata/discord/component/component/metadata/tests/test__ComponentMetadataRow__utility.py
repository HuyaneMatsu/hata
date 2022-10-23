import vampytest

from ...component import Component
from ...component_type import ComponentType

from ..row import ComponentMetadataRow

from .test__ComponentMetadataRow__constructor import _check_is_all_attribute_set


def test__ComponentMetadataRow__copy():
    """
    Tests whether ``ComponentMetadataRow.copy`` works as intended.
    """
    components = [Component(ComponentType.button, label = 'chata')]
    
    keyword_parameters = {
        'components': components,
    }
    
    component_metadata = ComponentMetadataRow(keyword_parameters)
    copy = component_metadata.copy()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.components, tuple(components))


def test__ComponentMetadataRow__copy_with_0():
    """
    Tests whether ``ComponentMetadataRow.copy_with`` works as intended.
    
    Case: no fields.
    """
    components = [Component(ComponentType.button, label = 'chata')]
    
    keyword_parameters = {
        'components': components,
    }
    
    component_metadata = ComponentMetadataRow(keyword_parameters)
    copy = component_metadata.copy_with({})
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.components, tuple(components))


def test__ComponentMetadataRow__copy_with__1():
    """
    Tests whether ``ComponentMetadataRow.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_components = [Component(ComponentType.button, label = 'chata')]
    new_components = [Component(ComponentType.button, label = 'yuina')]
    
    keyword_parameters = {
        'components': old_components,
    }
    
    component_metadata = ComponentMetadataRow(keyword_parameters)
    copy = component_metadata.copy_with({
        'components': new_components,
    })
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.components, tuple(new_components))
