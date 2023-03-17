import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    scheduled_event_id = 202303150004
    
    for input_value, defaults, expected_output in (
        (scheduled_event_id, False, {'id': str(scheduled_event_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
