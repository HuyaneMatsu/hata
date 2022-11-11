import vampytest

from ..constants import MIN_LENGTH_DEFAULT
from ..fields import parse_min_length


def test__parse_min_length():
    """
    Tests whether ``parse_min_length`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MIN_LENGTH_DEFAULT),
        ({'min_length': 10}, 10),
    ):
        output = parse_min_length(input_data)
        vampytest.assert_eq(output, expected_output)
