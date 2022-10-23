import vampytest

from ..text_input import ComponentMetadataTextInput

from ...preinstanced import TextInputStyle

from .test__ComponentMetadataTextInput__constructor import _check_is_all_attribute_set


def test__ComponentMetadataTextInput__copy():
    """
    Tests whether ``ComponentMetadataTextInput.copy`` works as intended.
    """
    custom_id = 'night'
    label = 'end'
    max_length = 11
    min_length = 10
    required = True
    placeholder = 'green'
    text_input_style = TextInputStyle.paragraph
    value = 'sanatorium'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'label': label,
        'max_length': max_length,
        'min_length': min_length,
        'placeholder': placeholder,
        'required': required,
        'text_input_style': text_input_style,
        'value': value,
    }
    
    component_metadata = ComponentMetadataTextInput(keyword_parameters)
    copy = component_metadata.copy()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_eq(copy.label, label)
    vampytest.assert_eq(copy.max_length, max_length)
    vampytest.assert_eq(copy.min_length, min_length)
    vampytest.assert_eq(copy.placeholder, placeholder)
    vampytest.assert_eq(copy.required, required)
    vampytest.assert_is(copy.text_input_style, text_input_style)
    vampytest.assert_eq(copy.value, value)

    

def test__ComponentMetadataTextInput__copy_with__0():
    """
    Tests whether ``ComponentMetadataTextInput.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'night'
    label = 'end'
    max_length = 11
    min_length = 10
    required = True
    placeholder = 'green'
    text_input_style = TextInputStyle.paragraph
    value = 'sanatorium'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'label': label,
        'max_length': max_length,
        'min_length': min_length,
        'placeholder': placeholder,
        'required': required,
        'text_input_style': text_input_style,
        'value': value,
    }
    
    component_metadata = ComponentMetadataTextInput(keyword_parameters)
    copy = component_metadata.copy_with({})
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_eq(copy.label, label)
    vampytest.assert_eq(copy.max_length, max_length)
    vampytest.assert_eq(copy.min_length, min_length)
    vampytest.assert_eq(copy.placeholder, placeholder)
    vampytest.assert_eq(copy.required, required)
    vampytest.assert_is(copy.text_input_style, text_input_style)
    vampytest.assert_eq(copy.value, value)


def test__ComponentMetadataTextInput__copy_with__1():
    """
    Tests whether ``ComponentMetadataTextInput.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_custom_id = 'night'
    new_custom_id = 'kagami'
    old_label = 'end'
    new_label = 'kagerou'
    old_max_length = 11
    new_max_length = 12
    old_min_length = 10
    new_min_length = 9
    old_required = True
    new_required = False
    old_placeholder = 'green'
    new_placeholder = 'yuuka'
    old_text_input_style = TextInputStyle.paragraph
    new_text_input_style = TextInputStyle.short
    old_value = 'sanatorium'
    new_value = 'hana'
    
    keyword_parameters = {
        'custom_id': old_custom_id,
        'label': old_label,
        'max_length': old_max_length,
        'min_length': old_min_length,
        'placeholder': old_placeholder,
        'required': old_required,
        'text_input_style': old_text_input_style,
        'value': old_value,
    }
    
    component_metadata = ComponentMetadataTextInput(keyword_parameters)
    copy = component_metadata.copy_with({
        'custom_id': new_custom_id,
        'label': new_label,
        'max_length': new_max_length,
        'min_length': new_min_length,
        'placeholder': new_placeholder,
        'required': new_required,
        'text_input_style': new_text_input_style,
        'value': new_value,
    })
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.max_length, new_max_length)
    vampytest.assert_eq(copy.min_length, new_min_length)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_is(copy.text_input_style, new_text_input_style)
    vampytest.assert_eq(copy.value, new_value)
