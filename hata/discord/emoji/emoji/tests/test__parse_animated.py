import vampytest

from ..fields import parse_animated


def _iter_options():
    yield {}, False
    yield {'animated': False}, False
    yield {'animated': True}, True
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_animated(input_data):
    """
    Tests whether ``parse_animated`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to work with.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_animated(input_data)
    vampytest.assert_instance(output, bool)
    return output
