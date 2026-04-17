import vampytest

from ..fields import put_boost_count


def _iter_options():
    yield (
        0,
        False,
        {},
    )
    
    yield (
        0,
        True,
        {'premium_subscription_count': 0},
    )
    
    yield (
        1,
        False,
        {'premium_subscription_count': 1},
    )
    
    yield (
        1,
        True,
        {'premium_subscription_count': 1},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_boost_count(input_value, defaults):
    """
    Tests whether ``put_boost_count`` is working as intended.
    
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
    return put_boost_count(input_value, {}, defaults)
