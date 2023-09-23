from datetime import datetime as DateTime

import vampytest

from ..fields import validate_timed_out_until


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield None, None
    yield until, until


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_timed_out_until__passing(input_value):
    """
    Tests whether ``validate_timed_out_until`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | DateTime`
    """
    return validate_timed_out_until(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_timed_out_until__type_error(input_value):
    """
    Tests whether ``validate_timed_out_until`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_timed_out_until(input_value)
