import vampytest

from ..constants import MIN_VALUES_DEFAULT
from ..fields import parse_min_values


def test__parse_min_values():
    """
    Tests whether ``parse_min_values`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MIN_VALUES_DEFAULT),
        ({'min_values': 10}, 10),
    ):
        output = parse_min_values(input_data)
        vampytest.assert_eq(output, expected_output)
