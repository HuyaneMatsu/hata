import vampytest

from ..component import Component, ComponentType
from ..utils import create_row


def test__create_button():
    """
    Tests whether ``create_button`` works as intended.
    """
    sub_component_1 = Component(ComponentType.button)
    sub_component_2 = Component(ComponentType.string_select)
    
    component = create_row(
        sub_component_1,
        sub_component_2,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.row)
    vampytest.assert_eq(component.components, (sub_component_1, sub_component_2))
