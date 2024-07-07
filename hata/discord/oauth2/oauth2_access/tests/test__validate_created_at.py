from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..fields import validate_created_at


def _iter_options__passing():
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield created_at, created_at


def _iter_options__type_error():
    yield 12.6
    yield None


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_created_at(input_value):
    """
    Tests whether ``validate_created_at`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `DateTime`
    
    Raises
    ------
    TypeError
    """
    return validate_created_at(input_value)
