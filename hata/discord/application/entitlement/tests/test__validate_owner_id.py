import vampytest

from ..fields import validate_owner_id


def _iter_options__passing():
    owner_id = 202310030000
    
    yield 0, 0
    yield owner_id, owner_id
    yield str(owner_id), owner_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_owner_id__passing(input_value):
    """
    Tests whether `validate_owner_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    """
    return validate_owner_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with(None)
def test__validate_owner_id__type_error(input_value):
    """
    Tests whether `validate_owner_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_owner_id(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('-1')
@vampytest.call_with('1111111111111111111111')
@vampytest.call_with(-1)
@vampytest.call_with(1111111111111111111111)
def test__validate_owner_id__value_error(input_value):
    """
    Tests whether `validate_owner_id` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_owner_id(input_value)
