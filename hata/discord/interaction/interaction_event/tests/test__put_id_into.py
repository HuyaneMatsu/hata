import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` is working as intended.
    """
    interaction_event_id = 202302210021
    
    for input_value, defaults, expected_output in (
        (interaction_event_id, False, {'id': str(interaction_event_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
