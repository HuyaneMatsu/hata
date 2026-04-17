import vampytest

from ..preinstanced import StickerFormat
from ..utils import create_partial_sticker_from_partial_data

from .test__Sticker__constructor import _assert_fields_set


def test__create_partial_sticker_from_partial_data__default():
    """
    Tests whether ``create_partial_sticker_from_partial_data`` works as intended.
    
    Case: default.
    """
    sticker_id = 202305250003
    
    name = 'koishi'
    sticker_format = StickerFormat.png
    
    data = {
        'id': str(sticker_id),
        'name': name,
        'format_type': sticker_format.value,
    }
    
    sticker = create_partial_sticker_from_partial_data(data)
    _assert_fields_set(sticker)
    
    vampytest.assert_is(sticker.format, sticker_format)
    vampytest.assert_eq(sticker.name, name)
    
    vampytest.assert_eq(sticker.id, sticker_id)


def test__create_partial_sticker_from_partial_data__caching():
    """
    Tests whether ``create_partial_sticker_from_partial_data`` works as intended.
    
    Case: caching.
    """
    sticker_id = 202305250004

    data = {
        'id': str(sticker_id),
    }
    
    sticker = create_partial_sticker_from_partial_data(data)
    test_sticker = create_partial_sticker_from_partial_data(data)
    
    vampytest.assert_is(sticker, test_sticker)

