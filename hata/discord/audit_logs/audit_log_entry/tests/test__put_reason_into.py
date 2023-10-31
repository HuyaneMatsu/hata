import vampytest

from ..fields import put_reason_into


def iter_options():
    yield None, False, {}
    yield None, True, {'reason': ''}
    yield 'a', False, {'reason': 'a'}
    yield 'a', True, {'reason': 'a'}


@vampytest._(vampytest.call_from(iter_options()).returning_last())
def test__put_reason_into(input_value, defaults):
    """
    Tests whether ``put_reason_into`` works as intended.
    
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
    return put_reason_into(input_value, {}, defaults)
