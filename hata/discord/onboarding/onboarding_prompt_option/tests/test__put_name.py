import vampytest

from ..fields import put_name


def _iter_options():
    yield '', False, {'title': ''}
    yield '', True, {'title': ''}
    yield 'a', False, {'title': 'a'}
    yield 'a', True, {'title': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_name(input_value, defaults):
    """
    Tests whether ``put_name`` works as intended.
    
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
    return put_name(input_value, {}, defaults)
