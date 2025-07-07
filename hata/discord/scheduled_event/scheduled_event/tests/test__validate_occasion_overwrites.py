from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..fields import validate_occasion_overwrites


def _iter_options__passing():
    occasion_overwrite_0 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    occasion_overwrite_1 = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 15, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    
    yield None, None
    yield [], None
    yield [occasion_overwrite_0, occasion_overwrite_1], (occasion_overwrite_0, occasion_overwrite_1)
    yield [occasion_overwrite_1, occasion_overwrite_0], (occasion_overwrite_0, occasion_overwrite_1)


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_occasion_overwrites(input_value):
    """
    Tests whether ``validate_occasion_overwrites`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<ScheduledEventOccasionOverwrite>``
    
    Raising
    -------
    TypeError
    """
    output = validate_occasion_overwrites(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ScheduledEventOccasionOverwrite)
    
    return output
