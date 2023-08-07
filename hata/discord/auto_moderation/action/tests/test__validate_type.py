import vampytest

from ..fields import validate_type
from ..preinstanced import AutoModerationActionType


def _iter_options():
    yield None, AutoModerationActionType.none
    yield AutoModerationActionType.timeout, AutoModerationActionType.timeout
    yield AutoModerationActionType.timeout.value, AutoModerationActionType.timeout


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_type__passing(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``AutoModerationActionType``
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, AutoModerationActionType)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with('')
def test__validate_type__type_error(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value where we are expecting `TypeError`.
    
    Raises
    ------
    TypeError
    """
    validate_type(input_value)
