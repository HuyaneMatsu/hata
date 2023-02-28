import vampytest

from ...application_command_option import ApplicationCommandOption, ApplicationCommandOptionType

from ..fields import put_options_into


def test__put_options_into():
    """
    Tests whether ``put_options_into`` is working as intended.
    """
    option_0 = ApplicationCommandOption('ibuki', 'suika', ApplicationCommandOptionType.integer)
    option_1 = ApplicationCommandOption('ibuki', 'suika', ApplicationCommandOptionType.string)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'options': []}),
        ((option_0, ), False, {'options': [option_0.to_data()]}),
        ((option_0, option_1), False, {'options': [option_0.to_data(), option_1.to_data()]}),
    ):
        data = put_options_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
