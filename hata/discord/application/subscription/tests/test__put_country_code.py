import vampytest

from ..fields import put_country_code


def _iter_options():
    yield None, False, {}
    yield None, True, {'country': None}
    yield 'a', False, {'country': 'a'}
    yield 'a', True, {'country': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_country_code(input_value, defaults):
    """
    Tests whether ``put_country_code`` works as intended.
    
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
    return put_country_code(input_value, {}, defaults)
