import vampytest

from ..fields import put_state_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'state': ''}
    yield 'a', False, {'state': 'a'}
    yield 'a', True, {'state': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_state_into(input_value, defaults):
    """
    Tests whether ``put_state_into`` works as intended.
    
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
    return put_state_into(input_value, {}, defaults)
