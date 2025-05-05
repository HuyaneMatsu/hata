import vampytest

from ..fields import put_placeholder


def _iter_options():
    yield None, False, {}
    yield None, True, {'placeholder': ''}
    yield 'a', False, {'placeholder': 'a'}
    yield 'a', True, {'placeholder': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_placeholder(input_value, defaults):
    """
    Tests whether ``put_placeholder`` works as intended.
    
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
    return put_placeholder(input_value, {}, defaults)
