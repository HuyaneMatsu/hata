import vampytest

from ...preinstanced import TextInputStyle

from ..text_input import ComponentMetadataTextInput


def test__ComponentMetadataTextInput__repr():
    """
    Tests whether ``ComponentMetadataTextInput.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataTextInput__hash():
    """
    Tests whether ``ComponentMetadataTextInput.__hash__`` works as intended.
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
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataTextInput__eq():
    """
    Tests whether ``ComponentMetadataTextInput.__eq__`` works as intended.
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
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())

    for field_name, field_value in (
        ('custom_id', 'kagome'),
        ('label', 'game'),
        ('max_length', 12),
        ('min_length', 11),
        ('required', False),
        ('placeholder', 'over'),
        ('text_input_style', TextInputStyle.short),
        ('value', 'nue'),
    ):
        test_component_metadata = ComponentMetadataTextInput({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
