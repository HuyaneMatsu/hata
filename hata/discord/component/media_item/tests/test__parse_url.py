import vampytest

from ..fields import parse_url


def _iter_options():
    yield {}, ''
    yield {'url': None}, ''
    yield {'url': ''}, ''
    yield {'url': 'https://orindance.party/'}, 'https://orindance.party/'
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_url(input_data):
    """
    Tests whether ``parse_url`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    return parse_url(input_data)
