import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..role_select import ComponentMetadataRoleSelect


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataRoleSelect`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataRoleSelect``
        Component metadata to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataRoleSelect)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.default_values, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.placeholder, str, nullable = True)


def test__ComponentMetadataRoleSelect__new__no_fields():
    """
    Tests whether ``ComponentMetadataRoleSelect.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataRoleSelect()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataRoleSelect__new__all_fields():
    """
    Tests whether ``ComponentMetadataRoleSelect.__new__`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140035)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataRoleSelect__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataRoleSelect.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataRoleSelect.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataRoleSelect__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataRoleSelect.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140036)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    keyword_parameters = {
        'custom_id': custom_id,
        'default_values': default_values,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'required': required,
    }
    
    component_metadata = ComponentMetadataRoleSelect.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)
