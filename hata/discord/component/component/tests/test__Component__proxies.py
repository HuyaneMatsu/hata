import vampytest

from ....channel import ChannelType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ...component_metadata import ButtonStyle, SeparatorSpacingSize, TextInputStyle
from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType
from ...media_info import MediaInfo
from ...media_item import MediaItem
from ...string_select_option import StringSelectOption

from ..component import Component
from ..preinstanced import ComponentType


def test__Component__proxies__reading_defaults():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading defaults.
    """
    component = Component(ComponentType.none)
    
    vampytest.assert_instance(component.button_style, ButtonStyle)
    vampytest.assert_instance(component.channel_types, tuple, nullable = True)
    vampytest.assert_instance(component.color, Color, nullable = True)
    vampytest.assert_instance(component.components, tuple, nullable = True)
    vampytest.assert_instance(component.content, str, nullable = True)
    vampytest.assert_instance(component.custom_id, str, nullable = True)
    vampytest.assert_instance(component.default_values, tuple, nullable = True)
    vampytest.assert_instance(component.description, str, nullable = True)
    vampytest.assert_instance(component.emoji, Emoji, nullable = True)
    vampytest.assert_instance(component.enabled, bool)
    vampytest.assert_instance(component.divider, bool)
    vampytest.assert_instance(component.label, str, nullable = True)
    vampytest.assert_instance(component.items, tuple, nullable = True)
    vampytest.assert_instance(component.max_length, int)
    vampytest.assert_instance(component.max_values, int)
    vampytest.assert_instance(component.media, MediaInfo, nullable = True)
    vampytest.assert_instance(component.min_length, int)
    vampytest.assert_instance(component.min_values, int)
    vampytest.assert_instance(component.options, tuple, nullable = True)
    vampytest.assert_instance(component.placeholder, str, nullable = True)
    vampytest.assert_instance(component.required, bool)
    vampytest.assert_instance(component.sku_id, int)
    vampytest.assert_instance(component.spacing_size, SeparatorSpacingSize)
    vampytest.assert_instance(component.spoiler, bool)
    vampytest.assert_instance(component.text_input_style, TextInputStyle)
    vampytest.assert_instance(component.url, str, nullable = True)
    vampytest.assert_instance(component.value, str, nullable = True)


def test__Component__proxies__read_button__generic():
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


def test__Component__proxies__read_button__sku_id():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading button fields with sku id.
    """
    sku_id = 202405180079
    
    component = Component(
        ComponentType.button,
        sku_id = sku_id,
    )
    
    vampytest.assert_eq(component.sku_id, sku_id)


def test__Component__proxies__read_channel_select():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading channel select fields.
    """
    channel_types = [ChannelType.private]
    custom_id = 'kaguya'
    max_values = 10
    min_values = 9
    placeholder = 'gear'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130050)]
    
    component = Component(
        ComponentType.channel_select,
        channel_types = channel_types,
        custom_id = custom_id,
        default_values = default_values,
        max_values = max_values,
        min_values = min_values,
        placeholder = placeholder,
    )
    
    vampytest.assert_eq(component.channel_types, tuple(channel_types))
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.default_values, tuple(default_values))
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.placeholder, placeholder)


def test__Component__proxies__read_row():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading row fields.
    """
    components = [
        Component(ComponentType.button, label = 'mokou'),
    ]
    
    component = Component(
        ComponentType.row,
        components = components,
    )
    
    vampytest.assert_eq(component.components, tuple(components))



def test__Component__proxies__read_section():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading section fields.
    """
    components = [
        Component(ComponentType.text_display, content = 'mokou'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component = Component(
        ComponentType.section,
        components = components,
        thumbnail = thumbnail,
    )
    
    vampytest.assert_eq(component.components, tuple(components))
    vampytest.assert_eq(component.thumbnail, thumbnail)


def test__Component__proxies__read_text_input():
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


def test__Component__proxies__read_string_select():
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


def test__Component__proxies__read_button_style():
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


def test__Component__proxies__read_text_display():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading text fields.
    """
    content = 'remilia'
    
    component = Component(
        ComponentType.text_display,
        content = content,
    )
    
    vampytest.assert_eq(component.content, content)


