import vampytest

from ..fields import put_session_id


def _iter_options():
    yield None, False, {}
    yield None, True, {'session_id': ''}
    yield 'a', False, {'session_id': 'a'}
    yield 'a', True, {'session_id': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_session_id(input_value, defaults):
    """
    Tests whether ``put_session_id`` works as intended.
    
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
    return put_session_id(input_value, {}, defaults)
