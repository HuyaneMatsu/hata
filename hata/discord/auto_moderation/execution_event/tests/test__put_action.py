import vampytest

from ...action import AutoModerationAction

from ..fields import put_action


def test__put_action():
    """
    Tests whether ``put_action`` works as intended.
    """
    action = AutoModerationAction(duration = 69)
    
    for input_value, expected_output in (
        (action, {'action': action.to_data(defaults = True)}),
    ):
        data = put_action(input_value, {}, True)
        vampytest.assert_eq(data, expected_output)
