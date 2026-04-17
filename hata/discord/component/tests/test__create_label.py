import vampytest

from ..component import Component, ComponentType
from ..utils import create_label


def test__create_label():
    """
    Tests whether ``create_label`` works as intended.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component = create_label(
        label,
        description,
        sub_component,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.label)
    vampytest.assert_eq(component.component, sub_component)
    vampytest.assert_eq(component.description, description)
    vampytest.assert_eq(component.label, label)
