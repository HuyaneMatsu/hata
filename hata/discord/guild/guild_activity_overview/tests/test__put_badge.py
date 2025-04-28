import vampytest

from ..fields import put_badge


def _iter_options():
    yield (
        0,
        False,
        {'badge': 0},
    )
    
    yield (
        0,
        True,
        {'badge': 0},
    )
    
    yield (
        1,
        False,
        {'badge': 1},
    )
    
    yield (
        1,
        True,
        {'badge': 1},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_badge(input_value, defaults):
    """
    Tests whether ``put_badge`` is working as intended.
    
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
    return put_badge(input_value, {}, defaults)
