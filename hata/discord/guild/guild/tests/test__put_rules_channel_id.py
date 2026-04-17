import vampytest

from ..fields import put_rules_channel_id


def test__put_rules_channel_id():
    """
    Tests whether ``put_rules_channel_id`` works as intended.
    """
    rules_channel_id = 202306100010
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'rules_channel_id': None}),
        (rules_channel_id, False, {'rules_channel_id': str(rules_channel_id)}),
    ):
        data = put_rules_channel_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
