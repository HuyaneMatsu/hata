import vampytest

from ...action import AutoModerationAction

from ..fields import validate_actions


def test__validate_action():
    """
    Tests whether ``validate_actions`` works as intended.
    """
    action_1 = AutoModerationAction(duration = 69)
    action_2 = AutoModerationAction(channel_id = 202211170023)
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([action_1, action_2], (action_1, action_2)),
    ):
        output = validate_actions(input_value)
        vampytest.assert_eq(output, expected_output)
