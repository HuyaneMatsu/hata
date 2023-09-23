import vampytest

from ..fields import parse_emoji_pack_collectible


def _iter_options():
    yield {}, False
    yield {'is_emoji_pack_collectible': False}, False
    yield {'is_emoji_pack_collectible': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_emoji_pack_collectible(input_data):
    """
    Tests whether ``parse_emoji_pack_collectible`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_emoji_pack_collectible(input_data)
