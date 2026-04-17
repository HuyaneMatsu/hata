import vampytest

from ..fields import put_reason


def _iter_options():
    yield None, False, {}
    yield None, True, {'reason': ''}
    yield 'a', False, {'reason': 'a'}
    yield 'a', True, {'reason': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_reason(input_value, defaults):
    """
    Tests whether ``put_reason`` works as intended.
    
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
    return put_reason(input_value, {}, defaults)
