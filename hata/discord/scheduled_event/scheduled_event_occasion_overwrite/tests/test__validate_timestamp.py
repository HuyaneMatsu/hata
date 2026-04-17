from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..fields import validate_timestamp


def _iter_options__passing():
    timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc)
    
    yield timestamp, timestamp


def _iter_options__type_error():
    yield None
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_timestamp(input_value):
    """
    Tests whether `validate_timestamp` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `DateTime`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_timestamp(input_value)
    vampytest.assert_instance(output, DateTime)
    return output
