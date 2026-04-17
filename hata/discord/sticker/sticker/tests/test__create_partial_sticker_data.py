import vampytest

from ..preinstanced import StickerFormat
from ..sticker import Sticker
from ..utils import create_partial_sticker_data


def test__create_partial_sticker_data():
    """
    Tests whether ``create_partial_sticker_data`` works as intended.
    """
    sticker_id = 202305250002
    name = 'koishi'
    sticker_format = StickerFormat.png
    
    sticker = Sticker.precreate(
        sticker_id,
        name = name,
        sticker_format = sticker_format,
    )
    
    expected_output = {
        'id': str(sticker_id),
        'name': name,
        'format_type': sticker_format.value,
    }
    
    vampytest.assert_eq(
        create_partial_sticker_data(sticker),
        expected_output,
    )
