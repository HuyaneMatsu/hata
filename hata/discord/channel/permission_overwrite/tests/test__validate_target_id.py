import vampytest

from ..fields import validate_target_id


def _iter_options():
    target_id = 202210050004
    
    yield 0, 0
    yield target_id, target_id
    yield str(target_id), target_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_target_id__passing(input_value):
    """
    Tests whether ``validate_target_id`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `TypeError`
    """
    return validate_target_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_target_id__type_error(input_value):
    """
    Tests whether ``validate_target_id`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_target_id(input_value)
