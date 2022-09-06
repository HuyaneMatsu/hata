import vampytest

from .. import ActivityAssets


def test__ActivityAssets__from_data__0():
    """
    Tests whether ``ActivityAssets.from_data`` works as intended.
    
    Case: all fields given.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    
    field = ActivityAssets.from_data({
        'large_image': image_large,
        'small_image': image_small,
        'large_text': text_large,
        'small_text': text_small,
    })
    
    vampytest.assert_eq(field.image_large, image_large)
    vampytest.assert_eq(field.image_small, image_small)
    vampytest.assert_eq(field.text_large, text_large)
    vampytest.assert_eq(field.text_small, text_small)


def test__ActivityAssets__from_data__1():
    """
    Tests whether ``ActivityAssets.from_data`` works as intended.
    
    Case: no fields given.
    """
    field = ActivityAssets.from_data({})
    
    vampytest.assert_is(field.image_large, None)
    vampytest.assert_is(field.image_small, None)
    vampytest.assert_is(field.text_large, None)
    vampytest.assert_is(field.text_small, None)


def test__ActivityAssets__to_data__0():
    """
    Tests whether ``ActivityAssets.to_data`` works as intended.
    
    Case: all fields set.
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
    
    data = field.to_data()
    
    vampytest.assert_in('large_image', data)
    vampytest.assert_in('small_image', data)
    vampytest.assert_in('large_text', data)
    vampytest.assert_in('small_text', data)
    
    vampytest.assert_eq(data['large_image'], image_large)
    vampytest.assert_eq(data['small_image'], image_small)
    vampytest.assert_eq(data['large_text'], text_large)
    vampytest.assert_eq(data['small_text'], text_small)


def test__ActivityAssets__to_data__1():
    """
    Tests whether ``ActivityAssets.to_data`` works as intended.
    
    Case: no fields set.
    """
    field = ActivityAssets()
    data = field.to_data()
    
    vampytest.assert_not_in('large_image', data)
    vampytest.assert_not_in('small_image', data)
    vampytest.assert_not_in('large_text', data)
    vampytest.assert_not_in('small_text', data)
