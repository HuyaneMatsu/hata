import vampytest

from ..fields import put_name


def _iter_options():
    yield '', False, {'name': ''}
    yield '', True, {'name': ''}
    yield 'a', False, {'name': 'a'}
    yield 'a', True, {'name': 'a'}


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
