import vampytest

from ..fields import put_vanity_code


def _iter_options():
    yield None, False, {}
    yield None, True, {'vanity_url_code': ''}
    yield 'a', False, {'vanity_url_code': 'a'}
    yield 'a', True, {'vanity_url_code': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_vanity_code(input_value, defaults):
    """
    Tests whether ``put_vanity_code`` works as intended.
    
    Parameters
    ----------
    input_value : `None`, `str`
        Value to serialize.
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_vanity_code(input_value, {}, defaults)
