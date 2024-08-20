import vampytest

from ..fields import parse_by_months
from ..preinstanced import ScheduleMonth


def _iter_options():
    yield ({}, None)
    yield ({'by_month': None}, None)
    yield ({'by_month': []}, None)
    
    yield (
        {
            'by_month': [
                ScheduleMonth.january.value,
                ScheduleMonth.august.value,
            ],
        },
        (
            ScheduleMonth.january,
            ScheduleMonth.august,
        ),
    )
    
    yield (
        {
            'by_month': [
                ScheduleMonth.august.value,
                ScheduleMonth.january.value,
            ],
        },
        (
            ScheduleMonth.january,
            ScheduleMonth.august,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_by_months(input_data):
    """
    Tests whether ``parse_by_months`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<ScheduleMonth>`
    """
    return parse_by_months(input_data)
