import vampytest

from ..fields import parse_chunk_index


def _iter_options():
    yield {}, 0
    yield {'chunk_index': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_chunk_index(input_data):
    """
    Tests whether ``parse_chunk_index`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the chunk index from.
    
    Returns
    -------
    output : `int`
    """
    return parse_chunk_index(input_data)
