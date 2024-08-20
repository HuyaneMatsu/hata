import vampytest

from ..fields import parse_by_year_days


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'by_year_day': None
        },
        None,
    )
    
    yield (
        {
            'by_year_day': []
        },
        None,
    )
    
    yield (
        {
            'by_year_day': [
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
            'by_year_day': [
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
def test__parse_by_year_days(input_data):
    """
    Tests whether ``parse_by_year_days`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    return parse_by_year_days(input_data)
