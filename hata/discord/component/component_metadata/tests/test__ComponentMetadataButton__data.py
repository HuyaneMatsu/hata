import vampytest

from ....core import BUILTIN_EMOJIS

from ..button import ComponentMetadataButton
from ..preinstanced import ButtonStyle

from .test__ComponentMetadataButton__constructor import _assert_fields_set


def test__ComponentMetadataButton__from_data():
    """
    Tests whether ``ComponentMetadataButton.from_data`` works as intended.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = 'https://orindance.party/'
    
    data = {
        'style': button_style.value,
        'custom_id': custom_id,
        'emoji': {'name': emoji.unicode},
        'disabled': not enabled,
        'label': label,
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_is(component_metadata.button_style, button_style)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_is(component_metadata.emoji, emoji)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.label, label)
    vampytest.assert_eq(component_metadata.url, url)


def test__ComponentMetadataButton__to_data__0():
    """
    Tests whether ``ComponentMetadataButton.to_data`` works as intended.
    
    Case: include defaults.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    enabled = False
    emoji = BUILTIN_EMOJIS['heart']
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
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {
            'style': button_style.value,
            'custom_id': custom_id,
            'emoji': {'name': emoji.unicode},
            'disabled': not enabled,
            'label': label,
            'url': url,
        },
    )

def test__ComponentMetadataButton__to_data__1():
    """
    Tests whether ``ComponentMetadataButton.to_data`` works as intended.
    
    Case: include defaults | test for `url`.
    """
    button_style = ButtonStyle.link
    custom_id = None
    enabled = False
    emoji = None
    label = 'frost'
    url = 'https://orindance.party/'
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        url = url,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {
            'style': button_style.value,
            'custom_id': custom_id,
            'emoji': emoji,
            'disabled': not enabled,
            'label': label,
            'url': url,
        },
    )
