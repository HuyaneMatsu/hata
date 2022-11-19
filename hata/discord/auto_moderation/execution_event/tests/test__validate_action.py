import vampytest

from ...action import AutoModerationAction

from ..fields import validate_action


def test__validate_action__0():
    """
    Tests whether ``validate_action`` works as intended.
    
    Case: Passing.
    """
    action = AutoModerationAction(duration = 69)
    
    for input_value, expected_output in (
        (None, AutoModerationAction()),
        (action, action),
    ):
        output = validate_action(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_action__1():
    """
    Tests whether ``validate_action`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_action(input_value)
