import vampytest

from ..fields import parse_id


def _iter_options():
    sku_id = 'koishi'
    
    yield {}, ''
    yield {'id': None}, ''
    yield {'id': ''}, ''
    yield {'id': sku_id}, sku_id


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
    output : `str`
    """
    return parse_id(input_data)
