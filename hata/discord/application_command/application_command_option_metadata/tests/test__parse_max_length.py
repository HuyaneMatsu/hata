import vampytest

from ..constants import MAX_LENGTH_DEFAULT, MAX_LENGTH_MAX
from ..fields import parse_max_length


def test__parse_max_length():
    """
    Tests whether ``parse_max_length`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MAX_LENGTH_DEFAULT),
        ({'max_length': 1}, 1),
        ({'max_length': MAX_LENGTH_MAX}, MAX_LENGTH_DEFAULT),
    ):
        output = parse_max_length(input_data)
        vampytest.assert_eq(output, expected_output)
