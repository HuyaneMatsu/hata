import vampytest

from ..fields import put_url


def _iter_options():
    yield None, False, {}
    yield None, True, {'url': None}
    yield 'https://orindance.party/', False, {'url': 'https://orindance.party/'}
    yield 'https://orindance.party/', True, {'url': 'https://orindance.party/'}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_url(input_value, defaults):
    """
    Tests whether ``put_url`` works as intended.
    
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
    return put_url(input_value, {}, defaults)
