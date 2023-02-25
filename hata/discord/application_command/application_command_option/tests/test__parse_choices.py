import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..fields import parse_choices


def test__parse_choices():
    """
    Tests whether ``parse_choices`` works as intended.
    
    Case: passing.
    """
    choice_0 = ApplicationCommandOptionChoice('suika')
    choice_1 = ApplicationCommandOptionChoice('suwako')
    
    for input_data, expected_output in (
        ({}, None),
        ({'choices': None}, None),
        ({'choices': []}, None),
        ({'choices': [choice_0.to_data()]}, (choice_0,)),
        ({'choices': [choice_0.to_data(), choice_1.to_data()]}, (choice_0, choice_1)),
    ):
        output = parse_choices(input_data)
        vampytest.assert_eq(output, expected_output)
