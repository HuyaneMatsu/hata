import vampytest

from ....core import BUILTIN_EMOJIS

from ..button import ComponentMetadataButton
from ..preinstanced import ButtonStyle

from .test__ComponentMetadataButton__constructor import _assert_fields_set


def test__ComponentMetadataButton__copy():
    """
    Tests whether ``ComponentMetadataButton.copy`` works as intended.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        url = url,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_is(copy.button_style, button_style)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_is(copy.emoji, emoji)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.label, label)


def test__ComponentMetadataButton__copy_with__0():
    """
    Tests whether ``ComponentMetadataButton.copy_with`` works as intended.
    
    Case: no fields.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        url = url,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_is(copy.button_style, button_style)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_is(copy.emoji, emoji)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.label, label)


def test__ComponentMetadataButton__copy_with__1():
    """
    Tests whether ``ComponentMetadataButton.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_button_style = ButtonStyle.green
    new_button_style = ButtonStyle.red
    old_custom_id = 'orin'
    new_custom_id = 'okuu'
    old_emoji = BUILTIN_EMOJIS['heart']
    new_emoji = BUILTIN_EMOJIS['knife']
    old_enabled = False
    new_enabled = True
    old_label = 'frost'
    new_label = 'fragment'
    old_url = None
    new_url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = old_button_style,
        custom_id = old_custom_id,
        emoji = old_emoji,
        enabled = old_enabled,
        label = old_label,
        url = old_url,
    )
    copy = component_metadata.copy_with(
        button_style = new_button_style,
        custom_id = new_custom_id,
        emoji = new_emoji,
        enabled = new_enabled,
        label = new_label,
        url = new_url,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_is(copy.button_style, new_button_style)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.url, new_url)


def test__ComponentMetadataButton__copy_with_keyword_parameters__0():
    """
    Tests whether ``ComponentMetadataButton.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        url = url,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_is(copy.button_style, button_style)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_is(copy.emoji, emoji)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.label, label)


def test__ComponentMetadataButton__copy_with_keyword_parameters__1():
    """
    Tests whether ``ComponentMetadataButton.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_button_style = ButtonStyle.green
    new_button_style = ButtonStyle.red
    old_custom_id = 'orin'
    new_custom_id = 'okuu'
    old_emoji = BUILTIN_EMOJIS['heart']
    new_emoji = BUILTIN_EMOJIS['knife']
    old_enabled = False
    new_enabled = True
    old_label = 'frost'
    new_label = 'fragment'
    old_url = None
    new_url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = old_button_style,
        custom_id = old_custom_id,
        emoji = old_emoji,
        enabled = old_enabled,
        label = old_label,
        url = old_url,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'button_style': new_button_style,
        'custom_id': new_custom_id,
        'emoji': new_emoji,
        'enabled': new_enabled,
        'label': new_label,
        'url': new_url,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_is(copy.button_style, new_button_style)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.url, new_url)
