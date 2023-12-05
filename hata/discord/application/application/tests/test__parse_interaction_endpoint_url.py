import vampytest

from ..fields import parse_interaction_endpoint_url


def _iter_options():
    yield {}, None
    yield {'interactions_endpoint_url': None}, None
    yield {'interactions_endpoint_url': ''}, None
    yield {'interactions_endpoint_url': 'https://orindance.party/'}, 'https://orindance.party/'
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_interaction_endpoint_url(input_data):
    """
    Tests whether ``parse_interaction_endpoint_url`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    return parse_interaction_endpoint_url(input_data)
