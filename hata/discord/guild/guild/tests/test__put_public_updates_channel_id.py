import vampytest

from ..fields import put_public_updates_channel_id


def test__put_public_updates_channel_id():
    """
    Tests whether ``put_public_updates_channel_id`` works as intended.
    """
    public_updates_channel_id = 202306100004
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'public_updates_channel_id': None}),
        (public_updates_channel_id, False, {'public_updates_channel_id': str(public_updates_channel_id)}),
    ):
        data = put_public_updates_channel_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
