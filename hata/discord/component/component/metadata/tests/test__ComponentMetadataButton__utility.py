import vampytest

from .....core import BUILTIN_EMOJIS

from ...preinstanced import ButtonStyle

from ..button import ComponentMetadataButton

from .test__ComponentMetadataButton__constructor import _check_is_all_attribute_set


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
    
    keyword_parameters = {
        'button_style': button_style,
        'custom_id': custom_id,
        'emoji': emoji,
        'enabled': enabled,
        'label': label,
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    copy = component_metadata.copy()
    
    _check_is_all_attribute_set(copy)
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
    
    keyword_parameters = {
        'button_style': button_style,
        'custom_id': custom_id,
        'emoji': emoji,
        'enabled': enabled,
        'label': label,
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    copy = component_metadata.copy_with({})
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_is(copy.button_style, button_style)
    vampytest.assert_eq(copy.custom_id, custom_id)
    vampytest.assert_is(copy.emoji, emoji)
    vampytest.assert_eq(copy.enabled, enabled)
    vampytest.assert_eq(copy.label, label)


def test__ComponentMetadataButton__copy_with():
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
    
    keyword_parameters = {
        'button_style': old_button_style,
        'custom_id': old_custom_id,
        'emoji': old_emoji,
        'enabled': old_enabled,
        'label': old_label,
        'url': old_url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    copy = component_metadata.copy_with({
        'button_style': new_button_style,
        'custom_id': new_custom_id,
        'emoji': new_emoji,
        'enabled': new_enabled,
        'label': new_label,
        'url': new_url,
    })
    
    _check_is_all_attribute_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_is(copy.button_style, new_button_style)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.label, new_label)
    vampytest.assert_eq(copy.url, new_url)
