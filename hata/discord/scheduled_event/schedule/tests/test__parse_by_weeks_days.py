import vampytest

from ...schedule_nth_weeks_day import ScheduleWeeksDay

from ..fields import parse_by_weeks_days


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'by_weekday': None,
        },
        None,
    )
    
    yield (
        {
            'by_weekday': [],
        },
        None,
    )
    
    yield (
        {
            'by_weekday': [
                ScheduleWeeksDay.monday.value,
                ScheduleWeeksDay.wednesday.value,
            ],
        },
        (
            ScheduleWeeksDay.monday,
            ScheduleWeeksDay.wednesday,
        ),
    )
    
    yield (
        {
            'by_weekday': [
                ScheduleWeeksDay.wednesday.value,
                ScheduleWeeksDay.monday.value,
            ],
        },
        (
            ScheduleWeeksDay.monday,
            ScheduleWeeksDay.wednesday,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_by_weeks_days(input_data):
    """
    Tests whether ``parse_by_weeks_days`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<ScheduleWeeksDay>`
    """
    return parse_by_weeks_days(input_data)
