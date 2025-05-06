import vampytest

from ...color import Color

from ..component import Component, ComponentType
from ..utils import create_container


def test__create_container():
    """
    Tests whether ``create_container`` works as intended.
    """
    color = Color.from_rgb(5, 7, 3)
    sub_component_0 = Component(ComponentType.text_display, content = 'Fire')
    sub_component_1 = Component(ComponentType.row)
    spoiler = True
    
    component = create_container(
        sub_component_0,
        sub_component_1,
        color = color,
        spoiler = spoiler,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.container)
    vampytest.assert_eq(component.color, color)
    vampytest.assert_eq(component.components, (sub_component_0, sub_component_1))
    vampytest.assert_eq(component.spoiler, spoiler)
