import vampytest

from ..fields import put_slowmode


def _iter_options():
    yield (
        0,
        False,
        {},
    )
    
    yield (
        0,
        True,
        {'rate_limit_per_user': None},
    )
    
    yield (
        1,
        False,
        {'rate_limit_per_user': 1},
    )
    
    yield (
        1,
        True,
        {'rate_limit_per_user': 1},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_slowmode(input_value, defaults):
    """
    Tests whether ``put_slowmode`` is working as intended.
    
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
    return put_slowmode(input_value, {}, defaults)
