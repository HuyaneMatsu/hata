import vampytest

from ..component import Component, ComponentType, TextInputStyle
from ..utils import create_text_input

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
    
    component = create_text_input(
        custom_id = custom_id,
        label = label,
        max_length = max_length,
        min_length = min_length,
        placeholder = placeholder,
        required = required,
        style = text_input_style,
        value = value,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.text_input)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.label, label)
    vampytest.assert_eq(component.max_length, max_length)
    vampytest.assert_eq(component.min_length, min_length)
    vampytest.assert_eq(component.placeholder, placeholder)
    vampytest.assert_eq(component.required, required)
    vampytest.assert_is(component.text_input_style, text_input_style)
    vampytest.assert_eq(component.value, value)
