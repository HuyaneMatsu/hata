import vampytest

from ..fields import put_chunk_index_into


def _iter_options():
    yield 0, False, {'chunk_index': 0}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_chunk_index_into(chunk_index, defaults):
    """
    Tests whether ``put_chunk_index_into`` works as intended.
    
    Parameters
    ----------
    chunk_index : `int`
        The chunk index to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_chunk_index_into(chunk_index, {}, defaults)
