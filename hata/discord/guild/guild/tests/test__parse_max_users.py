import vampytest

from ..constants import MAX_USERS_DEFAULT
from ..fields import parse_max_users


def test__parse_max_users():
    """
    Tests whether ``parse_max_users`` works as intended.
    """
    for input_data, expected_output in (
        ({}, MAX_USERS_DEFAULT),
        ({'max_members': 1}, 1),
    ):
        output = parse_max_users(input_data)
        vampytest.assert_eq(output, expected_output)
