import vampytest

from ..fields import put_height


def _iter_options():
    yield (
        0,
        False,
        {'height': 0},
    )
    
    yield (
        0,
        True,
        {'height': 0},
    )
    
    yield (
        1,
        False,
        {'height': 1},
    )
    
    yield (
        1,
        True,
        {'height': 1},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_height(input_value, defaults):
    """
    Tests whether ``put_height`` is working as intended.
    
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
    return put_height(input_value, {}, defaults)
