import vampytest

from ..fields import parse_content_type

def _iter_options():
    yield {}, None
    yield {'content_type': None}, None
    yield {'content_type': ''}, None
    yield {'content_type': 'a'}, 'a'
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_content_type(input_data):
    """
    Tests whether ``parse_content_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_content_type(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
