import vampytest

from .....channel import ChannelType

from ..channel_select import ComponentMetadataChannelSelect

from .test__ComponentMetadataChannelSelect__constructor import _check_is_all_attribute_set


def test__ComponentMetadataChannelSelect__from_data():
    """
    Tests whether ``ComponentMetadataChannelSelect.from_data`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    
    data = {
        'custom_id': custom_id,
        'disabled': not enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'channel_types': [channel_type.value for channel_type in channel_types],
    }
    
    component_metadata = ComponentMetadataChannelSelect.from_data(data)
    _check_is_all_attribute_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.channel_types, tuple(channel_types))


def test__ComponentMetadataChannelSelect__to_data():
    """
    Tests whether ``ComponentMetadataChannelSelect.to_data`` works as intended.
    
    Case: include defaults.
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
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {
            'custom_id': custom_id,
            'disabled': not enabled,
            'max_values': max_values,
            'min_values': min_values,
            'placeholder': placeholder,
            'channel_types': [channel_type.value for channel_type in channel_types],
        },
    )
