import vampytest

from ..fields import put_title_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'title': ''}
    yield 'a', False, {'title': 'a'}
    yield 'a', True, {'title': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_title_into(input_value, defaults):
    """
    Tests whether ``put_title_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None`, `str`
        Value to put into data.
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_title_into(input_value, {}, defaults)