def test__Component__proxies__read_thumbnail_media():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading thumbnail media.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component = Component(
        ComponentType.thumbnail_media,
        description = description,
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_eq(component.description, description)
    vampytest.assert_eq(component.media, media)
    vampytest.assert_eq(component.spoiler, spoiler)


def test__Component__proxies__read_media_gallery():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading media gallery.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component = Component(
        ComponentType.media_gallery,
        items = items,
    )
    
    vampytest.assert_eq(component.items, tuple(items))


def test__Component__proxies__read_attachment_media():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading attachment media.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component = Component(
        ComponentType.attachment_media,
        media = media,
        spoiler = spoiler,
    )
    
    vampytest.assert_eq(component.media, media)
    vampytest.assert_eq(component.spoiler, spoiler)


def test__Component__proxies__read_separator():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading separator.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component = Component(
        ComponentType.separator,
        divider = divider,
        spacing_size = spacing_size,
    )
    
    vampytest.assert_eq(component.divider, divider)
    vampytest.assert_is(component.spacing_size, spacing_size)



def test__Component__proxies__read_container():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading container fields.
    """
    color = Color.from_rgb(5, 6, 7)
    components = [
        Component(ComponentType.text_display, content = 'mokou'),
    ]
    spoiler = True
    
    component = Component(
        ComponentType.container,
        color = color,
        components = components,
        spoiler = spoiler
    )
    
    vampytest.assert_eq(component.color, color)
    vampytest.assert_eq(component.components, tuple(components))
    vampytest.assert_eq(component.spoiler, spoiler)


def test__Component__proxies__write_button__generic():
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


def test__Component__proxies__write_button():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing button fields.
    """
    sku_id = 202405180082
    
    component = Component(ComponentType.button)
    
    component.sku_id = sku_id
    
    vampytest.assert_eq(component.sku_id, sku_id)


def test__Component__proxies__write_channel_select():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing channel select fields.
    """
    channel_types = [ChannelType.private]
    custom_id = 'kaguya'
    max_values = 10
    min_values = 9
    placeholder = 'gear'
    default_values = [EntitySelectDefaultValue(EntitySelectDefaultValueType.channel, 202310130050)]
    
    component = Component(ComponentType.channel_select)
    
    component.channel_types = channel_types
    component.custom_id = custom_id
    component.max_values = max_values
    component.min_values = min_values
    component.placeholder = placeholder
    component.default_values = default_values
    
    vampytest.assert_eq(component.channel_types, tuple(channel_types))
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.default_values, tuple(default_values))
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.placeholder, placeholder)


def test__Component__proxies__write_section():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing section fields.
    """
    components = [
        Component(ComponentType.button, label = 'mokou'),
    ]
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component = Component(ComponentType.section)
    
    component.components = components
    component.thumbnail = thumbnail
    
    vampytest.assert_eq(component.components, tuple(components))
    vampytest.assert_eq(component.thumbnail, thumbnail)


def test__Component__proxies__write_row():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing row fields.
    """
    components = [
        Component(ComponentType.button, label = 'mokou'),
    ]
    
    component = Component(ComponentType.row)
    
    component.components = components
    
    vampytest.assert_eq(component.components, tuple(components))


def test__Component__proxies__write_text_input():
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


def test__Component__proxies__write_string_select():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing string select fields.
    """
    options = [StringSelectOption('yume')]
    
    component = Component(ComponentType.string_select)
    
    component.options = options
    
    vampytest.assert_eq(component.options, tuple(options))


def test__Component__proxies__write_button_style():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing button fields (Button style only).
    """
    button_style = ButtonStyle.red
    
    component = Component(ComponentType.button)
    
    component.button_style = button_style
    
    vampytest.assert_is(component.button_style, button_style)


def test__Component__proxies__write_text_display():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing text fields.
    """
    content = 'remilia'
    
    component = Component(ComponentType.text_display)
    
    component.content = content
    
    vampytest.assert_eq(component.content, content)


def test__Component__proxies__write_thumbnail_media():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading thumbnail media.
    """
    description = 'Its Orin <3'
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component = Component(
        ComponentType.thumbnail_media,
    )
    
    component.description = description
    component.media = media
    component.spoiler = spoiler
    
    vampytest.assert_eq(component.description, description)
    vampytest.assert_eq(component.media, media)
    vampytest.assert_eq(component.spoiler, spoiler)


def test__Component__proxies__write_media_gallery():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing media gallery fields.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component = Component(ComponentType.media_gallery)
    
    component.items = items
    
    vampytest.assert_eq(component.items, tuple(items))


def test__Component__proxies__write_attachment_media():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: reading attachment media.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component = Component(
        ComponentType.attachment_media,
    )
    
    component.media = media
    component.spoiler = spoiler
    
    vampytest.assert_eq(component.media, media)
    vampytest.assert_eq(component.spoiler, spoiler)


def test__Component__proxies__write_separator():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing separator fields.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component = Component(ComponentType.separator)
    
    component.divider = divider
    component.spacing_size = spacing_size
    
    vampytest.assert_eq(component.divider, divider)
    vampytest.assert_is(component.spacing_size, spacing_size)


def test__Component__proxies__write_container():
    """
    Tests whether ``Component`` field proxies work as intended.
    
    Case: writing container fields.
    """
    color = Color.from_rgb(5, 6, 7)
    components = [
        Component(ComponentType.text_display, content = 'mokou'),
    ]
    spoiler = True
    
    component = Component(
        ComponentType.container,
    )
    
    component.color = color
    component.components = components
    component.spoiler = spoiler
    
    vampytest.assert_eq(component.color, color)
    vampytest.assert_eq(component.components, tuple(components))
    vampytest.assert_eq(component.spoiler, spoiler)
