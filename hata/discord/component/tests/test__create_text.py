import vampytest

from ..component import Component, ComponentType
from ..utils import create_text


def test__create_text():
    """
    Tests whether ``create_text`` works as intended.
    """
    content = 'orin'
    
    component = create_text(
        content = content,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.text)
    vampytest.assert_eq(component.content, content)
