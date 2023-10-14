import vampytest

from ....channel import ChannelType

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..channel_select import ComponentMetadataChannelSelect


def test__ComponentMetadataChannelSelect__repr():
    """
    Tests whether ``ComponentMetadataChannelSelect.__repr__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130010)]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataChannelSelect__hash():
    """
    Tests whether ``ComponentMetadataChannelSelect.__hash__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130011)]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataChannelSelect__eq():
    """
    Tests whether ``ComponentMetadataChannelSelect.__eq__`` works as intended.
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130012)]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'channel_types': channel_types,
        'default_values': default_values,
    }
    
    component_metadata = ComponentMetadataChannelSelect(**keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())

    for field_name, field_value in (
        ('custom_id', 'distopia'),
        ('enabled', True),
        ('max_values', 11),
        ('min_values', 8),
        ('placeholder', 'kokoro'),
        ('channel_types', None),
        ('default_values', None),
    ):
        test_component_metadata = ComponentMetadataChannelSelect(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
