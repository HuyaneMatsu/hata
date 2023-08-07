import vampytest

from ..fields import parse_type
from ..preinstanced import StickerType


def _iter_options():
    yield {}, StickerType.none
    yield {'type': StickerType.guild.value}, StickerType.guild


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``StickerType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, StickerType)
    return output
