import vampytest

from ..component import Component, ComponentType
from ..utils import create_text_display


def test__create_text_display():
    """
    Tests whether ``create_text_display`` works as intended.
    """
    content = 'orin'
    
    component = create_text_display(
        content = content,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.text_display)
    vampytest.assert_eq(component.content, content)
