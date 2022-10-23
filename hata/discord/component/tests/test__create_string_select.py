import vampytest

from ..component import Component, ComponentType
from ..string_select_option import StringSelectOption

from ..utils import create_string_select


def test__create_string_select():
    """
    Tests whether ``create_string_select`` works as intended.
    """
    custom_id = 'orin'
    enabled = False
    options = [StringSelectOption('yume')]
    placeholder = 'amai'
    max_values = 8
    min_values = 7
    
    component = create_string_select(
        custom_id = custom_id,
        enabled = enabled,
        options = options,
        placeholder = placeholder,
        max_values = max_values,
        min_values = min_values,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.string_select)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.enabled, enabled)
    vampytest.assert_eq(component.options, tuple(options))
    vampytest.assert_eq(component.placeholder, placeholder)
    vampytest.assert_eq(component.max_values, max_values)
    vampytest.assert_eq(component.min_values, min_values)
