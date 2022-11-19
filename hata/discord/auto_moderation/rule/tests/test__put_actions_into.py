import vampytest

from ...action import AutoModerationAction

from ..fields import put_actions_into


def test__parse_action():
    """
    Tests whether ``put_actions_into`` works as intended.
    """
    action_1 = AutoModerationAction(duration = 69)
    action_2 = AutoModerationAction(channel_id = 202211170022)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'actions': []}),
        ((action_1, action_2), True, {'actions': [action_1.to_data(defaults = True), action_2.to_data(defaults = True)]}),
    ):
        output = put_actions_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
