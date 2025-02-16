import vampytest

from ..fields import put_syncing


def test__put_syncing():
    """
    Tests whether ``put_syncing`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'syncing': False}),
        (True, False, {'syncing': True}),
    ):
        data = put_syncing(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
