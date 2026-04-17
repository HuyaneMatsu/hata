from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..fields import validate_pinned_at


def _iter_options__passing():
    pinned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield pinned_at, pinned_at


def _iter_options__type_error():
    yield None
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_pinned_at(input_value):
    """
    Tests whether ``validate_pinned_at`` works as intended.
    
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
    output = validate_pinned_at(input_value)
    vampytest.assert_instance(output, DateTime)
    return output
