import vampytest

from ..component import Component, ComponentType
from ..shared_fields import put_components_into


def test__put_components_into():
    """
    Tests whether ``put_components_into`` works as intended.
    """
    component = Component(ComponentType.button, label = 'hello')
    
    for input_value, expected_output in (
        (None, {'components': []}),
        ((component, ), {'components': [component.to_data(defaults = True)]}),
    ):
        output = put_components_into(input_value, {}, True)
        vampytest.assert_eq(output, expected_output)
