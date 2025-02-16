import vampytest

from ...schedule_nth_weeks_day import ScheduleWeeksDay

from ..fields import put_by_weeks_days


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'by_weekday': [],
        },
    )
    
    yield (
        (
            ScheduleWeeksDay.monday,
            ScheduleWeeksDay.wednesday,
        ),
        False,
        {
            'by_weekday': [
                ScheduleWeeksDay.monday.value,
                ScheduleWeeksDay.wednesday.value,
            ],
        },
    )
    
    yield (
        (
            ScheduleWeeksDay.monday,
            ScheduleWeeksDay.wednesday,
        ),
        True,
        {
            'by_weekday': [
                ScheduleWeeksDay.monday.value,
                ScheduleWeeksDay.wednesday.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_by_weeks_days(input_value, defaults):
    """
    Tests whether ``put_by_weeks_days`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<ScheduleWeeksDay>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_by_weeks_days(input_value, {}, defaults)
