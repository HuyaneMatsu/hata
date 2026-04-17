import vampytest

from ..fields import parse_premium


def _iter_options():
    yield {}, False
    yield {'premium': False}, False
    yield {'premium': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_premium(input_data):
    """
    Tests whether ``parse_premium`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_premium(input_data)
