import vampytest

from ....component import Component, ComponentType

from ..fields import put_components_into


def test__put_components_into():
    """
    Tests whether ``put_components_into`` works as intended.
    """
    component_0 = Component(ComponentType.button, label = 'Hell')
    component_1 = Component(ComponentType.row, components = Component(ComponentType.button, label = 'Rose'))
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'components': []}),
        ((component_0, ), False, {'components': [component_0.to_data()]},),
        (
            (component_0, component_1),
            True,
            {'components': [component_0.to_data(defaults = True), component_1.to_data(defaults = True)]},
        ),
    ):
        output = put_components_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
