import vampytest

from ..component import Component, ComponentType

from ..utils import create_checkbox


def test__create_checkbox():
    """
    Tests whether ``create_checkbox`` works as intended.
    """
    custom_id = 'orin'
    default = True
    
    component = create_checkbox(
        custom_id = custom_id,
        default = default,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.checkbox)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.default, default)
