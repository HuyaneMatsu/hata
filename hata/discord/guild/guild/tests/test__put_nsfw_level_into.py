import vampytest

from ..fields import put_nsfw_level_into
from ..preinstanced import NsfwLevel


def _iter_options():
    yield NsfwLevel.none, False, {'nsfw_level': NsfwLevel.none.value}
    yield NsfwLevel.none, True, {'nsfw_level': NsfwLevel.none.value}
    yield NsfwLevel.safe, False, {'nsfw_level': NsfwLevel.safe.value}
    yield NsfwLevel.safe, True, {'nsfw_level': NsfwLevel.safe.value}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_nsfw_level_into(input_value, defaults):
    """
    Tests whether ``put_nsfw_level_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``NsfwLevel``
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_nsfw_level_into(input_value, {}, defaults)
