import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..button import ComponentMetadataButton
from ..preinstanced import ButtonStyle


def _assert_fields_set(component_metadata):
    """
    Checks whether the ``ComponentMetadataButton`` has all it's attributes set.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataButton)
    vampytest.assert_instance(component_metadata.button_style, ButtonStyle)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.emoji, Emoji, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.label, str, nullable = True)
    vampytest.assert_instance(component_metadata.url, str, nullable = True)


def test__ComponentMetadataButton__new__0():
    """
    Tests whether ``ComponentMetadataButton.__new__`` works as intended.
    
    Case: no fields.
    """
    component_metadata = ComponentMetadataButton()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataButton__new__1():
    """
    Tests whether ``ComponentMetadataButton.__new__`` works as intended.
    
    Case: all fields given.
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
    _assert_fields_set(component_metadata)
    vampytest.assert_is(component_metadata.button_style, button_style)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_is(component_metadata.emoji, emoji)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.label, label)
    vampytest.assert_eq(component_metadata.url, url)


def test__ComponentMetadataButton__new__2():
    """
    Tests whether ``ComponentMetadataButton.__new__`` works as intended.
    
    Case: url.
    """
    url = 'https://orindance.party/'
    
    component_metadata = ComponentMetadataButton(
        url = url,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_is(component_metadata.button_style, ButtonStyle.link)
    vampytest.assert_eq(component_metadata.url, url)



def test__ComponentMetadataButton__from_keyword_parameters__0():
    """
    Tests whether ``ComponentMetadataButton.from_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataButton.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataButton__from_keyword_parameters__1():
    """
    Tests whether ``ComponentMetadataButton.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
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
    
    component_metadata = ComponentMetadataButton.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_is(component_metadata.button_style, button_style)
    vampytest.assert_eq(component_metadata.custom_id, custom_id)
    vampytest.assert_is(component_metadata.emoji, emoji)
    vampytest.assert_eq(component_metadata.enabled, enabled)
    vampytest.assert_eq(component_metadata.label, label)
    vampytest.assert_eq(component_metadata.url, url)


def test__ComponentMetadataButton__from_keyword_parameters__2():
    """
    Tests whether ``ComponentMetadataButton.from_keyword_parameters`` works as intended.
    
    Case: url.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_is(component_metadata.button_style, ButtonStyle.link)
    vampytest.assert_eq(component_metadata.url, url)
