import vampytest

from ...checkbox_group_option import CheckboxGroupOption

from ..checkbox_group import ComponentMetadataCheckboxGroup

from .test__ComponentMetadataCheckboxGroup__constructor import _assert_fields_set


def test__ComponentMetadataCheckboxGroup__from_data():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.from_data`` works as intended.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    data = {
        'custom_id': custom_id,
        'max_values': max_values,
        'min_values': min_values,
        'options': [string_type.to_data() for string_type in options],
        'required': required,
    }
    
    component_metadata = ComponentMetadataCheckboxGroup.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.options, tuple(options))
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataCheckboxGroup__to_data():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        options = options,
        required = required,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'custom_id': custom_id,
            'max_values': max_values,
            'min_values': min_values,
            'options': [string_type.to_data(defaults = True) for string_type in options],
            'required': required,
        },
    )
