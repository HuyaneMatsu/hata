import vampytest

from ..fields import put_friend_sync


def test__put_friend_sync():
    """
    Tests whether ``put_friend_sync`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'friend_sync': False}),
        (True, False, {'friend_sync': True}),
    ):
        data = put_friend_sync(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
