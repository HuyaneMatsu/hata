import vampytest

from ...action import AutoModerationAction

from ..fields import parse_actions


def test__parse_action():
    """
    Tests whether ``parse_actions`` works as intended.
    """
    action_1 = AutoModerationAction(duration = 69)
    action_2 = AutoModerationAction(channel_id = 202211170021)
    
    for input_data, expected_output in (
        ({}, None),
        ({'actions': None}, None),
        ({'actions': []}, None),
        ({'actions': [action_1.to_data(defaults = True), action_2.to_data(defaults = True)]}, (action_1, action_2)),
    ):
        output = parse_actions(input_data)
        vampytest.assert_eq(output, expected_output)
