import vampytest

from ..fields import put_alert_system_message_id


def test__put_alert_system_message_id():
    """
    Tests whether ``put_alert_system_message_id`` is working as intended.
    """
    alert_system_message_id = 202211160005
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'alert_system_message_id': None}),
        (alert_system_message_id, False, {'alert_system_message_id': str(alert_system_message_id)}),
    ):
        data = put_alert_system_message_id(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
