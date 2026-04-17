import vampytest

from ..fields import put_emoji_pack_collectible


def _iter_options():
    yield False, False, {}
    yield False, True, {'is_emoji_pack_collectible': False}
    yield True, False, {'is_emoji_pack_collectible': True}
    yield True, True, {'is_emoji_pack_collectible': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_emoji_pack_collectible(input_value, defaults):
    """
    Tests whether ``put_emoji_pack_collectible`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_emoji_pack_collectible(input_value, {}, defaults)
