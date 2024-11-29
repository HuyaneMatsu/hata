from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ..event import _validate_deprecation
from ..event_deprecation import EventDeprecation


def _iter_options__passing():
    yield None, None
    yield (
        EventDeprecation(
            'koishi',
            DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
            trigger_after = DateTime.now(tz = TimeZone.utc) + TimeDelta(days = 5000),
        ),
        None,
    )
    
    yield (
        EventDeprecation(
            'orin',
            DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        ),
        EventDeprecation(
            'orin',
            DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        )
    )


def _iter_options__type_error():
    yield object()


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_deprecation(input_value):
    """
    Tests whether ``_validate_deprecation`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test with.
    
    Returns
    -------
    output : `None | EventDeprecation`
    
    Raises
    ------
    TypeError
    """
    output = _validate_deprecation(input_value)
    vampytest.assert_instance(output, EventDeprecation, nullable = True)
    return output
