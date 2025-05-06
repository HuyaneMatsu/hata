import vampytest

from ..fields import put_width


def _iter_options():
    yield (
        0,
        False,
        {'width': 0},
    )
    
    yield (
        0,
        True,
        {'width': 0},
    )
    
    yield (
        1,
        False,
        {'width': 1},
    )
    
    yield (
        1,
        True,
        {'width': 1},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_width(input_value, defaults):
    """
    Tests whether ``put_width`` is working as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    
    defaults : `bool`
        Whether fields with their default should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_width(input_value, {}, defaults)
