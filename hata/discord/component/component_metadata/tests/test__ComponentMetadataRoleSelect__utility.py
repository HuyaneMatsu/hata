import vampytest

from ....guild import Guild

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..role_select import ComponentMetadataRoleSelect

from .test__ComponentMetadataRoleSelect__constructor import _assert_fields_set


def test__ComponentMetadataRoleSelect__clean_copy():
    """
    Tests whether ``ComponentMetadataRoleSelect.clean_copy`` works as intended.
    """
    guild_id = 202505030023
    guild = Guild.precreate(guild_id)
    
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 20250503004)]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataRoleSelect__copy():
    """
    Tests whether ``ComponentMetadataRoleSelect.copy`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140041)]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataRoleSelect__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataRoleSelect.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140042)]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.max_values, max_values)
    vampytest.assert_eq(copy.min_values, min_values)
    vampytest.assert_eq(copy.placeholder, placeholder)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataRoleSelect__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataRoleSelect.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140043),
    ]
    
    new_custom_id = 'uta'
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140044),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140045),
    ]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = old_custom_id,
        enabled = old_enabled,
        max_values = old_max_values,
        min_values = old_min_values,
        placeholder = old_placeholder,
        default_values = old_default_values,
    )
    copy = component_metadata.copy_with(
        custom_id = new_custom_id,
        enabled = new_enabled,
        max_values = new_max_values,
        min_values = new_min_values,
        placeholder = new_placeholder,
        default_values = new_default_values,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.default_values, tuple(new_default_values))


def test__ComponentMetadataRoleSelect__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataRoleSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140046)]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        default_values = default_values,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataRoleSelect__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataRoleSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140047),
    ]
    
    new_custom_id = 'uta'
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140048),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310140049),
    ]
    
    component_metadata = ComponentMetadataRoleSelect(
        custom_id = old_custom_id,
        enabled = old_enabled,
        max_values = old_max_values,
        min_values = old_min_values,
        placeholder = old_placeholder,
        default_values = old_default_values,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'enabled': new_enabled,
        'max_values': new_max_values,
        'min_values': new_min_values,
        'placeholder': new_placeholder,
        'default_values': new_default_values,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.default_values, tuple(new_default_values))


def _iter_options__iter_contents():
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202505030003)]
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'custom_id': custom_id,
            'enabled': enabled,
            'max_values': max_values,
            'min_values': min_values,
            'placeholder': placeholder,
            'default_values': default_values,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataRoleSelect__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataRoleSelect.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataRoleSelect(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
