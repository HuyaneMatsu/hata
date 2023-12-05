import vampytest

from ..fields import validate_type
from ..preinstanced import StickerType


def _iter_options__passing():
    yield None, StickerType.none
    yield StickerType.guild, StickerType.guild
    yield StickerType.guild.value, StickerType.guild


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_type(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``StickerType``
    
    Raises
    ------
    TypeError
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, StickerType)
    return output
