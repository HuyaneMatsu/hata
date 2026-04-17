import vampytest

from ..component import Component, ComponentType

from ..utils import create_attachment_input


def test__create_attachment_input():
    """
    Tests whether ``create_attachment_input`` works as intended.
    """
    custom_id = 'orin'
    max_values = 8
    min_values = 7
    required = True
    
    component = create_attachment_input(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.attachment_input)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.required, required)
