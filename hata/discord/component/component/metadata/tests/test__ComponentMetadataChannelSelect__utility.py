import vampytest

from .....channel import ChannelType

from ..channel_select import ComponentMetadataChannelSelect

from .test__ComponentMetadataChannelSelect__constructor import _check_is_all_attribute_set


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
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'channel_types': channel_types,
    }
    
    component_metadata = ComponentMetadataChannelSelect(keyword_parameters)
    copy = component_metadata.copy()
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.max_values, max_values)
    vampytest.assert_eq(copy.min_values, min_values)
    vampytest.assert_eq(copy.placeholder, placeholder)
    vampytest.assert_eq(copy.channel_types, tuple(channel_types))


def test__ComponentMetadataChannelSelect__copy_with__0():
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
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'channel_types': channel_types,
    }
    
    component_metadata = ComponentMetadataChannelSelect(keyword_parameters)
    copy = component_metadata.copy_with({})
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.max_values, max_values)
    vampytest.assert_eq(copy.min_values, min_values)
    vampytest.assert_eq(copy.placeholder, placeholder)
    vampytest.assert_eq(copy.channel_types, tuple(channel_types))


def test__ComponentMetadataChannelSelect__copy_with__1():
    """
    Tests whether ``ComponentMetadataChannelSelect.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    new_custom_id = 'uta'
    old_enabled = False
    new_enabled = True
    old_max_values = 10
    new_max_values = 11
    old_min_values = 9
    new_min_values = 8
    old_placeholder = 'swing'
    new_placeholder = 'kotoba'
    old_channel_types = [ChannelType.private]
    new_channel_types = [ChannelType.guild_text, ChannelType.guild_voice]
    
    keyword_parameters = {
        'custom_id': old_custom_id,
        'enabled': old_enabled,
        'max_values': old_max_values,
        'min_values': old_min_values,
        'placeholder': old_placeholder,
        'channel_types': old_channel_types,
    }
    
    component_metadata = ComponentMetadataChannelSelect(keyword_parameters)
    copy = component_metadata.copy_with({
        'custom_id': new_custom_id,
        'enabled': new_enabled,
        'max_values': new_max_values,
        'min_values': new_min_values,
        'placeholder': new_placeholder,
        'channel_types': new_channel_types,
    })
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.placeholder, new_placeholder)
    vampytest.assert_eq(copy.channel_types, tuple(new_channel_types))
