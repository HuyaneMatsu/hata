import vampytest

from ..fields import parse_by_month_days


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'by_month_day': None
        },
        None,
    )
    
    yield (
        {
            'by_month_day': []
        },
        None,
    )
    
    yield (
        {
            'by_month_day': [
                1,
                2,
            ],
        },
        (
            1,
            2,
        ),
    )
    
    yield (
        {
            'by_month_day': [
                2,
                1,
            ],
        },
        (
            1,
            2,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_by_month_days(input_data):
    """
    Tests whether ``parse_by_month_days`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    return parse_by_month_days(input_data)
