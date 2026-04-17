import vampytest

from ..checkbox_group_option import CheckboxGroupOption
from ..component import Component, ComponentType

from ..utils import create_checkbox_group


def test__create_checkbox_group():
    """
    Tests whether ``create_checkbox_group`` works as intended.
    """
    custom_id = 'orin'
    options = [CheckboxGroupOption('yume')]
    max_values = 8
    min_values = 7
    required = True
    
    component = create_checkbox_group(
        custom_id = custom_id,
        options = options,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.checkbox_group)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.options, tuple(options))
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
    vampytest.assert_eq(component.required, required)
