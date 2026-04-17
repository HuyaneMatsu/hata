import vampytest

from ...action import AutoModerationAction

from ..fields import parse_action


def test__parse_action():
    """
    Tests whether ``parse_action`` works as intended.
    """
    action = AutoModerationAction(duration = 69)
    
    for input_data, expected_output in (
        ({}, AutoModerationAction()),
        ({'action': action.to_data(defaults = True)}, action)
    ):
        output = parse_action(input_data)
        vampytest.assert_eq(output, expected_output)
