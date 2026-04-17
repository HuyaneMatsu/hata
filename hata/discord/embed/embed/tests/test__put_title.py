import vampytest

from ..fields import put_title


def _iter_options():
    yield None, False, {}
    yield None, True, {'title': ''}
    yield 'a', False, {'title': 'a'}
    yield 'a', True, {'title': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_title(input_value, defaults):
    """
    Tests whether ``put_title`` works as intended.
    
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
    return put_title(input_value, {}, defaults)
