import vampytest

from ..fields import put_boost_cost


def _iter_options():
    yield (
        0,
        False,
        {
            'boost_price': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'boost_price': 0,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_boost_cost(input_value, defaults):
    """
    Tests whether ``put_boost_cost`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_boost_cost(input_value, {}, defaults)
