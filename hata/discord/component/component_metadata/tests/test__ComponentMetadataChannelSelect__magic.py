import vampytest

from ....channel import ChannelType

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..channel_select import ComponentMetadataChannelSelect


def test__ComponentMetadataChannelSelect__repr():
    """
    Tests whether ``ComponentMetadataChannelSelect.__repr__`` works as intended.
    """
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130010)]
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
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataChannelSelect__hash():
    """
    Tests whether ``ComponentMetadataChannelSelect.__hash__`` works as intended.
    """
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130011)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
        required = required,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def _iter_options__eq():
    channel_types = [ChannelType.private]
    custom_id = 'oriental'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130012)]
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    required = True
    
    keyword_parameters = {
        'channel_types': channel_types,
        'custom_id': custom_id,
        'default_values': default_values,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'required': required,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'channel_types': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'custom_id': 'distopia',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'default_values': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'enabled': True,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'max_values': 11,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'min_values': 8,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'placeholder': 'kokoro',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'required': False,
        },
        False,
    )

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ComponentMetadataChannelSelect__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataChannelSelect.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    component_metadata_0 = ComponentMetadataChannelSelect(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataChannelSelect(**keyword_parameters_1)
    
    output = component_metadata_0 == component_metadata_1
    vampytest.assert_instance(output, bool)
    return output
