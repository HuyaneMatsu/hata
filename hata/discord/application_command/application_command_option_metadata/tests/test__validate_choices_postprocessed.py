import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..fields import validate_choices_postprocessed


def test__validate_choices_postprocessed__0():
    """
    Tests whether ``validate_choices_postprocessed`` works as intended.
    
    Case: passing.
    """
    choice_0 = ApplicationCommandOptionChoice('suika')
    choice_1 = ApplicationCommandOptionChoice('suwako')
    
    for input_data, input_type, expected_output in (
        (None, int, None),
        ([], int, None),
        ([choice_0], str, (choice_0,)),
        ([choice_0, choice_1], str, (choice_0, choice_1,)),
        ([choice_0 for _ in range(30)], str, (*(choice_0 for _ in range(25)),))
    ):
        output = validate_choices_postprocessed(input_data, input_type)
        vampytest.assert_eq(output, expected_output)


def test__validate_choices_postprocessed__1():
    """
    Tests whether ``validate_choices_postprocessed`` works as intended.
    
    Case: `TypeError`.
    """
    choice_0 = ApplicationCommandOptionChoice('suika')
    
    for input_data, option_type in (
        (12.6, object),
        (ApplicationCommandOptionChoice('suika'), float),
    ):
        with vampytest.assert_raises(TypeError):
            validate_choices_postprocessed(input_data, option_type)
