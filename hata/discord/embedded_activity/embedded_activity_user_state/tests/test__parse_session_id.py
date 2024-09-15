import vampytest

from ..constants import SESSION_ID_LENGTH_MIN
from ..fields import parse_session_id


def _iter_options():
    yield {}, ''
    yield {'session_id': None}, ''
    yield {'session_id': ''}, ''
    yield {'session_id': 'a' * SESSION_ID_LENGTH_MIN}, 'a' * SESSION_ID_LENGTH_MIN


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_session_id(input_data):
    """
    Tests whether ``parse_session_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    return parse_session_id(input_data)
