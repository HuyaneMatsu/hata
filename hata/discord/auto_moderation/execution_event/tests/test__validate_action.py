import vampytest

from ...action import AutoModerationAction

from ..fields import validate_action


def _iter_options__passing():
    action = AutoModerationAction(duration = 69)
    
    yield None, AutoModerationAction()
    yield action, action


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_action(input_value):
    """
    Tests whether ``validate_action`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``AutoModerationAction``
    
    Raises
    ------
    TypeError
    """
    output = validate_action(input_value)
    vampytest.assert_instance(output, AutoModerationAction)
    return output
