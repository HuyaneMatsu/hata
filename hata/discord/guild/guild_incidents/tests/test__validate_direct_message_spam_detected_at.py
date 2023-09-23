from datetime import datetime as DateTime

import vampytest

from ..fields import validate_direct_message_spam_detected_at


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield None, None
    yield until, until


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_direct_message_spam_detected_at__passing(input_value):
    """
    Tests whether ``validate_direct_message_spam_detected_at`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | DateTime`
    """
    return validate_direct_message_spam_detected_at(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_direct_message_spam_detected_at__type_error(input_value):
    """
    Tests whether ``validate_direct_message_spam_detected_at`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_direct_message_spam_detected_at(input_value)
