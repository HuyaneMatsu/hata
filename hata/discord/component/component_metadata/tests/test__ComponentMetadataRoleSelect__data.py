import vampytest

from ..role_select import ComponentMetadataRoleSelect

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType


from .test__ComponentMetadataRoleSelect__constructor import _assert_fields_set


def test__ComponentMetadataRoleSelect__from_data():
    """
    Tests whether ``ComponentMetadataRoleSelect.from_data`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140037)]
    
    data = {
        'custom_id': custom_id,
        'disabled': not enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'default_values': [default_value.to_data() for default_value in default_values],
    }
    
    component_metadata = ComponentMetadataRoleSelect.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))


def test__ComponentMetadataRoleSelect__to_data():
    """
    Tests whether ``ComponentMetadataRoleSelect.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140038)]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'custom_id': custom_id,
            'disabled': not enabled,
            'max_values': max_values,
            'min_values': min_values,
            'placeholder': placeholder,
            'default_values': [default_value.to_data(defaults = True) for default_value in default_values],
        },
    )
