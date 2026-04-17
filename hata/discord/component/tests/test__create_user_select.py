import vampytest

from ..component import Component, ComponentType

from ..utils import create_user_select


def test__create_user_select():
    """
    Tests whether ``create_user_select`` works as intended.
    """
    custom_id = 'orin'
    enabled = False
    placeholder = 'amai'
    max_values = 8
    min_values = 7
    required = True
    
    component = create_user_select(
        custom_id = custom_id,
        enabled = enabled,
        placeholder = placeholder,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.user_select)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.enabled, enabled)
    vampytest.assert_eq(component.placeholder, placeholder)
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.required, required)
