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
    sku_id = 0
    url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        sku_id = sku_id,
        url = url,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataButton__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataButton.copy_with`` works as intended.
    
    Case: no fields.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    sku_id = 0
    url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        sku_id = sku_id,
        url = url,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataButton__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataButton.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_button_style = ButtonStyle.green
    old_custom_id = 'orin'
    old_emoji = BUILTIN_EMOJIS['heart']
    old_enabled = False
    old_label = 'frost'
    old_sku_id = 0
    old_url = None
    
    
    new_button_style = ButtonStyle.red
    new_custom_id = 'okuu'
    new_emoji = BUILTIN_EMOJIS['knife']
    new_enabled = True
    new_label = 'fragment'
    new_sku_id = 0
    new_url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = old_button_style,
        custom_id = old_custom_id,
        emoji = old_emoji,
        enabled = old_enabled,
        label = old_label,
        sku_id = old_sku_id,
        url = old_url,
    )
    copy = component_metadata.copy_with(
        button_style = new_button_style,
        custom_id = new_custom_id,
        emoji = new_emoji,
        enabled = new_enabled,
        label = new_label,
        sku_id = new_sku_id,
        url = new_url,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_is(copy.button_style, new_button_style)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.sku_id, new_sku_id)
    vampytest.assert_eq(copy.url, new_url)


def test__ComponentMetadataButton__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataButton.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    sku_id = 0
    url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        sku_id = sku_id,
        url = url,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataButton__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataButton.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_button_style = ButtonStyle.green
    old_custom_id = 'orin'
    old_emoji = BUILTIN_EMOJIS['heart']
    old_enabled = False
    old_label = 'frost'
    old_sku_id = 0
    old_url = None
    
    new_button_style = ButtonStyle.red
    new_custom_id = 'okuu'
    new_emoji = BUILTIN_EMOJIS['knife']
    new_enabled = True
    new_label = 'fragment'
    new_sku_id = 0
    new_url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = old_button_style,
        custom_id = old_custom_id,
        emoji = old_emoji,
        enabled = old_enabled,
        label = old_label,
        sku_id = old_sku_id,
        url = old_url,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'button_style': new_button_style,
        'custom_id': new_custom_id,
        'emoji': new_emoji,
        'enabled': new_enabled,
        'label': new_label,
        'sku_id': new_sku_id,
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
