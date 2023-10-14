import vampytest

from ....channel import ChannelType

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..channel_select import ComponentMetadataChannelSelect

from .test__ComponentMetadataChannelSelect__constructor import _assert_fields_set


def test__ComponentMetadataChannelSelect__copy():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130013)]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataChannelSelect__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130014)]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataChannelSelect__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_channel_types = [ChannelType.private]
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130015),
    ]
    
    new_custom_id = 'uta'
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_channel_types = [ChannelType.guild_text, ChannelType.guild_voice]
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130016),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130017),
    ]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = old_custom_id,
        enabled = old_enabled,
        max_values = old_max_values,
        min_values = old_min_values,
        placeholder = old_placeholder,
        channel_types = old_channel_types,
        default_values = old_default_values,
    )
    copy = component_metadata.copy_with(
        custom_id = new_custom_id,
        enabled = new_enabled,
        max_values = new_max_values,
        min_values = new_min_values,
        placeholder = new_placeholder,
        channel_types = new_channel_types,
        default_values = new_default_values,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.channel_types, tuple(new_channel_types))
    vampytest.assert_eq(copy.default_values, tuple(new_default_values))


def test__ComponentMetadataChannelSelect__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130018)]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataChannelSelect__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_enabled = False
    old_max_values = 10
    old_min_values = 9
    old_placeholder = 'swing'
    old_channel_types = [ChannelType.private]
    old_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130019),
    ]
    
    new_custom_id = 'uta'
    new_enabled = True
    new_max_values = 11
    new_min_values = 8
    new_placeholder = 'kotoba'
    new_channel_types = [ChannelType.guild_text, ChannelType.guild_voice]
    new_default_values = [
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130020),
        EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130021),
    ]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = old_custom_id,
        enabled = old_enabled,
        max_values = old_max_values,
        min_values = old_min_values,
        placeholder = old_placeholder,
        channel_types = old_channel_types,
        default_values = old_default_values,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'enabled': new_enabled,
        'max_values': new_max_values,
        'min_values': new_min_values,
        'placeholder': new_placeholder,
        'channel_types': new_channel_types,
        'default_values': new_default_values,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.channel_types, tuple(new_channel_types))
    vampytest.assert_eq(copy.default_values, tuple(new_default_values))
