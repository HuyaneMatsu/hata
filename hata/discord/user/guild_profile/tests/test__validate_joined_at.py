from datetime import datetime as DateTime

import vampytest

from ..fields import validate_joined_at


def _iter_options__passing():
    joined_at = DateTime(2016, 5, 14)
    
    yield None, None
    yield joined_at, joined_at


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_joined_at(input_value):
    """
    Tests whether ``validate_joined_at`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | DateTime`
    
    Raises
    ------
    TypeError
    """
    return validate_joined_at(input_value)
