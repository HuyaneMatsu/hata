import vampytest

from ..component import Component, ComponentType
from ..media_info import MediaInfo
from ..utils import create_section


def test__create_section():
    """
    Tests whether ``create_section`` works as intended.
    """
    sub_component_0 = Component(ComponentType.text_display, content = 'Orin')
    sub_component_1 = Component(ComponentType.text_display, content = 'Dancing')
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo('attachment://orin.png'),
    )
    
    component = create_section(
        sub_component_0,
        sub_component_1,
        thumbnail = thumbnail,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.section)
    vampytest.assert_eq(component.components, (sub_component_0, sub_component_1))
    vampytest.assert_eq(component.thumbnail, thumbnail)
