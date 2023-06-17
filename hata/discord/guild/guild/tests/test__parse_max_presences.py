import vampytest

from ..constants import MAX_PRESENCES_DEFAULT
from ..fields import parse_max_presences


def test__parse_max_presences():
    """
    Tests whether ``parse_max_presences`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MAX_PRESENCES_DEFAULT),
        ({'max_presences': 1}, 1),
    ):
        output = parse_max_presences(input_data)
        vampytest.assert_eq(output, expected_output)
