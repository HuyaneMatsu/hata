from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...activity_timestamps import ActivityTimestamps

from ..fields import validate_timestamps


def _iter_options__passing():
    timestamps = ActivityTimestamps(start = DateTime(2016, 3, 16, tzinfo = TimeZone.utc))
    
    yield None, None
    yield timestamps, timestamps


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_timestamps(input_value):
    """
    Tests whether ``validate_timestamps`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | ActivityTimestamps`
    
    Raising
    -------
    TypeError
    """
    output = validate_timestamps(input_value)
    vampytest.assert_instance(output, ActivityTimestamps, nullable = True)
    return output
