import vampytest

from ..fields import put_system_channel_id


def test__put_system_channel_id():
    """
    Tests whether ``put_system_channel_id`` works as intended.
    """
    system_channel_id = 202306150001
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'system_channel_id': None}),
        (system_channel_id, False, {'system_channel_id': str(system_channel_id)}),
    ):
        data = put_system_channel_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
