import vampytest

from ..fields import put_title


def _iter_options():
    yield '', False, {'label': ''}
    yield '', True, {'label': ''}
    yield 'a', False, {'label': 'a'}
    yield 'a', True, {'label': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_title(input_value, defaults):
    """
    Tests whether ``put_title`` works as intended.
    
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
    return put_title(input_value, {}, defaults)
