import vampytest

from ..constants import SESSION_ID_LENGTH_MAX, SESSION_ID_LENGTH_MIN 
from ..fields import validate_session_id


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'a' * SESSION_ID_LENGTH_MIN, 'a' * SESSION_ID_LENGTH_MIN


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (SESSION_ID_LENGTH_MIN - 1)
    yield 'a' * (SESSION_ID_LENGTH_MAX - 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_session_id(input_value):
    """
    Tests whether `validate_session_id` works as intended.
    
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
    output = validate_session_id(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
