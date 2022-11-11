import vampytest

from ....component import ComponentType

from ..fields import validate_component_type


def test__validate_component_type__0():
    """
    Tests whether `validate_component_type` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (ComponentType.button, ComponentType.button),
        (ComponentType.button.value, ComponentType.button)
    ):
        output = validate_component_type(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_component_type__1():
    """
    Tests whether `validate_component_type` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_component_type(input_value)
