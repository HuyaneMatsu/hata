import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..mentionable_select import ComponentMetadataMentionableSelect

from .test__ComponentMetadataMentionableSelect__constructor import _assert_fields_set


def test__ComponentMetadataMentionableSelect__copy():
    """
    Tests whether ``ComponentMetadataMentionableSelect.copy`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130029)]
    
    component_metadata = ComponentMetadataMentionableSelect(
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


def test__ComponentMetadataMentionableSelect__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataMentionableSelect.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130030)]
    
    component_metadata = ComponentMetadataMentionableSelect(
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


def test__ComponentMetadataMentionableSelect__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataMentionableSelect.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130031),
    ]
    
    new_custom_id = 'uta'
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130032),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130033),
    ]
    
    component_metadata = ComponentMetadataMentionableSelect(
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


def test__ComponentMetadataMentionableSelect__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataMentionableSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130034)]
    
    component_metadata = ComponentMetadataMentionableSelect(
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


def test__ComponentMetadataMentionableSelect__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataMentionableSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130035),
    ]
    
    new_custom_id = 'uta'
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130036),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130037),
    ]
    
    component_metadata = ComponentMetadataMentionableSelect(
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
