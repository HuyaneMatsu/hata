import vampytest

from ..fields import put_count


def _iter_options():
    yield 0, False, {'count': 0}
    yield 0, True, {'count': 0}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_count(count, defaults):
    """
    Tests whether ``put_count`` works as intended.
    
    Parameters
    ----------
    count : `int`
        The count to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_count(count, {}, defaults)
