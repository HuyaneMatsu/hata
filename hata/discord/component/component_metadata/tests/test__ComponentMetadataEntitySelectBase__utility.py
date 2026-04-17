import vampytest

from ....guild import Guild

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..entity_select_base import ComponentMetadataEntitySelectBase

from .test__ComponentMetadataEntitySelectBase__constructor import _assert_fields_set


def test__ComponentMetadataEntitySelectBase__clean_copy():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.clean_copy`` works as intended.
    """
    guild_id = 202505030018
    guild = Guild.precreate(guild_id)
    
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202505030019)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataEntitySelectBase__copy():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.copy`` works as intended.
    """
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140007)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataEntitySelectBase__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140008)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataEntitySelectBase__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140009),
    ]
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_required = True
    
    new_custom_id = 'uta'
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140010),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140011),
    ]
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_required = False
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = old_custom_id,
        default_values = old_default_values,
        enabled = old_enabled,
        max_values = old_max_values,
        min_values = old_min_values,
        placeholder = old_placeholder,
        required = old_required,
    )
    copy = component_metadata.copy_with(
        custom_id = new_custom_id,
        default_values = new_default_values,
        enabled = new_enabled,
        max_values = new_max_values,
        min_values = new_min_values,
        placeholder = new_placeholder,
        required = new_required,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.default_values, tuple(new_default_values))
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.required, new_required)


def test__ComponentMetadataEntitySelectBase__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140012)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataEntitySelectBase__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataEntitySelectBase.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140013),
    ]
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_required = True
    
    new_custom_id = 'uta'
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140014),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310140015),
    ]
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_required = False
    
    component_metadata = ComponentMetadataEntitySelectBase(
        custom_id = old_custom_id,
        default_values = old_default_values,
        enabled = old_enabled,
        max_values = old_max_values,
        min_values = old_min_values,
        placeholder = old_placeholder,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'default_values': new_default_values,
        'enabled': new_enabled,
        'max_values': new_max_values,
        'min_values': new_min_values,
        'placeholder': new_placeholder,
        'required': new_required,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.default_values, tuple(new_default_values))
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.required, new_required)


def _iter_options__iter_contents():
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202505030001)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'custom_id': custom_id,
            'default_values': default_values,
            'enabled': enabled,
            'max_values': max_values,
            'min_values': min_values,
            'placeholder': placeholder,
            'required': required,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataEntitySelectBase__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataEntitySelectBase.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataEntitySelectBase(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
