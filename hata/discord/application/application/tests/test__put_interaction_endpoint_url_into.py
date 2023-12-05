import vampytest

from ..fields import put_interaction_endpoint_url_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'interactions_endpoint_url': None}
    yield 'https://orindance.party/', False, {'interactions_endpoint_url': 'https://orindance.party/'}
    yield 'https://orindance.party/', True, {'interactions_endpoint_url': 'https://orindance.party/'}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_interaction_endpoint_url_into(input_value, defaults):
    """
    Tests whether ``put_interaction_endpoint_url_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialize.
    defaults : `bool`
        Whether fields with their value should be included as well.
    
    Returns
    -------
    output_data : `dict<str, object>`
    """
    return put_interaction_endpoint_url_into(input_value, {}, defaults)
