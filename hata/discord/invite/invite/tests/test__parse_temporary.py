import vampytest

from ..fields import parse_temporary


def _iter_options():
    yield {}, False
    yield {'temporary': False}, False
    yield {'temporary': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_temporary(input_data):
    """
    Tests whether ``parse_temporary`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_temporary(input_data)
