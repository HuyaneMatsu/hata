import vampytest

from ..fields import validate_title


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'a', 'a'
    yield 'aa', 'aa'


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_title(input_value):
    """
    Tests whether `validate_title` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | str`
    
    Raises
    ------
    TypeError
    """
    return validate_title(input_value)
