import vampytest

from ..fields import validate_sampling_rate


def _iter_options__passing():
    yield 2, 2
    yield 1, 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_sampling_rate__passing(input_value):
    """
    Tests whether `validate_sampling_rate` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    """
    return validate_sampling_rate(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with('12')
def test__validate_sampling_rate__type_error(input_value):
    """
    Tests whether `validate_sampling_rate` works as intended.
    
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
    validate_sampling_rate(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with(-1)
@vampytest.call_with(0)
def test__validate_sampling_rate__value_error(input_value):
    """
    Tests whether `validate_sampling_rate` works as intended.
    
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
    validate_sampling_rate(input_value)
