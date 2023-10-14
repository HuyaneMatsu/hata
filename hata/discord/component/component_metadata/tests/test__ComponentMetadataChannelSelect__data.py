import vampytest

from ....channel import ChannelType

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..channel_select import ComponentMetadataChannelSelect

from .test__ComponentMetadataChannelSelect__constructor import _assert_fields_set


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
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130008)]
    
    data = {
        'custom_id': custom_id,
        'disabled': not enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'channel_types': [channel_type.value for channel_type in channel_types],
        'default_values': [default_value.to_data() for default_value in default_values],
    }
    
    component_metadata = ComponentMetadataChannelSelect.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.channel_types, tuple(channel_types))
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))


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
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130009)]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
    )
    
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
            'default_values': [default_value.to_data(defaults = True) for default_value in default_values],
        },
    )
