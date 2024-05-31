import vampytest

from ..constants import DESCRIPTION_LENGTH_MAX, DESCRIPTION_LENGTH_MIN
from ..fields import validate_description


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'aa', 'aa'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (DESCRIPTION_LENGTH_MAX + 1)
    yield 'a' * (DESCRIPTION_LENGTH_MIN - 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_description(input_value):
    """
    Tests whether `validate_description` works as intended.
    
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
    ValueError
    """
    return validate_description(input_value)
