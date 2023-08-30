import vampytest

from ..fields import parse_id


def _iter_options():
    party_id = 'koishi'
    
    yield {}, None
    yield {'id': None}, None
    yield {'id': ''}, None
    yield {'id': party_id}, party_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_id(input_data):
    """
    Tests whether ``parse_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None`, `str`
    """
    return parse_id(input_data)
