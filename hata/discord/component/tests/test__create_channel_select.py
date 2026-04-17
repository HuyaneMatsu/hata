import vampytest

from ...channel import ChannelType

from ..component import Component, ComponentType

from ..utils import create_channel_select


def test__create_channel_select():
    """
    Tests whether ``create_channel_select`` works as intended.
    """
    custom_id = 'orin'
    enabled = False
    placeholder = 'amai'
    max_values = 8
    min_values = 7
    channel_types = [ChannelType.private]
    required = True
    
    component = create_channel_select(
        custom_id = custom_id,
        enabled = enabled,
        placeholder = placeholder,
        max_values = max_values,
        min_values = min_values,
        channel_types = channel_types,
        required = required,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.channel_select)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.enabled, enabled)
    vampytest.assert_eq(component.placeholder, placeholder)
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.channel_types, tuple(channel_types))
    vampytest.assert_eq(component.required, required)
