import vampytest

from ...schedule_nth_weeks_day import ScheduleNthWeeksDay

from ..fields import put_by_nth_weeks_days


def _iter_options():
    nth_weeks_day_0 = ScheduleNthWeeksDay(nth_week = 1)
    nth_weeks_day_1 = ScheduleNthWeeksDay(nth_week = 2)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'by_n_weekday': [],
        },
    )
    
    yield (
        (nth_weeks_day_0, nth_weeks_day_1),
        False,
        {
            'by_n_weekday': [
                nth_weeks_day_0.to_data(defaults = False),
                nth_weeks_day_1.to_data(defaults = False),
            ],
        },
    )
    
    yield (
        (nth_weeks_day_0, nth_weeks_day_1),
        True,
        {
            'by_n_weekday': [
                nth_weeks_day_0.to_data(defaults = True),
                nth_weeks_day_1.to_data(defaults = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_by_nth_weeks_days(input_value, defaults):
    """
    Tests whether ``put_by_nth_weeks_days`` works as intended.
    
    Parameters
    ----------
    input_value : `Nome | tuple<ScheduleNthWeeksDay>`
        The value to serialize parse from.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_by_nth_weeks_days(input_value, {}, defaults)
