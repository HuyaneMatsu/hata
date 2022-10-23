import vampytest

from ..select_base import ComponentMetadataSelectBase


def test__ComponentMetadataSelectBase__repr():
    """
    Tests whether ``ComponentMetadataSelectBase.__repr__`` works as intended.
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
    
    component_metadata = ComponentMetadataSelectBase(keyword_parameters)
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataSelectBase__hash():
    """
    Tests whether ``ComponentMetadataSelectBase.__hash__`` works as intended.
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
    
    component_metadata = ComponentMetadataSelectBase(keyword_parameters)
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataSelectBase__eq():
    """
    Tests whether ``ComponentMetadataSelectBase.__eq__`` works as intended.
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
    
    component_metadata = ComponentMetadataSelectBase(keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())

    for field_name, field_value in (
        ('custom_id', 'distopia'),
        ('enabled', True),
        ('max_values', 11),
        ('min_values', 8),
        ('placeholder', 'kokoro'),
    ):
        test_component_metadata = ComponentMetadataSelectBase({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
