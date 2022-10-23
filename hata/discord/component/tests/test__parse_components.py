import vampytest

from ..component import Component, ComponentType
from ..shared_fields import parse_components


def test__parse_components():
    """
    Tests whether ``parse_components`` works as intended.
    """
    component = Component(ComponentType.button, label = 'hello')
    
    for input_value, expected_output in (
        ({}, None),
        ({'components': None}, None),
        ({'components': [component.to_data()]}, (component, )),
    ):
        output = parse_components(input_value)
        vampytest.assert_eq(output, expected_output)
