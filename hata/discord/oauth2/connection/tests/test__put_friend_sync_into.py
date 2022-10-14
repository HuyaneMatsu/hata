import vampytest

from ..fields import put_friend_sync_into


def test__put_friend_sync_into():
    """
    Tests whether ``put_friend_sync_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'friend_sync': False}),
        (True, False, {'friend_sync': True}),
    ):
        data = put_friend_sync_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
