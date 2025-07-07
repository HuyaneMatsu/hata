import vampytest

from ..fields import put_value


def _iter_options():
    yield (
        0,
        False,
        {
            'id': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'id': 0,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_value(value, defaults):
    """
    Tests whether ``put_value`` works as intended.
    
    Parameters
    ----------
    value : `int`
        Input value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_value(value, {}, defaults)
