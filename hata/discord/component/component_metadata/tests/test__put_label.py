import vampytest

from ..fields import put_label


def _iter_options():
    yield None, False, {}
    yield None, True, {'label': ''}
    yield 'a', False, {'label': 'a'}
    yield 'a', True, {'label': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_label(input_value, defaults):
    """
    Tests whether ``put_label`` works as intended.
    
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
    return put_label(input_value, {}, defaults)
