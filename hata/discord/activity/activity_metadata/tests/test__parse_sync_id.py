import vampytest

from ..fields import parse_sync_id


def _iter_options():
    yield {}, None
    yield {'sync_id': None}, None
    yield {'sync_id': ''}, None
    yield {'sync_id': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sync_id(input_data):
    """
    Tests whether ``parse_sync_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    return parse_sync_id(input_data)
