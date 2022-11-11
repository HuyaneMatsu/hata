import vampytest

from ...interaction_metadata import InteractionMetadataApplicationCommand, InteractionMetadataBase

from ..fields import validate_interaction
from ..preinstanced import InteractionType


def test__validate_interaction__0():
    """
    Tests whether ``validate_interaction`` works as intended.
    
    Case: passing.
    """
    interaction_0 = InteractionMetadataApplicationCommand()
    interaction_1 = InteractionMetadataApplicationCommand(name = 'Yumemi')
    
    
    for input_value, expected_output in (
        (None, interaction_0),
        (interaction_1, interaction_1),
    ):
        output = validate_interaction(input_value, InteractionType.application_command)
        vampytest.assert_eq(output, expected_output)


def test__validate_interaction__1():
    """
    Tests whether ``validate_interaction`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        InteractionMetadataBase(),
    ):
        with vampytest.assert_raises(TypeError):
            validate_interaction(input_value, InteractionType.application_command)
