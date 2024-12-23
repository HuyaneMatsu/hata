from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..fields import validate_current_period_start


def _iter_options__passing():
    current_period_start = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield None, None
    yield current_period_start, current_period_start


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_current_period_start(input_value):
    """
    Tests whether ``validate_current_period_start`` works as intended.
    
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
    output = validate_current_period_start(input_value)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output