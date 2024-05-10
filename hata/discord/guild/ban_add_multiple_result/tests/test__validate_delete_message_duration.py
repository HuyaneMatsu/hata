import vampytest

from ..constants import DELETE_MESSAGE_DURATION_DEFAULT, DELETE_MESSAGE_DURATION_MAX, DELETE_MESSAGE_DURATION_MIN
from ..fields import validate_delete_message_duration


def _iter_options__passing():
    yield None, DELETE_MESSAGE_DURATION_DEFAULT
    yield DELETE_MESSAGE_DURATION_DEFAULT, DELETE_MESSAGE_DURATION_DEFAULT
    yield 60, 60


def _iter_options__value_error():
    yield DELETE_MESSAGE_DURATION_MIN - 1
    yield DELETE_MESSAGE_DURATION_MAX + 1


def _iter_options__type_error():
    yield 'hello mister'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_delete_message_duration(input_value):
    """
    Tests whether `validate_delete_message_duration` works as intended.
    
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
    return validate_delete_message_duration(input_value)
