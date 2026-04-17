import vampytest

from ..fields import put_count


def _iter_options():
    yield (
        0,
        False,
        {
            'count': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'count': 0,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_count(input_value, defaults):
    """
    Tests whether ``put_count`` works as intended.
    
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
    return put_count(input_value, {}, defaults)
