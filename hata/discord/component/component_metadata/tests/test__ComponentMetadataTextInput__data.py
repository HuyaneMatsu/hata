import vampytest

from ..preinstanced import TextInputStyle
from ..text_input import ComponentMetadataTextInput

from .test__ComponentMetadataTextInput__constructor import _assert_fields_set


def test__ComponentMetadataTextInput__from_data():
    """
    Tests whether ``ComponentMetadataTextInput.from_data`` works as intended.
    """
    custom_id = 'night'
    label = 'end'
    max_length = 11
    min_length = 10
    required = True
    placeholder = 'green'
    text_input_style = TextInputStyle.paragraph
    value = 'sanatorium'
    
    data = {
        'custom_id': custom_id,
        'label': label,
        'max_length': max_length,
        'min_length': min_length,
        'placeholder': placeholder,
        'required': required,
        'style': text_input_style.value,
        'value': value,
    }
    
    component_metadata = ComponentMetadataTextInput.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.label, label)
    vampytest.assert_eq(component_metadata.max_length, max_length)
    vampytest.assert_eq(component_metadata.min_length, min_length)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)
    vampytest.assert_is(component_metadata.text_input_style, text_input_style)
    vampytest.assert_eq(component_metadata.value, value)


def test__ComponentMetadataTextInput__to_data():
    """
    Tests whether ``ComponentMetadataTextInput.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    custom_id = 'night'
    label = 'end'
    max_length = 11
    min_length = 10
    required = True
    placeholder = 'green'
    text_input_style = TextInputStyle.paragraph
    value = 'sanatorium'
    
    component_metadata = ComponentMetadataTextInput(
        custom_id = custom_id,
        label = label,
        max_length = max_length,
        min_length = min_length,
        placeholder = placeholder,
        required = required,
        text_input_style = text_input_style,
        value = value,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'custom_id': custom_id,
            'label': label,
            'max_length': max_length,
            'min_length': min_length,
            'placeholder': placeholder,
            'required': required,
            'style': text_input_style.value,
            'value': value,
        },
    )
