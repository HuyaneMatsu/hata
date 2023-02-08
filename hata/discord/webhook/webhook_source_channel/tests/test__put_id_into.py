import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    channel_id = 202301310001
    
    for input_value, defaults, expected_output in (
        (0, False, {'id': None}),
        (0, True, {'id': None}),
        (channel_id, False, {'id': str(channel_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
