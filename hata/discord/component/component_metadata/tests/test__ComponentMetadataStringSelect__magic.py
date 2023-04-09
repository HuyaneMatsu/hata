import vampytest

from ...string_select_option import StringSelectOption

from ..string_select import ComponentMetadataStringSelect


def test__ComponentMetadataStringSelect__repr():
    """
    Tests whether ``ComponentMetadataStringSelect.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    options = [StringSelectOption('yume')]
    
    component_metadata = ComponentMetadataStringSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        options = options,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataStringSelect__hash():
    """
    Tests whether ``ComponentMetadataStringSelect.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    options = [StringSelectOption('yume')]
    
    component_metadata = ComponentMetadataStringSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        options = options,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataStringSelect__eq():
    """
    Tests whether ``ComponentMetadataStringSelect.__eq__`` works as intended.
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
    
    component_metadata = ComponentMetadataStringSelect(**keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())

    for field_name, field_value in (
        ('custom_id', 'distopia'),
        ('enabled', True),
        ('max_values', 11),
        ('min_values', 8),
        ('placeholder', 'kokoro'),
        ('options', None),
    ):
        test_component_metadata = ComponentMetadataStringSelect(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
