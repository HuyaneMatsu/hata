import vampytest

from ..fields import parse_available


def _iter_options():
    yield {}, True
    yield {'available': False}, False
    yield {'available': True}, True
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_available(input_data):
    """
    Tests whether ``parse_available`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to work with.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_available(input_data)
    vampytest.assert_instance(output, bool)
    return output
