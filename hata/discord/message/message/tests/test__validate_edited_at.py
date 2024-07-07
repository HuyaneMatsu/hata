from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..fields import validate_edited_at


def _iter_options__passing():
    edited_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, None
    yield edited_at, edited_at


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_edited_at(input_value):
    """
    Tests whether ``validate_edited_at`` works as intended.
    
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
    return validate_edited_at(input_value)
