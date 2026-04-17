import vampytest

from ..utils import create_partial_sticker_from_id


def test__create_partial_sticker_from_id__default():
    """
    Tests whether ``create_partial_sticker_from_id`` works as intended.
    
    Case: default.
    """
    sticker_id = 202402240014
    
    sticker = create_partial_sticker_from_id(sticker_id)
    
    vampytest.assert_eq(sticker.id, sticker_id)


def test__create_partial_sticker_from_id__caching():
    """
    Tests whether ``create_partial_sticker_from_id`` works as intended.
    
    Case: caching.
    """
    sticker_id = 202402240015
    
    sticker = create_partial_sticker_from_id(sticker_id)
    test_sticker = create_partial_sticker_from_id(sticker_id)
    
    vampytest.assert_is(sticker, test_sticker)
