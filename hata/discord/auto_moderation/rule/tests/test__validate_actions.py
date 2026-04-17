import vampytest

from ...action import AutoModerationAction

from ..fields import validate_actions


def _iter_options__passing():
    action_0 = AutoModerationAction(duration = 69)
    action_1 = AutoModerationAction(channel_id = 202211170023)
    
    yield (None, None)
    yield ([], None)
    yield ([action_0, action_1], (action_0, action_1))


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_action(input_value):
    """
    Tests whether ``validate_actions`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<AutoModerationAction>`
    
    Raises
    ------
    TypeError
    """
    return validate_actions(input_value)
