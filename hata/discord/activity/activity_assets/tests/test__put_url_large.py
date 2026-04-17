import vampytest

from ..fields import put_url_large


def _iter_options():
    yield None, False, {}
    yield None, True, {'large_url': ''}
    yield 'a', False, {'large_url': 'a'}
    yield 'a', True, {'large_url': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_url_large(input_value, defaults):
    """
    Tests whether ``put_url_large`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialize.
    
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_url_large(input_value, {}, defaults)
