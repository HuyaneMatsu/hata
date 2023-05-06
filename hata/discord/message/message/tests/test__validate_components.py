import vampytest

from ....component import Component, ComponentType

from ..fields import validate_components


def test__validate_components__0():
    """
    Tests whether ``validate_components`` works as intended.
    
    Case: passing.
    """
    component_0 = Component(ComponentType.button, label = 'Hell')
    component_1 = Component(ComponentType.row, components = Component(ComponentType.button, label = 'Rose'))
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([component_0], (component_0, )),
        ([component_0, component_1], (component_0, component_1)),
    ):
        output = validate_components(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_components__1():
    """
    Tests whether ``validate_components`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_components(input_value)
