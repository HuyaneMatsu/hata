import vampytest

from ..preinstanced import TextInputStyle
from ..text_input import ComponentMetadataTextInput


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataTextInput`` has all it's attributes set.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataTextInput)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.label, str, nullable = True)
    vampytest.assert_instance(component_metadata.max_length, int)
    vampytest.assert_instance(component_metadata.min_length, int)
    vampytest.assert_instance(component_metadata.placeholder, str, nullable = True)
    vampytest.assert_instance(component_metadata.required, bool)
    vampytest.assert_instance(component_metadata.text_input_style, TextInputStyle)
    vampytest.assert_instance(component_metadata.value, str, nullable = True)


def test__ComponentMetadataTextInput__new__0():
    """
    Tests whether ``ComponentMetadataTextInput.__new__`` works as intended.
    
    Case: No fields given.
    """
    component_metadata = ComponentMetadataTextInput()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataTextInput__new__1():
    """
    Tests whether ``ComponentMetadataTextInput.__new__`` works as intended.
    
    Case: all fields given.
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
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.label, label)
    vampytest.assert_eq(component_metadata.max_length, max_length)
    vampytest.assert_eq(component_metadata.min_length, min_length)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)
    vampytest.assert_is(component_metadata.text_input_style, text_input_style)
    vampytest.assert_eq(component_metadata.value, value)


def test__ComponentMetadataTextInput__from_keyword_parameters__0():
    """
    Tests whether ``ComponentMetadataTextInput.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataTextInput.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataTextInput__from_keyword_parameters__1():
    """
    Tests whether ``ComponentMetadataTextInput.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
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
    
    component_metadata = ComponentMetadataTextInput.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.label, label)
    vampytest.assert_eq(component_metadata.max_length, max_length)
    vampytest.assert_eq(component_metadata.min_length, min_length)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)
    vampytest.assert_is(component_metadata.text_input_style, text_input_style)
    vampytest.assert_eq(component_metadata.value, value)
