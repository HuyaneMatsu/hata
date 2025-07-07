from datetime import datetime as DateTime, timezone as TimeZone

import vampytest    

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..fields import validate_occasion_overwrite


def _iter_options__passing():
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    
    yield occasion_overwrite, occasion_overwrite


def _iter_options__type_error():
    yield None
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_occasion_overwrite(input_value):
    """
    Tests whether ``validate_occasion_overwrite`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : ``ScheduledEventOccasionOverwrite``
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_occasion_overwrite(input_value)
    vampytest.assert_instance(output, ScheduledEventOccasionOverwrite)
    return output
