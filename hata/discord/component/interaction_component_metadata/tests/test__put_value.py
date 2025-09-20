import vampytest

from ..fields import put_value


def _iter_options():
    yield None, False, {}
    yield None, True, {'value': ''}
    yield 'a', False, {'value': 'a'}
    yield 'a', True, {'value': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_value(input_value, defaults):
    """
    Tests whether ``put_value`` works as intended.
    
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
    return put_value(input_value, {}, defaults)
