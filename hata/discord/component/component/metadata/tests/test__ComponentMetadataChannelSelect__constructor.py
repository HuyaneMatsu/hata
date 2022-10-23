import vampytest

from .....channel import ChannelType

from ..channel_select import ComponentMetadataChannelSelect


def _check_is_all_attribute_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataChannelSelect`` has all it's attributes set.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataChannelSelect)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.placeholder, str, nullable = True)
    vampytest.assert_instance(component_metadata.channel_types, tuple, nullable = True)



def test__ComponentMetadataChannelSelect__new__0():
    """
    Tests whether ``ComponentMetadataChannelSelect.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataChannelSelect(keyword_parameters)
    _check_is_all_attribute_set(component_metadata)


def test__ComponentMetadataChannelSelect__new__1():
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
    
    keyword_parameters = {
        'custom_id': custom_id,
        'enabled': enabled,
        'max_values': max_values,
        'min_values': min_values,
        'placeholder': placeholder,
        'channel_types': channel_types,
    }
    
    component_metadata = ComponentMetadataChannelSelect(keyword_parameters)
    _check_is_all_attribute_set(component_metadata)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.max_values, max_values)
    vampytest.assert_eq(component_metadata.min_values, min_values)
    vampytest.assert_eq(component_metadata.placeholder, placeholder)
    vampytest.assert_eq(component_metadata.channel_types, tuple(channel_types))
