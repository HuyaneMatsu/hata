import vampytest

from ...string_select_option import StringSelectOption

from ..string_select import ComponentMetadataStringSelect

from .test__ComponentMetadataStringSelect__constructor import _check_is_all_attribute_set


def test__ComponentMetadataStringSelect__copy():
    """
    Tests whether ``ComponentMetadataStringSelect.copy`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    options = [StringSelectOption('yume')]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'options': options,
    }
    
    component_metadata = ComponentMetadataStringSelect(keyword_parameters)
    copy = component_metadata.copy()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.max_values, max_values)
    vampytest.assert_eq(copy.min_values, min_values)
    vampytest.assert_eq(copy.placeholder, placeholder)
    vampytest.assert_eq(copy.options, tuple(options))


def test__ComponentMetadataStringSelect__copy_with__0():
    """
    Tests whether ``ComponentMetadataStringSelect.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    options = [StringSelectOption('yume')]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'options': options,
    }
    
    component_metadata = ComponentMetadataStringSelect(keyword_parameters)
    copy = component_metadata.copy_with({})
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.max_values, max_values)
    vampytest.assert_eq(copy.min_values, min_values)
    vampytest.assert_eq(copy.placeholder, placeholder)
    vampytest.assert_eq(copy.options, tuple(options))


def test__ComponentMetadataStringSelect__copy_with__1():
    """
    Tests whether ``ComponentMetadataStringSelect.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    new_custom_id = 'uta'
    old_enabled = False
    new_enabled = True
    old_max_values = 10
    new_max_values = 11
    old_min_values = 9
    new_min_values = 8
    old_placeholder = 'swing'
    new_placeholder = 'kotoba'
    old_options = [StringSelectOption('yume')]
    new_options = [StringSelectOption('shinjite'), StringSelectOption('boku')]
    
    keyword_parameters = {
        'custom_id': old_custom_id,
        'enabled': old_enabled,
        'max_values': old_max_values,
        'min_values': old_min_values,
        'placeholder': old_placeholder,
        'options': old_options,
    }
    
    component_metadata = ComponentMetadataStringSelect(keyword_parameters)
    copy = component_metadata.copy_with({
        'custom_id': new_custom_id,
        'enabled': new_enabled,
        'max_values': new_max_values,
        'min_values': new_min_values,
        'placeholder': new_placeholder,
        'options': new_options,
    })
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.options, tuple(new_options))
