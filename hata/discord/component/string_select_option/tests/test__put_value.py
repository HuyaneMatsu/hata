import vampytest

from ..fields import put_value


def _iter_options():
    yield '', False, {'value': ''}
    yield '', True, {'value': ''}
    yield 'a', False, {'value': 'a'}
    yield 'a', True, {'value': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_value(input_value, defaults):
    """
    Tests whether ``put_value`` works as intended.
    
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
    return put_value(input_value, {}, defaults)
