import vampytest

from ..fields import parse_managed


def _iter_options():
    yield {}, False
    yield {'managed': False}, False
    yield {'managed': True}, True
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_managed(input_data):
    """
    Tests whether ``parse_managed`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to work with.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_managed(input_data)
    vampytest.assert_instance(output, bool)
    return output
