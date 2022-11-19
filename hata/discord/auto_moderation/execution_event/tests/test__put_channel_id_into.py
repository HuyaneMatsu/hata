import vampytest

from ..fields import put_channel_id_into


def test__put_channel_id_into():
    """
    Tests whether ``put_channel_id_into`` is working as intended.
    """
    channel_id = 202211160006
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'channel_id': None}),
        (channel_id, False, {'channel_id': str(channel_id)}),
    ):
        data = put_channel_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
