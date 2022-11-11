import vampytest

from ...core import BUILTIN_EMOJIS

from ..component import Component, ComponentType
from ..component_metadata import ButtonStyle
from ..utils import create_button


def test__create_button():
    """
    Tests whether ``create_button`` works as intended.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = None
    
    component = create_button(
        style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        url = url,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.button)
    vampytest.assert_is(component.button_style, button_style)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_is(component.emoji, emoji)
    vampytest.assert_eq(component.enabled, enabled)
    vampytest.assert_eq(component.label, label)
    vampytest.assert_eq(component.url, url)
