import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    message_interaction_id = 202304230008
    
    for input_value, defaults, expected_output in (
        (message_interaction_id, False, {'id': str(message_interaction_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
