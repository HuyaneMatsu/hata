import vampytest

from ..fields import put_size


def _iter_options():
    yield (
        0,
        False,
        {
            'size': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'size': 0,
        },
    )
    
    yield (
        1,
        False,
        {
            'size': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'size': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_size(input_value, defaults):
    """
    Tests whether ``put_size`` is working as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_size(input_value, {}, defaults)
