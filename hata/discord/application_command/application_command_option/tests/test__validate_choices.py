import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..fields import validate_choices
from ..preinstanced import ApplicationCommandOptionType


def test__validate_choices__0():
    """
    Tests whether ``validate_choices`` works as intended.
    
    Case: passing.
    """
    choice_0 = ApplicationCommandOptionChoice('suika')
    choice_1 = ApplicationCommandOptionChoice('suwako')
    
    for input_data, expected_output in (
        (None, None),
        ([], None),
        ([choice_0], (choice_0,)),
        ([choice_0, choice_1], (choice_0, choice_1,)),
        ([choice_0 for _ in range(30)], (*(choice_0 for _ in range(25)),))
    ):
        output = validate_choices(input_data)
        vampytest.assert_eq(output, expected_output)


def test__validate_choices__1():
    """
    Tests whether ``validate_choices`` works as intended.
    
    Case: `TypeError`.
    """
    choice_0 = ApplicationCommandOptionChoice('suika')
    
    for input_data, option_type in (
        (12.6, ApplicationCommandOptionType.none),
        (ApplicationCommandOptionChoice('suika'), ApplicationCommandOptionType.float),
    ):
        with vampytest.assert_raises(TypeError):
            validate_choices(input_data, option_type)
