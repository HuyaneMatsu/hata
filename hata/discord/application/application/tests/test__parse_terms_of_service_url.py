import vampytest

from ..fields import parse_terms_of_service_url


def _iter_options():
    yield {}, None
    yield {'terms_of_service_url': None}, None
    yield {'terms_of_service_url': ''}, None
    yield {'terms_of_service_url': 'https://orindance.party/'}, 'https://orindance.party/'
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_terms_of_service_url(input_data):
    """
    Tests whether ``parse_terms_of_service_url`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_terms_of_service_url(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
