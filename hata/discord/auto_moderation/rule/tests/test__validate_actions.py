import vampytest

from ...action import AutoModerationAction

from ..fields import validate_actions


def _iter_options():
    action_0 = AutoModerationAction(duration = 69)
    action_1 = AutoModerationAction(channel_id = 202211170023)
    
    yield (None, None)
    yield ([], None)
    yield ([action_0, action_1], (action_0, action_1))
    


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_action__passing(input_value):
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
    """
    return validate_actions(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with([12.6])
def test__validate_action__type_error(input_value):
    """
    Tests whether ``validate_actions`` works as intended.
    
    Case: type error.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_actions(input_value)
