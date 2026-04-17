import vampytest

from ..fields import put_by_year_days


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
            'by_year_day': [],
        },
    )
    
    yield (
        (
            1,
            2,
        ),
        False,
        {
            'by_year_day': [
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
            'by_year_day': [
                1,
                2,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_by_year_days(input_value, defaults):
    """
    Tests whether ``put_by_year_days`` is working as intended.
    
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
    return put_by_year_days(input_value, {}, defaults)
