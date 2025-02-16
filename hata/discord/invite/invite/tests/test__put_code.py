import vampytest

from ..fields import put_code


def _iter_options():
    yield '', False, {'code': ''}
    yield '', True, {'code': ''}
    yield 'a', False, {'code': 'a'}
    yield 'a', True, {'code': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_code(input_value, defaults):
    """
    Tests whether ``put_code`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_code(input_value, {}, defaults)
