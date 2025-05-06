import vampytest

from ..fields import put_message_id


def test__put_message_id():
    """
    Tests whether ``put_message_id`` works as intended.
    """
    message_id = 202304270001
    
    for input_value, defaults, expected_output in (
        (0, False, {'message_id': None}),
        (message_id, False, {'message_id': str(message_id)}),
    ):
        data = put_message_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
