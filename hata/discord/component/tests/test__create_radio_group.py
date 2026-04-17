import vampytest

from ..radio_group_option import RadioGroupOption
from ..component import Component, ComponentType

from ..utils import create_radio_group


def test__create_radio_group():
    """
    Tests whether ``create_radio_group`` works as intended.
    """
    custom_id = 'orin'
    options = [RadioGroupOption('yume')]
    required = True
    
    component = create_radio_group(
        custom_id = custom_id,
        options = options,
        required = required,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.radio_group)
    vampytest.assert_eq(component.custom_id, custom_id)
    vampytest.assert_eq(component.options, tuple(options))
    vampytest.assert_eq(component.required, required)
