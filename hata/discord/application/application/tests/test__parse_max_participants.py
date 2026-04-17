import vampytest

from ..constants import MAX_PARTICIPANTS_DEFAULT
from ..fields import parse_max_participants


def test__parse_max_participants():
    """
    Tests whether ``parse_max_participants`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MAX_PARTICIPANTS_DEFAULT),
        ({'max_participants': -1}, MAX_PARTICIPANTS_DEFAULT),
        ({'max_participants': 1}, 1),
    ):
        output = parse_max_participants(input_data)
        vampytest.assert_eq(output, expected_output)
