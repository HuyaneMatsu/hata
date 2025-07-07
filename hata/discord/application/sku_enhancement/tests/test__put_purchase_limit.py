import vampytest

from ..fields import put_purchase_limit


def _iter_options():
    yield (
        0,
        False,
        {
            'purchase_limit': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'purchase_limit': 0,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_purchase_limit(input_value, defaults):
    """
    Tests whether ``put_purchase_limit`` works as intended.
    
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
    return put_purchase_limit(input_value, {}, defaults)
