import vampytest

from ....color import Color
from ....emoji import Emoji

from ...component import Component
from ...media_info import MediaInfo

from ..base import ComponentMetadataBase
from ..preinstanced import ButtonStyle, SeparatorSpacingSize, TextInputStyle


def test__ComponentMetadataBase__placeholders():
    """
    Tests whether ``ComponentMetadataBase``'s placeholders works as intended.
    """
    component_metadata = ComponentMetadataBase()
    
    vampytest.assert_instance(component_metadata.button_style, ButtonStyle)
    vampytest.assert_instance(component_metadata.channel_types, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.components, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.color, Color, nullable = True)
    vampytest.assert_instance(component_metadata.content, str, nullable = True)
    vampytest.assert_instance(component_metadata.custom_id, str, nullable = True)
    vampytest.assert_instance(component_metadata.default_values, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.description, str, nullable = True)
    vampytest.assert_instance(component_metadata.divider, bool)
    vampytest.assert_instance(component_metadata.emoji, Emoji, nullable = True)
    vampytest.assert_instance(component_metadata.enabled, bool)
    vampytest.assert_instance(component_metadata.items, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.label, str, nullable = True)
    vampytest.assert_instance(component_metadata.max_length, int)
    vampytest.assert_instance(component_metadata.max_values, int)
    vampytest.assert_instance(component_metadata.media, MediaInfo, nullable = True)
    vampytest.assert_instance(component_metadata.min_length, int)
    vampytest.assert_instance(component_metadata.min_values, int)
    vampytest.assert_instance(component_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(component_metadata.placeholder, str, nullable = True)
    vampytest.assert_instance(component_metadata.required, bool)
    vampytest.assert_instance(component_metadata.sku_id, int)
    vampytest.assert_instance(component_metadata.spacing_size, SeparatorSpacingSize)
    vampytest.assert_instance(component_metadata.spoiler, bool)
    vampytest.assert_instance(component_metadata.text_input_style, TextInputStyle)
    vampytest.assert_instance(component_metadata.thumbnail, Component, nullable = True)
    vampytest.assert_instance(component_metadata.url, str, nullable = True)
    vampytest.assert_instance(component_metadata.value, str, nullable = True)
