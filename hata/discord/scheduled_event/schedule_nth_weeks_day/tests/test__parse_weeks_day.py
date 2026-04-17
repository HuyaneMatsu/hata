import vampytest

from ..fields import parse_weeks_day
from ..preinstanced import ScheduleWeeksDay


def _iter_options():
    yield {}, ScheduleWeeksDay.monday
    yield {'day': ScheduleWeeksDay.monday.value}, ScheduleWeeksDay.monday
    yield {'day': ScheduleWeeksDay.tuesday.value}, ScheduleWeeksDay.tuesday


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_weeks_day(input_data):
    """
    Tests whether ``parse_weeks_day`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ScheduleWeeksDay``
    """
    output = parse_weeks_day(input_data)
    vampytest.assert_instance(output, ScheduleWeeksDay)
    return output
