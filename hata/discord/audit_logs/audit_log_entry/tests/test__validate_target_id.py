import vampytest
from ..fields import validate_target_id


def _iter_options__passing():
    target_id = 202310200002
    
    yield 0, 0
    yield target_id, target_id
    yield str(target_id), target_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_target_id__passing(input_value):
    """
    Tests whether `validate_target_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `target_id` of.
    
    Returns
    -------
    output : `int`
    """
    return validate_target_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_target_id__type_error(input_value):
    """
    Tests whether `validate_target_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `target_id` of.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_target_id(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('-1')
@vampytest.call_with('1111111111111111111111')
@vampytest.call_with(-1)
@vampytest.call_with(1111111111111111111111)
def test__validate_target_id__value_error(input_value):
    """
    Tests whether `validate_target_id` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `target_id` of.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_target_id(input_value)
