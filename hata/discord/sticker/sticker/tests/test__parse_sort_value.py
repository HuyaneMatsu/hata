import vampytest

from ..constants import SORT_VALUE_DEFAULT
from ..fields import parse_sort_value


def test__parse_sort_value():
    """
    Tests whether ``parse_sort_value`` works as intended.
    """
    for input_data, expected_output in (
        ({}, SORT_VALUE_DEFAULT),
        ({'sort_value': 1}, 1),
    ):
        output = parse_sort_value(input_data)
        vampytest.assert_eq(output, expected_output)
