import vampytest

from ....channel import ChannelType
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...component_metadata import ButtonStyle, TextInputStyle
from ...string_select_option import StringSelectOption

from ..component import Component
from ..preinstanced import ComponentType


def test__Component__proxies__0():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading defaults.
    """
    component = Component(ComponentType.none)
    
    vampytest.assert_instance(component.button_style, ButtonStyle)
    vampytest.assert_instance(component.channel_types, tuple, nullable = True)
    vampytest.assert_instance(component.components, tuple, nullable = True)
    vampytest.assert_instance(component.custom_id, str, nullable = True)
    vampytest.assert_instance(component.emoji, Emoji, nullable = True)
    vampytest.assert_instance(component.enabled, bool)
    vampytest.assert_instance(component.label, str, nullable = True)
    vampytest.assert_instance(component.max_length, int)
    vampytest.assert_instance(component.max_values, int)
    vampytest.assert_instance(component.min_length, int)
    vampytest.assert_instance(component.min_values, int)
    vampytest.assert_instance(component.options, tuple, nullable = True)
    vampytest.assert_instance(component.placeholder, str, nullable = True)
    vampytest.assert_instance(component.required, bool)
    vampytest.assert_instance(component.text_input_style, TextInputStyle)
    vampytest.assert_instance(component.url, str, nullable = True)
    vampytest.assert_instance(component.value, str, nullable = True)


def test__Component__proxies__1():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading button fields.
    """
    emoji = BUILTIN_EMOJIS['x']
    enabled = False
    label = 'fujiwara'
    url = 'https://orindance.party/'
    
    component = Component(
        ComponentType.button,
        emoji = emoji,
        enabled = enabled,
        label = label,
        url = url,
    )
    
    vampytest.assert_is(component.emoji, emoji)
    vampytest.assert_eq(component.enabled, enabled)
    vampytest.assert_eq(component.label, label)
    vampytest.assert_eq(component.url, url)


def test__Component__proxies__2():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading channel select fields.
    """
    channel_types = [ChannelType.private]
    custom_id = 'kaguya'
    max_values = 10
    min_values = 9
    placeholder = 'gear'
    
    component = Component(
        ComponentType.channel_select,
        channel_types = channel_types,
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )
    
    vampytest.assert_eq(component.channel_types, tuple(channel_types))
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.placeholder, placeholder)


def test__Component__proxies__3():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading row fields.
    """
    components = [Component(ComponentType.button, label = 'mokou')]
    
    component = Component(
        ComponentType.row,
        components = components,
    )
    
    vampytest.assert_eq(component.components, tuple(components))


def test__Component__proxies__4():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading text input fields.
    """
    max_length = 10
    min_length = 9
    text_input_style = TextInputStyle.paragraph
    value = 'reisen'
    
    component = Component(
        ComponentType.text_input,
        max_length = max_length,
        min_length = min_length,
        text_input_style = text_input_style,
        value = value,
    )
    
    vampytest.assert_eq(component.max_length, max_length)
    vampytest.assert_eq(component.min_length, min_length)
    vampytest.assert_is(component.text_input_style, text_input_style)
    vampytest.assert_eq(component.value, value)


def test__Component__proxies__5():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading string select fields.
    """
    options = [StringSelectOption('yume')]
    
    component = Component(
        ComponentType.string_select,
        options = options,
    )
    
    vampytest.assert_eq(component.options, tuple(options))


def test__Component__proxies__6():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading button fields (Button style only).
    """
    button_style = ButtonStyle.red
    
    component = Component(
        ComponentType.button,
        button_style = button_style,
    )
    
    vampytest.assert_is(component.button_style, button_style)




def test__Component__proxies__7():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing button fields.
    """
    emoji = BUILTIN_EMOJIS['x']
    enabled = False
    label = 'fujiwara'
    url = 'https://orindance.party/'
    
    component = Component(ComponentType.button)
    
    component.emoji = emoji
    component.enabled = enabled
    component.label = label
    component.url = url
    
    vampytest.assert_is(component.emoji, emoji)
    vampytest.assert_eq(component.enabled, enabled)
    vampytest.assert_eq(component.label, label)
    vampytest.assert_eq(component.url, url)


def test__Component__proxies__8():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing channel select fields.
    """
    channel_types = [ChannelType.private]
    custom_id = 'kaguya'
    max_values = 10
    min_values = 9
    placeholder = 'gear'
    
    component = Component(ComponentType.channel_select)
    
    component.channel_types = channel_types
    component.custom_id = custom_id
    component.max_values = max_values
    component.min_values = min_values
    component.placeholder = placeholder
    
    vampytest.assert_eq(component.channel_types, tuple(channel_types))
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.placeholder, placeholder)


def test__Component__proxies__9():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing row fields.
    """
    components = [Component(ComponentType.button, label = 'mokou')]
    
    component = Component(ComponentType.row)
    
    component.components = components
    
    vampytest.assert_eq(component.components, tuple(components))


def test__Component__proxies__10():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing text input fields.
    """
    max_length = 10
    min_length = 9
    text_input_style = TextInputStyle.paragraph
    value = 'reisen'
    
    component = Component(ComponentType.text_input)
    
    component.max_length = max_length
    component.min_length = min_length
    component.text_input_style = text_input_style
    component.value = value
    
    vampytest.assert_eq(component.max_length, max_length)
    vampytest.assert_eq(component.min_length, min_length)
    vampytest.assert_is(component.text_input_style, text_input_style)
    vampytest.assert_eq(component.value, value)


def test__Component__proxies__11():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing string select fields.
    """
    options = [StringSelectOption('yume')]
    
    component = Component(ComponentType.string_select)
    
    component.options = options
    
    vampytest.assert_eq(component.options, tuple(options))


def test__Component__proxies__12():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing button fields (Button style only).
    """
    button_style = ButtonStyle.red
    
    component = Component(ComponentType.button)
    
    component.button_style = button_style
    
    vampytest.assert_is(component.button_style, button_style)
