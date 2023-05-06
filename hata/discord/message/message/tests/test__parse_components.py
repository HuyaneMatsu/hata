import vampytest

from ....component import Component, ComponentType

from ..fields import parse_components


def test__parse_components():
    """
    Tests whether ``parse_components`` works as intended.
    """
    component_0 = Component(ComponentType.button, label = 'Hell')
    component_1 = Component(ComponentType.row, components = Component(ComponentType.button, label = 'Rose'))
    
    for input_value, expected_output in (
        ({}, None),
        ({'components': None}, None),
        ({'components': [component_0.to_data()]}, (component_0, )),
        ({'components': [component_0.to_data(), component_1.to_data()]}, (component_0, component_1)),
    ):
        output = parse_components(input_value)
        vampytest.assert_eq(output, expected_output)
