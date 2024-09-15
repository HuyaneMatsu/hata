import vampytest

from ..constants import SESSION_ID_LENGTH_MIN
from ..fields import put_session_id_into


def _iter_options():
    yield '', False, {'session_id': ''}
    yield '', True, {'session_id': ''}
    yield 'a' * SESSION_ID_LENGTH_MIN, False, {'session_id': 'a' * SESSION_ID_LENGTH_MIN}
    yield 'a' * SESSION_ID_LENGTH_MIN, True, {'session_id': 'a' * SESSION_ID_LENGTH_MIN}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_session_id_into(input_value, defaults):
    """
    Tests whether ``put_session_id_into`` works as intended.
    
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
    return put_session_id_into(input_value, {}, defaults)
