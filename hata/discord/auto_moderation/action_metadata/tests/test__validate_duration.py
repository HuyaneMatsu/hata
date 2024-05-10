import vampytest

from ..fields import validate_duration


def _iter_options__passing():
    yield None, 0
    yield 0, 0
    yield 1, 1
    yield 12.6, 13


def _iter_options__type_error():
    yield 'hello'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_duration(input_value):
    """
    Tests whether `validate_duration` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `float`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_duration(input_value)
