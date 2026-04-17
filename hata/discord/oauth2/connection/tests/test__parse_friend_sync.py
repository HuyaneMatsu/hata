import vampytest

from ..fields import parse_friend_sync


def test__parse_friend_sync():
    """
    Tests whether ``parse_friend_sync`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'friend_sync': False}, False),
        ({'friend_sync': True}, True),
    ):
        output = parse_friend_sync(input_data)
        vampytest.assert_eq(output, expected_output)
