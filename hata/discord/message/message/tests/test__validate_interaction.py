import vampytest

from ...message_interaction import MessageInteraction

from ..fields import validate_interaction


def test__validate_interaction__0():
    """
    Tests whether `validate_interaction` works as intended.
    
    Case: passing.
    """
    interaction_id = 202304300005
    interaction = MessageInteraction.precreate(interaction_id, name = 'Orin')
    
    for input_value, expected_output in (
        (None, None),
        (interaction, interaction),
    ):
        output = validate_interaction(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_interaction__1():
    """
    Tests whether `validate_interaction` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_interaction(input_value)
