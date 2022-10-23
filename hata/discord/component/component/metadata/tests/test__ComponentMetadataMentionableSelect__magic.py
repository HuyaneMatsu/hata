import vampytest

from ..mentionable_select import ComponentMetadataMentionableSelect


def test__ComponentMetadataMentionableSelect__repr():
    """
    Tests whether ``ComponentMetadataMentionableSelect.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
    }
    
    component_metadata = ComponentMetadataMentionableSelect(keyword_parameters)
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataMentionableSelect__hash():
    """
    Tests whether ``ComponentMetadataMentionableSelect.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
    }
    
    component_metadata = ComponentMetadataMentionableSelect(keyword_parameters)
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataMentionableSelect__eq():
    """
    Tests whether ``ComponentMetadataMentionableSelect.__eq__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
    }
    
    component_metadata = ComponentMetadataMentionableSelect(keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())

    for field_name, field_value in (
        ('custom_id', 'distopia'),
        ('enabled', True),
        ('max_values', 11),
        ('min_values', 8),
        ('placeholder', 'kokoro'),
    ):
        test_component_metadata = ComponentMetadataMentionableSelect({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
