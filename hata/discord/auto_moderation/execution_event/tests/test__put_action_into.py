import vampytest

from ...action import AutoModerationAction

from ..fields import put_action_into


def test__put_action_into():
    """
    Tests whether ``put_action_into`` works as intended.
    """
    action = AutoModerationAction(duration = 69)
    
    for input_value, expected_output in (
        (action, {'action': action.to_data(defaults = True)}),
    ):
        data = put_action_into(input_value, {}, True)
        vampytest.assert_eq(data, expected_output)
