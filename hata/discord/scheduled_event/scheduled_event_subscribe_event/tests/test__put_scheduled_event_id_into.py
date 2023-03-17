import vampytest

from ..fields import put_scheduled_event_id_into


def test__put_scheduled_event_id_into():
    """
    Tests whether ``put_scheduled_event_id_into`` is working as intended.
    """
    scheduled_event_id = 202303110065
    
    for input_value, defaults, expected_output in (
        (scheduled_event_id, False, {'guild_scheduled_event_id': str(scheduled_event_id)}),
    ):
        data = put_scheduled_event_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
