import vampytest

from ..helpers import _strip_emoji_name


@vampytest._(vampytest.call_with('koishi').returning('koishi'))
@vampytest._(vampytest.call_with(':koishi').returning('koishi'))
@vampytest._(vampytest.call_with('koishi:').returning('koishi'))
@vampytest._(vampytest.call_with(':koishi:').returning('koishi'))
def test__strip_emoji_name(value):
    """
    Tests whether ``_strip_emoji_name`` works as intended.
    
    Parameters
    ----------
    value : `str`
        The value to strip.
    
    Returns
    -------
    output : `str`
    """
    return _strip_emoji_name(value)
