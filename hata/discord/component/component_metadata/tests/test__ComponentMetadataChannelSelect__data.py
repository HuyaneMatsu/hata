import vampytest

from ....channel import ChannelType

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..channel_select import ComponentMetadataChannelSelect

from .test__ComponentMetadataChannelSelect__constructor import _assert_fields_set


def test__ComponentMetadataChannelSelect__from_data():
    """
    Tests whether ``ComponentMetadataChannelSelect.from_data`` works as intended.
    """
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130008)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    data = {
        'channel_types': [channel_type.value for channel_type in channel_types],
        'custom_id': custom_id,
        'default_values': [default_value.to_data() for default_value in default_values],
        'disabled': not enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'required': required,
    }
    
    component_metadata = ComponentMetadataChannelSelect.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.channel_types, tuple(channel_types))
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.required, required)


def test__ComponentMetadataChannelSelect__to_data():
    """
    Tests whether ``ComponentMetadataChannelSelect.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130009)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataChannelSelect(
        channel_types = channel_types,
        custom_id = custom_id,
        default_values = default_values,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        required = required,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'channel_types': [channel_type.value for channel_type in channel_types],
            'custom_id': custom_id,
            'default_values': [default_value.to_data(defaults = True) for default_value in default_values],
            'disabled': not enabled,
            'max_values': max_values,
            'min_values': min_values,
            'placeholder': placeholder,
            'required': required,
        },
    )
