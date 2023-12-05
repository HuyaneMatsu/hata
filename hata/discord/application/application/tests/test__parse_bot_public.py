import vampytest

from ..fields import parse_bot_public


def _iter_options():
    yield {}, False
    yield {'bot_public': False}, False
    yield {'bot_public': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_bot_public(input_data):
    """
    Tests whether ``parse_bot_public`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_bot_public(input_data)
