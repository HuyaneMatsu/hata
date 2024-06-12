import vampytest

from ...component import Component, ComponentType

from ..row import ComponentMetadataRow

from .test__ComponentMetadataRow__constructor import _assert_fields_set


def test__ComponentMetadataRow__copy():
    """
    Tests whether ``ComponentMetadataRow.copy`` works as intended.
    """
    components = [Component(ComponentType.button, label = 'chata')]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataRow__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataRow.copy_with`` works as intended.
    
    Case: no fields.
    """
    components = [Component(ComponentType.button, label = 'chata')]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataRow__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataRow.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_components = [Component(ComponentType.button, label = 'chata')]
    
    new_components = [Component(ComponentType.button, label = 'yuina')]
    
    component_metadata = ComponentMetadataRow(
        components = old_components,
    )
    copy = component_metadata.copy_with(
        components = new_components,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.components, tuple(new_components))


def test__ComponentMetadataRow__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataRow.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    components = [Component(ComponentType.button, label = 'chata')]
    
    component_metadata = ComponentMetadataRow(
        components = components,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataRow__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataRow.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_components = [Component(ComponentType.button, label = 'chata')]
    
    new_components = [Component(ComponentType.button, label = 'yuina')]
    
    component_metadata = ComponentMetadataRow(
        components = old_components,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'components': new_components,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.components, tuple(new_components))
