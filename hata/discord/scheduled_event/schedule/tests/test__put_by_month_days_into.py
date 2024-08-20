import vampytest

from ..fields import put_by_month_days_into


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
            'by_month_day': [],
        },
    )
    
    yield (
        (
            1,
            2,
        ),
        False,
        {
            'by_month_day': [
                1,
                2,
            ],
        },
    )
    
    yield (
        (
            1,
            2,
        ),
        True,
        {
            'by_month_day': [
                1,
                2,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_by_month_days_into(input_value, defaults):
    """
    Tests whether ``put_by_month_days_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_by_month_days_into(input_value, {}, defaults)
