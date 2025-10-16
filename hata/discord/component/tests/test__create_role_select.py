import vampytest

from ..component import Component, ComponentType

from ..utils import create_role_select


def test__create_role_select():
    """
    Tests whether ``create_role_select`` works as intended.
    """
    custom_id = 'orin'
    enabled = False
    placeholder = 'amai'
    max_values = 8
    min_values = 7
    required = True
    
    component = create_role_select(
        custom_id = custom_id,
        enabled = enabled,
        placeholder = placeholder,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.role_select)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.enabled, enabled)
    vampytest.assert_eq(component.placeholder, placeholder)
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.required, required)
