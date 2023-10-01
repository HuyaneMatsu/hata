from datetime import datetime as DateTime

import vampytest

from ..fields import validate_joined_at


def _iter_options():
    joined_at = DateTime(2016, 5, 14)
    
    yield None, None
    yield joined_at, joined_at


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_joined_at__passing(input_value):
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
    """
    return validate_joined_at(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_joined_at__type_error(input_value):
    """
    Tests whether ``validate_joined_at`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_joined_at(input_value)
