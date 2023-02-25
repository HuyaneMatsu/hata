import vampytest

from ..constants import APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT
from ..fields import put_min_length_into


def test__put_min_length_into():
    """
    Tests whether ``put_min_length_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT, False, {}),
        (
            APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT,
            True,
            {'min_length': APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT},
        ),
        (10, False, {'min_length': 10}),
    ):
        data = put_min_length_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
