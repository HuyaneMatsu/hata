import vampytest

from ...component import Component, ComponentType

from ..fields import validate_components


def test__validate_components__0():
    """
    Tests whether ``validate_components`` works as intended.
    
    Case: passing.
    """
    component = Component(ComponentType.button, label = 'hello')
    row = Component(ComponentType.row, components = [component])
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([component], (row, )),
        ([row], (row, )),
    ):
        output = validate_components(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_components__1():
    """
    Tests whether ``validate_components`` works as intended.
    
    Case: `TypeError`.
    """
    component = Component(ComponentType.button, label = 'hello')
    
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_components(input_value)
