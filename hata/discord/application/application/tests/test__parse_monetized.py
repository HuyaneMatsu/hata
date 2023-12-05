import vampytest

from ..fields import parse_monetized


def _iter_options():
    yield {}, False
    yield {'is_monetized': False}, False
    yield {'is_monetized': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_monetized(input_data):
    """
    Tests whether ``parse_monetized`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_monetized(input_data)
