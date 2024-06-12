import vampytest

from ..text import ComponentMetadataText

from .test__ComponentMetadataText__constructor import _assert_fields_set


def test__ComponentMetadataText__copy():
    """
    Tests whether ``ComponentMetadataText.copy`` works as intended.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataText(
        content = content,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataText__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataText.copy_with`` works as intended.
    
    Case: no fields.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataText(
        content = content,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataText__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataText.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_content = 'hey sister'
    
    new_content = 'hey mister'
    
    component_metadata = ComponentMetadataText(
        content = old_content,
    )
    copy = component_metadata.copy_with(
        content = new_content,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.content, new_content)


def test__ComponentMetadataText__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataText.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataText(
        content = content,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataText__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataText.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_content = 'hey sister'
    
    new_content = 'hey mister'
    
    component_metadata = ComponentMetadataText(
        content = old_content,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'content': new_content,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.content, new_content)
