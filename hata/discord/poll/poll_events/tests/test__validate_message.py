import vampytest

from ....message import Message

from ..fields import validate_message


def _iter_options__passing():
    message = Message.precreate(202404020009)
    
    yield message, message


def _iter_options__type_error():
    yield None
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_message(input_value):
    """
    Tests whether ``validate_message`` works as intended.
    
    Parameters
    ----------
    input_value : ``Message``
        Value to validate.
    
    Returns
    -------
    output : ``Message``
    
    Raises
    ------
    TypeError
    """
    return validate_message(input_value)
