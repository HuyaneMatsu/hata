import vampytest

from ..fields import parse_spoiler


def _iter_options():
    yield {}, False
    yield {'spoiler': None}, False
    yield {'spoiler': False}, False
    yield {'spoiler': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_spoiler(input_data):
    """
    Tests whether ``parse_spoiler`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_spoiler(input_data)
