import vampytest

from ..assets import ActivityAssets

from .test__ActivityAssets__constructor import _check_fields_set


def test__ActivityAssets__copy():
    """
    Tests whether ``ActivityAssets.copy`` works as intended.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    
    field = ActivityAssets(
        image_large = image_large,
        image_small = image_small,
        text_large = text_large,
        text_small = text_small,
    )
    copy = field.copy()
    _check_fields_set(copy)
    vampytest.assert_is_not(field, copy)

    vampytest.assert_eq(field, copy)



def test__ActivityAssets__copy_with__0():
    """
    Tests whether ``ActivityAssets.copy_with`` works as intended.
    
    Case: no fields given.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    
    field = ActivityAssets(
        image_large = image_large,
        image_small = image_small,
        text_large = text_large,
        text_small = text_small,
    )
    copy = field.copy_with()
    _check_fields_set(copy)
    vampytest.assert_is_not(field, copy)

    vampytest.assert_eq(field, copy)



def test__ActivityAssets__copy_with__1():
    """
    Tests whether ``ActivityAssets.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_image_large = 'plain'
    old_image_small = 'asia'
    old_text_large = 'senya'
    old_text_small = 'vocal'
    new_image_large = 'take'
    new_image_small = 'a'
    new_text_large = 'stand'
    new_text_small = 'maspark'
    
    field = ActivityAssets(
        image_large = old_image_large,
        image_small = old_image_small,
        text_large = old_text_large,
        text_small = old_text_small,
    )
    copy = field.copy_with(
        image_large = new_image_large,
        image_small = new_image_small,
        text_large = new_text_large,
        text_small = new_text_small,
    )
    _check_fields_set(copy)
    vampytest.assert_is_not(field, copy)

    vampytest.assert_eq(copy.image_large, new_image_large)
    vampytest.assert_eq(copy.image_small, new_image_small)
    vampytest.assert_eq(copy.text_large, new_text_large)
    vampytest.assert_eq(copy.text_small, new_text_small)
