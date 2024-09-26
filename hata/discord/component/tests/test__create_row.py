import vampytest

from ..component import Component, ComponentType
from ..utils import create_row


def test__create_row():
    """
    Tests whether ``create_row`` works as intended.
    """
    sub_component_0 = Component(ComponentType.button)
    sub_component_1 = Component(ComponentType.string_select)
    
    component = create_row(
        sub_component_0,
        sub_component_1,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.row)
    vampytest.assert_eq(component.components, (sub_component_0, sub_component_1))
