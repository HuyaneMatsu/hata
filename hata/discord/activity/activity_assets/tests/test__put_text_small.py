import vampytest

from ..fields import put_text_small


def _iter_options():
    yield None, False, {}
    yield None, True, {'small_text': ''}
    yield 'a', False, {'small_text': 'a'}
    yield 'a', True, {'small_text': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_text_small(input_value, defaults):
    """
    Tests whether ``put_text_small`` works as intended.
    
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
    return put_text_small(input_value, {}, defaults)
