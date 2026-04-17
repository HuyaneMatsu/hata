from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...scheduled_event_occasion_overwrite import ScheduledEventOccasionOverwrite

from ..fields import parse_occasion_overwrite


def _iter_options():
    occasion_overwrite = ScheduledEventOccasionOverwrite(
        timestamp = DateTime(2016, 5, 14, 13, 0, 0, tzinfo = TimeZone.utc),
    )
    
    yield (
        occasion_overwrite.to_data(defaults = False, include_internals = True),
        occasion_overwrite,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_occasion_overwrite(input_data):
    """
    Tests whether ``parse_occasion_overwrite`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ScheduledEventOccasionOverwrite``
    """
    output = parse_occasion_overwrite(input_data)
    vampytest.assert_instance(output, ScheduledEventOccasionOverwrite)
    return output
