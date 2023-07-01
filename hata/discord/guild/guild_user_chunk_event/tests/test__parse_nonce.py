import vampytest

from ..fields import parse_nonce


def _iter_options():
    yield {}, None
    yield {'nonce': None}, None
    yield {'nonce': ''}, None
    yield {'nonce': 'Okuu'}, 'Okuu'
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_nonce(input_data):
    """
    Tests whether ``parse_nonce`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the nonce from.
    
    Returns
    -------
    output : `None | str`
    """
    return parse_nonce(input_data)
