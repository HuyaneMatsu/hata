import vampytest

from ..fields import put_syncing_into


def test__put_syncing_into():
    """
    Tests whether ``put_syncing_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'syncing': False}),
        (True, False, {'syncing': True}),
    ):
        data = put_syncing_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
