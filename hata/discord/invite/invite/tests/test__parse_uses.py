import vampytest

from ..fields import parse_uses


def _iter_options():
    yield {}, None
    yield {'uses': None}, None
    yield {'uses': 0}, 0
    yield {'uses': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_uses(input_data):
    """
    Tests whether ``parse_uses`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse from.
    
    Returns
    -------
    output : `None | int`
    """
    return parse_uses(input_data)
