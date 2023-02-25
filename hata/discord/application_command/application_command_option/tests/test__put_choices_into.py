import vampytest

from ...application_command_option_choice import ApplicationCommandOptionChoice

from ..fields import put_choices_into


def test__put_choices_into():
    """
    Tests whether ``put_choices_into`` works as intended.
    
    Case: passing.
    """
    choice_0 = ApplicationCommandOptionChoice('suika')
    choice_1 = ApplicationCommandOptionChoice('suwako')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'choices': []}),
        ((choice_0,), False, {'choices': [choice_0.to_data()]}),
        ((choice_0, choice_1), False, {'choices': [choice_0.to_data(), choice_1.to_data()]}),
    ):
        output = put_choices_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
