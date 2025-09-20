import vampytest

from ..fields import put_state_url


def _iter_options():
    yield None, False, {}
    yield None, True, {'state_url': ''}
    yield 'a', False, {'state_url': 'a'}
    yield 'a', True, {'state_url': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_state_url(input_value, defaults):
    """
    Tests whether ``put_state_url`` works as intended.
    
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
    return put_state_url(input_value, {}, defaults)
