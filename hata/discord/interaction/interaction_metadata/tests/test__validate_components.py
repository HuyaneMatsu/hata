import vampytest

from ...interaction_component import InteractionComponent

from ..fields import validate_components


def test__validate_components__0():
    """
    Tests whether `validate_components` works as intended.
    
    Case: passing.
    """
    component = InteractionComponent(custom_id = 'fury')
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([component], (component, )),
    ):
        output = validate_components(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_components__1():
    """
    Tests whether `validate_components` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_components(input_value)
