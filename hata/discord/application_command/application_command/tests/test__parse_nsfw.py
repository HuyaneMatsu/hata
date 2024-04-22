import vampytest

from ..fields import parse_nsfw


def _iter_options():
    yield {}, False
    yield {'nsfw': None}, False
    yield {'nsfw': False}, False
    yield {'nsfw': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_nsfw(input_data):
    """
    Tests whether ``parse_nsfw`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_nsfw(input_data)
