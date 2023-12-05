import vampytest

from ..fields import parse_position


def _iter_options():
    yield {}, 0
    yield {'shelf_rank': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_position(input_data):
    """
    Tests whether ``parse_position`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the position from.
    
    Returns
    -------
    output : `int`
    """
    return parse_position(input_data)
