
import vampytest

from ..fields import put_nsfw_into


def _iter_options():
    yield False, False, {}
    yield False, True, {'nsfw': False}
    yield True, False, {'nsfw': True}
    yield True, True, {'nsfw': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_nsfw_into(input_value, defaults):
    """
    Tests whether ``put_nsfw_into`` works as intended.
    
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
    return put_nsfw_into(input_value, {}, defaults)
