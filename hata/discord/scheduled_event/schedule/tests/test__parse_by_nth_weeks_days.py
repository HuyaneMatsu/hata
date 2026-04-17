import vampytest

from ...schedule_nth_weeks_day import ScheduleNthWeeksDay

from ..fields import parse_by_nth_weeks_days


def _iter_options():
    nth_weeks_day_0 = ScheduleNthWeeksDay(nth_week = 1)
    nth_weeks_day_1 = ScheduleNthWeeksDay(nth_week = 2)
    
    yield {}, None
    yield {'by_n_weekday': None}, None
    yield {'by_n_weekday': []}, None
    yield (
        {
            'by_n_weekday': [
                nth_weeks_day_0.to_data(defaults = True),
                nth_weeks_day_1.to_data(defaults = True),
            ],
        },
        (nth_weeks_day_0, nth_weeks_day_1),
    )
    yield (
        {
            'by_n_weekday': [
                nth_weeks_day_1.to_data(defaults = True),
                nth_weeks_day_0.to_data(defaults = True),
            ],
        },
        (nth_weeks_day_0, nth_weeks_day_1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_by_nth_weeks_days(input_data):
    """
    Tests whether ``parse_by_nth_weeks_days`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `Nome | tuple<ScheduleNthWeeksDay>`
    """
    return parse_by_nth_weeks_days(input_data)
