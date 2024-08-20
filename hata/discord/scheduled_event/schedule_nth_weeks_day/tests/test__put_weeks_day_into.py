import vampytest

from ..fields import put_weeks_day_into
from ..preinstanced import ScheduleWeeksDay


def _iter_options():
    yield ScheduleWeeksDay.monday, False, {'day': ScheduleWeeksDay.monday.value}
    yield ScheduleWeeksDay.monday, True, {'day': ScheduleWeeksDay.monday.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_weeks_day_into(input_value, defaults):
    """
    Tests whether ``put_weeks_day_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ScheduleWeeksDay``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_weeks_day_into(input_value, {}, defaults)
