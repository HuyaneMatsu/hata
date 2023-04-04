import vampytest

from ..fields import put_channel_id_into


def test__put_channel_id_into():
    """
    Tests whether ``put_channel_id_into`` works as intended.
    """
    channel_id = 202304030001
    
    for input_value, defaults, expected_output in (
        (0, False, {'channel_id': None}),
        (0, True, {'channel_id': None}),
        (channel_id, False, {'channel_id': str(channel_id)}),
    ):
        data = put_channel_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
