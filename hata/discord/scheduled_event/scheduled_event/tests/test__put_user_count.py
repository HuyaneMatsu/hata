import vampytest

from ..fields import put_user_count


def _iter_options():
    yield 0, False, {'user_count': 0}
    yield 0, True, {'user_count': 0}
    yield 1, False, {'user_count': 1}
    yield 1, True, {'user_count': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_count(input_value, defaults):
    """
    Tests whether ``put_user_count`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_user_count(input_value, {}, defaults)
