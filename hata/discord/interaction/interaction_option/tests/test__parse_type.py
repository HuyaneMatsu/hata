import vampytest

from ....application_command import ApplicationCommandOptionType

from ..fields import parse_type


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ApplicationCommandOptionType.none),
        ({'type': ApplicationCommandOptionType.sub_command.value}, ApplicationCommandOptionType.sub_command),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
