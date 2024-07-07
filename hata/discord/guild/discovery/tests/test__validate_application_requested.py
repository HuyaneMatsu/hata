from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..fields import validate_application_requested


def _iter_options__passing():
    timestamp = DateTime(2016, 9, 9, tzinfo = TimeZone.utc)
    
    yield None, None
    yield timestamp, timestamp


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_application_requested(input_value):
    """
    Tests whether ``validate_application_requested`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | DateTime`
    
    Raising
    -------
    TypeError
    """
    output = validate_application_requested(input_value)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
