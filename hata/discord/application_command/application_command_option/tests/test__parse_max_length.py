import vampytest

from ..constants import APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX
from ..fields import parse_max_length


def test__parse_max_length():
    """
    Tests whether ``parse_max_length`` works as intended.
    """
    for input_data, expected_output in (
        ({}, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT),
        ({'max_length': 1}, 1),
        ({'max_length': APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX}, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT),
    ):
        output = parse_max_length(input_data)
        vampytest.assert_eq(output, expected_output)
