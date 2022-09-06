import vampytest

from .. import ActivityAssets


def test__ActivityAssets__new__0():
    """
    Tests whether ``ActivityAssets.__new__`` defaults empty values to `None`.
    """
    field = ActivityAssets(
        image_large = '',
        image_small = '',
        text_large = '',
        text_small = '',
    )
    
    vampytest.assert_is(field.image_large, None)
    vampytest.assert_is(field.image_small, None)
    vampytest.assert_is(field.text_large, None)
    vampytest.assert_is(field.text_small, None)


def test__ActivityAssets__new__1():
    """
    Tests whether ``ActivityAssets.__new__`` sets string values as expected.
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
    
    vampytest.assert_eq(field.image_large, image_large)
    vampytest.assert_eq(field.image_small, image_small)
    vampytest.assert_eq(field.text_large, text_large)
    vampytest.assert_eq(field.text_small, text_small)
