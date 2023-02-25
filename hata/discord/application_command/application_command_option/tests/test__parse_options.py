import vampytest

from ..application_command_option import ApplicationCommandOption
from ..fields import parse_options
from ..preinstanced import ApplicationCommandOptionType


def test__parse_options():
    """
    Tests whether ``parse_options`` works as intended.
    """
    option_0 = ApplicationCommandOption('ibuki', 'suika', ApplicationCommandOptionType.integer)
    option_1 = ApplicationCommandOption('ibuki', 'suika', ApplicationCommandOptionType.string)
    
    for input_data, expected_output in (
        ({}, None),
        ({'options': None}, None),
        ({'options': []}, None),
        ({'options': [option_0.to_data()]}, (option_0,)),
        ({'options': [option_0.to_data(), option_1.to_data()]}, (option_0, option_1)),
    ):
        output = parse_options(input_data)
        vampytest.assert_eq(output, expected_output)
