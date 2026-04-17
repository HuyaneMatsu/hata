import vampytest

from ..fields import parse_deeplink_url


def _iter_options():
    yield {}, None
    yield {'deeplink_uri': None}, None
    yield {'deeplink_uri': ''}, None
    yield {'deeplink_uri': 'https://orindance.party/'}, 'https://orindance.party/'
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_deeplink_url(input_data):
    """
    Tests whether ``parse_deeplink_url`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_deeplink_url(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
