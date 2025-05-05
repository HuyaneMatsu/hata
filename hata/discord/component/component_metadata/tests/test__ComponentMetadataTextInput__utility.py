import vampytest

from ....guild import Guild

from ..preinstanced import TextInputStyle
from ..text_input import ComponentMetadataTextInput

from .test__ComponentMetadataTextInput__constructor import _assert_fields_set


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
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
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
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
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
    old_label = 'end'
    old_max_length = 11
    old_min_length = 10
    old_required = True
    old_placeholder = 'green'
    old_text_input_style = TextInputStyle.paragraph
    old_value = 'sanatorium'
    
    new_custom_id = 'kagami'
    new_label = 'kagerou'
    new_max_length = 12
    new_min_length = 9
    new_required = False
    new_placeholder = 'yuuka'
    new_text_input_style = TextInputStyle.short
    new_value = 'hana'
    
    component_metadata = ComponentMetadataTextInput(
        custom_id = old_custom_id,
        label = old_label,
        max_length = old_max_length,
        min_length = old_min_length,
        placeholder = old_placeholder,
        required = old_required,
        text_input_style = old_text_input_style,
        value = old_value,
    )
    copy = component_metadata.copy_with(
        custom_id = new_custom_id,
        label = new_label,
        max_length = new_max_length,
        min_length = new_min_length,
        placeholder = new_placeholder,
        required = new_required,
        text_input_style = new_text_input_style,
        value = new_value,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.max_length, new_max_length)
    vampytest.assert_eq(copy.min_length, new_min_length)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_is(copy.text_input_style, new_text_input_style)
    vampytest.assert_eq(copy.value, new_value)


def test__ComponentMetadataTextInput__copy_with_keyword_parameters__0():
    """
    Tests whether ``ComponentMetadataTextInput.copy_with_keyword_parameters`` works as intended.
    
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
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_eq(copy.label, label)
    vampytest.assert_eq(copy.max_length, max_length)
    vampytest.assert_eq(copy.min_length, min_length)
    vampytest.assert_eq(copy.placeholder, placeholder)
    vampytest.assert_eq(copy.required, required)
    vampytest.assert_is(copy.text_input_style, text_input_style)
    vampytest.assert_eq(copy.value, value)


def test__ComponentMetadataTextInput__copy_with_keyword_parameters__1():
    """
    Tests whether ``ComponentMetadataTextInput.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_custom_id = 'night'
    old_label = 'end'
    old_max_length = 11
    old_min_length = 10
    old_required = True
    old_placeholder = 'green'
    old_text_input_style = TextInputStyle.paragraph
    old_value = 'sanatorium'
    
    new_custom_id = 'kagami'
    new_label = 'kagerou'
    new_max_length = 12
    new_min_length = 9
    new_required = False
    new_placeholder = 'yuuka'
    new_text_input_style = TextInputStyle.short
    new_value = 'hana'
    
    component_metadata = ComponentMetadataTextInput(
        custom_id = old_custom_id,
        label = old_label,
        max_length = old_max_length,
        min_length = old_min_length,
        placeholder = old_placeholder,
        required = old_required,
        text_input_style = old_text_input_style,
        value = old_value,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'label': new_label,
        'max_length': new_max_length,
        'min_length': new_min_length,
        'placeholder': new_placeholder,
        'required': new_required,
        'text_input_style': new_text_input_style,
        'value': new_value,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.max_length, new_max_length)
    vampytest.assert_eq(copy.min_length, new_min_length)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.required, new_required)
    vampytest.assert_is(copy.text_input_style, new_text_input_style)
    vampytest.assert_eq(copy.value, new_value)


def _iter_options__iter_contents():
    custom_id = 'night'
    label = 'end'
    max_length = 11
    min_length = 10
    required = True
    placeholder = 'green'
    text_input_style = TextInputStyle.paragraph
    value = 'sanatorium'
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'custom_id': custom_id,
            'label': label,
            'max_length': max_length,
            'min_length': min_length,
            'placeholder': placeholder,
            'required': required,
            'text_input_style': text_input_style,
            'value': value,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataTextInput__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataTextInput.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataTextInput(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
