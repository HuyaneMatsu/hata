import vampytest

from ..constants import MAX_VALUES_DEFAULT
from ..fields import parse_max_values


def test__parse_max_values():
    """
    Tests whether ``parse_max_values`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MAX_VALUES_DEFAULT),
        ({'max_values': 10}, 10),
    ):
        output = parse_max_values(input_data)
        vampytest.assert_eq(output, expected_output)
