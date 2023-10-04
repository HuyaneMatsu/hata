import vampytest

from ..fields import parse_consumed


def _iter_options():
    yield {}, False
    yield {'consumed': False}, False
    yield {'consumed': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_consumed(input_data):
    """
    Tests whether ``parse_consumed`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_consumed(input_data)
