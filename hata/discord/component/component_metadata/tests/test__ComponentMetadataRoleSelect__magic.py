import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..role_select import ComponentMetadataRoleSelect


def test__ComponentMetadataRoleSelect__repr():
    """
    Tests whether ``ComponentMetadataRoleSelect.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140020)]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataRoleSelect__hash():
    """
    Tests whether ``ComponentMetadataRoleSelect.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140039)]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataRoleSelect__eq():
    """
    Tests whether ``ComponentMetadataRoleSelect.__eq__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140040)]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'default_values': default_values,
    }
    
    component_metadata = ComponentMetadataRoleSelect(**keyword_parameters)
    
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
        test_component_metadata = ComponentMetadataRoleSelect(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
