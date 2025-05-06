import vampytest

from ..fields import put_attachment_size_limit


def _iter_options():
    yield (
        0,
        False,
        {'attachment_size_limit': 0},
    )
    
    yield (
        0,
        True,
        {'attachment_size_limit': 0},
    )
    
    yield (
        1,
        False,
        {'attachment_size_limit': 1},
    )
    
    yield (
        1,
        True,
        {'attachment_size_limit': 1},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_attachment_size_limit(input_value, defaults):
    """
    Tests whether ``put_attachment_size_limit`` is working as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    
    defaults : `bool`
        Whether values as their default should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_attachment_size_limit(input_value, {}, defaults)
