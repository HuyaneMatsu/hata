import vampytest

from ..fields import parse_redirect_urls


def _iter_options():
    yield {}, None
    yield {'redirect_uris': None}, None
    yield {'redirect_uris': []}, None
    yield {'redirect_uris': [None]}, None
    yield {'redirect_uris': ['a']}, ('a', )
    yield {'redirect_uris': ['a', None]}, ('a', )
    yield {'redirect_uris': ['b', 'a']}, ('a', 'b')


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_redirect_urls(input_data):
    """
    Tests whether ``parse_redirect_urls`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    return parse_redirect_urls(input_data)
