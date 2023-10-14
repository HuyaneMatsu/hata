import vampytest

from ....channel import ChannelType

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..channel_select import ComponentMetadataChannelSelect


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataChannelSelect`` has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataChannelSelect``
        Component metadata to check.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataChannelSelect)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.placeholder, str, nullable = True)
    vampytest.assert_instance(component_metadata.channel_types, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.default_values, tuple, nullable = True)


def test__ComponentMetadataChannelSelect__new__no_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.__new__`` works as intended.
    
    Case: no fields given.
    """
    component_metadata = ComponentMetadataChannelSelect()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataChannelSelect__new__all_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.__new__`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130006)]
    
    component_metadata = ComponentMetadataChannelSelect(
        custom_id = custom_id,
        enabled = enabled,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
        channel_types = channel_types,
        default_values = default_values,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.channel_types, tuple(channel_types))
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))


def test__ComponentMetadataChannelSelect__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataChannelSelect.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataChannelSelect__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataChannelSelect.from_keyword_parameters`` works as intended.
    
    Case: all fields given
    """
    custom_id = 'oriental'
    enabled = False
    max_values = 10
    min_values = 9
    placeholder = 'swing'
    channel_types = [ChannelType.private]
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130007)]
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'channel_types': channel_types,
        'default_values': default_values,
    }
    
    component_metadata = ComponentMetadataChannelSelect.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.channel_types, tuple(channel_types))
    vampytest.assert_eq(component_metadata.default_values, tuple(default_values))
