import vampytest

from ..assets import ActivityAssets

from .test__ActivityAssets__constructor import _assert_fields_set


def test__ActivityAssets__from_data__0():
    """
    Tests whether ``ActivityAssets.from_data`` works as intended.
    
    Case: all fields given.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    
    data = {
        'large_image': image_large,
        'small_image': image_small,
        'large_text': text_large,
        'small_text': text_small,
    }
    
    field = ActivityAssets.from_data(data)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.image_large, image_large)
    vampytest.assert_eq(field.image_small, image_small)
    vampytest.assert_eq(field.text_large, text_large)
    vampytest.assert_eq(field.text_small, text_small)


def test__ActivityAssets__to_data__0():
    """
    Tests whether ``ActivityAssets.to_data`` works as intended.
    
    Case: Include defaults.
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
    
    expected_output = {
        'large_image': image_large,
        'small_image': image_small,
        'large_text': text_large,
        'small_text': text_small,
    }
    
    vampytest.assert_eq(
        field.to_data(defaults = True),
        expected_output,
    )
