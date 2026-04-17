import vampytest

from ..fields import put_by_months
from ..preinstanced import ScheduleMonth


def _iter_options():
    yield (None, False, {})
    yield (None, True, {'by_month': []})
    
    yield (
        (
            ScheduleMonth.january,
            ScheduleMonth.august,
        ),
        False,
        {
            'by_month': [
                ScheduleMonth.january.value,
                ScheduleMonth.august.value,
            ],
        },
    )
    
    yield (
        (
            ScheduleMonth.january,
            ScheduleMonth.august,
        ),
        True,
        {
            'by_month': [
                ScheduleMonth.january.value,
                ScheduleMonth.august.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_by_months(input_value, defaults):
    """
    Tests whether ``put_by_months`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<ScheduleMonth>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_by_months(input_value, {}, defaults)
