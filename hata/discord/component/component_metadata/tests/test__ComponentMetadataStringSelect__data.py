import vampytest

from ...string_select_option import StringSelectOption

from ..string_select import ComponentMetadataStringSelect

from .test__ComponentMetadataStringSelect__constructor import _check_is_all_attribute_set


def test__ComponentMetadataStringSelect__from_data():
    """
    Tests whether ``ComponentMetadataStringSelect.from_data`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    options = [StringSelectOption('yume')]
    
    data = {
        'custom_id': custom_id,
        'disabled': not enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'options': [string_type.to_data() for string_type in options],
    }
    
    component_metadata = ComponentMetadataStringSelect.from_data(data)
    _check_is_all_attribute_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.options, tuple(options))


def test__ComponentMetadataStringSelect__to_data():
    """
    Tests whether ``ComponentMetadataStringSelect.to_data`` works as intended.
    
    Case: include defaults.
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
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {
            'custom_id': custom_id,
            'disabled': not enabled,
            'max_values': max_values,
            'min_values': min_values,
            'placeholder': placeholder,
            'options': [string_type.to_data(defaults = True) for string_type in options],
        },
    )
