import vampytest

from ..fields import validate_id


def _iter_options__passing():
    channel_id = 202301310002
    
    yield 0, 0
    yield channel_id, channel_id
    yield str(channel_id), channel_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_id__passing(input_value):
    """
    Tests whether `validate_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    """
    return validate_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_id__type_error(input_value):
    """
    Tests whether `validate_id` works as intended.
    
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
    validate_id(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('-1')
@vampytest.call_with('1111111111111111111111')
@vampytest.call_with(-1)
@vampytest.call_with(1111111111111111111111)
def test__validate_id__value_error(input_value):
    """
    Tests whether `validate_id` works as intended.
    
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
    validate_id(input_value)
