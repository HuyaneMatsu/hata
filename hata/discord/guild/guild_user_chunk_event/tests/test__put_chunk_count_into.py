import vampytest

from ..fields import put_chunk_count_into


def _iter_options():
    yield 0, False, {'chunk_count': 0}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_chunk_count_into(chunk_count, defaults):
    """
    Tests whether ``put_chunk_count_into`` works as intended.
    
    Parameters
    ----------
    chunk_count : `int`
        The chunk count to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_chunk_count_into(chunk_count, {}, defaults)
