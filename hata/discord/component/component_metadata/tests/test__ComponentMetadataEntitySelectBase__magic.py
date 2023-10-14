import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..entity_select_base import ComponentMetadataEntitySelectBase


def test__ComponentMetadataEntitySelectBase__repr():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140004)]
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataEntitySelectBase__hash():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140005)]
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataEntitySelectBase__eq():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.__eq__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140006)]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'default_values': default_values,
    }
    
    component_metadata = ComponentMetadataEntitySelectBase(**keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())

    for field_name, field_value in (
        ('custom_id', 'distopia'),
        ('enabled', True),
        ('max_values', 11),
        ('min_values', 8),
        ('placeholder', 'kokoro'),
        ('default_values', None),
    ):
        test_component_metadata = ComponentMetadataEntitySelectBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
