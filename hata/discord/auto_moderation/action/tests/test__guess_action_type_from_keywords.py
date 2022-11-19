import vampytest

from ..helpers import guess_action_type_from_keyword_parameters
from ..preinstanced import AutoModerationActionType


def test__guess_action_type_from_keyword_parameters__passing():
    """
    Tests whether ``guess_action_type_from_keyword_parameters`` works as intended.
    
    Case: passing.
    """
    for input_action_type, keyword_parameters, expected_output in (
        (AutoModerationActionType.timeout, {}, AutoModerationActionType.timeout),
        (AutoModerationActionType.timeout, {'duration': None}, AutoModerationActionType.timeout),
        (AutoModerationActionType.none, {}, AutoModerationActionType.none),
        (AutoModerationActionType.none, {'duration': None}, AutoModerationActionType.timeout),
        (AutoModerationActionType.none, {'channel_id': None}, AutoModerationActionType.send_alert_message),
    ):
        output = guess_action_type_from_keyword_parameters(input_action_type, keyword_parameters)
        vampytest.assert_is(output, expected_output)


def test__guess_action_type_from_keyword_parameters__type_error():
    """
    Tests whether ``guess_action_type_from_keyword_parameters`` works as intended.
    
    Case: `TypeError`.
    """
    for input_action_type, keyword_parameters in (
        (AutoModerationActionType.timeout, {'channel_id': None}),
        (AutoModerationActionType.none, {'duration': None, 'channel_id': None}),
    ):
        with vampytest.assert_raises(TypeError):
            guess_action_type_from_keyword_parameters(input_action_type, keyword_parameters)
