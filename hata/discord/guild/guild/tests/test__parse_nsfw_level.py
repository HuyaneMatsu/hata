import vampytest

from ..fields import parse_nsfw_level
from ..preinstanced import NsfwLevel


def _iter_options():
    yield {}, NsfwLevel.none
    yield {'nsfw_level': None}, NsfwLevel.none
    yield {'nsfw_level': NsfwLevel.safe.value}, NsfwLevel.safe


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_nsfw_level(input_data):
    """
    Tests whether ``parse_nsfw_level`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``NsfwLevel``
    """
    output = parse_nsfw_level(input_data)
    vampytest.assert_instance(output, NsfwLevel)
    return output
