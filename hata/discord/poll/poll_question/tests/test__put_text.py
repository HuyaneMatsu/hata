import vampytest

from ..fields import put_text


def _iter_options():
    yield None, False, {'text': ''}
    yield None, True, {'text': ''}
    yield 'a', False, {'text': 'a'}
    yield 'a', True, {'text': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_text(input_value, defaults):
    """
    Tests whether ``put_text`` works as intended.
    
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
    return put_text(input_value, {}, defaults)
