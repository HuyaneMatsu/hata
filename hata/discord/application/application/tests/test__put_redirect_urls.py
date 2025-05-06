import vampytest

from ..fields import put_redirect_urls


def _iter_options():
    yield None, False, {}
    yield None, True, {'redirect_uris': []}
    yield ('a', ), False, {'redirect_uris': ['a']}
    yield ('a', ), True, {'redirect_uris': ['a']}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_redirect_urls(input_value, defaults):
    """
    Tests whether ``put_redirect_urls`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<str>`
        Value to serialize.
    defaults : `bool`
        Whether fields with the default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_redirect_urls(input_value, {}, defaults)
