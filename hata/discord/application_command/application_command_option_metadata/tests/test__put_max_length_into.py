import vampytest

from ..constants import APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX
from ..fields import put_max_length_into


def test__put_max_length_into():
    """
    Tests whether ``put_max_length_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (
            APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT,
            False,
            {'max_length': APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX},
        ), (
            APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX,
            False,
            {'max_length': APPLICATION_COMMAND_OPTION_MAX_LENGTH_MAX},
        ), (
            10,
            False,
            {'max_length': 10},
        ),
    ):
        data = put_max_length_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
