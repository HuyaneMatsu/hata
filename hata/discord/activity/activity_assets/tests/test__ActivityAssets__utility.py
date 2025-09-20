import vampytest

from ..assets import ActivityAssets

from .test__ActivityAssets__constructor import _assert_fields_set


def test__ActivityAssets__copy():
    """
    Tests whether ``ActivityAssets.copy`` works as intended.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    url_large = 'https://orindance.party/bbo.png'
    url_small = 'https://orindance.party/llo.png'
    
    activity_assets = ActivityAssets(
        image_large = image_large,
        image_small = image_small,
        text_large = text_large,
        text_small = text_small,
        url_large = url_large,
        url_small = url_small,
    )
    copy = activity_assets.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(activity_assets, copy)

    vampytest.assert_eq(activity_assets, copy)


def test__ActivityAssets__copy_with__no_fields():
    """
    Tests whether ``ActivityAssets.copy_with`` works as intended.
    
    Case: no fields given.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    url_large = 'https://orindance.party/bbo.png'
    url_small = 'https://orindance.party/llo.png'
    
    activity_assets = ActivityAssets(
        image_large = image_large,
        image_small = image_small,
        text_large = text_large,
        text_small = text_small,
        url_large = url_large,
        url_small = url_small,
    )
    copy = activity_assets.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(activity_assets, copy)

    vampytest.assert_eq(activity_assets, copy)



def test__ActivityAssets__copy_with__all_fields():
    """
    Tests whether ``ActivityAssets.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_image_large = 'plain'
    old_image_small = 'asia'
    old_text_large = 'senya'
    old_text_small = 'vocal'
    old_url_large = 'https://orindance.party/bbo.png'
    old_url_small = 'https://orindance.party/llo.png'
    
    new_image_large = 'take'
    new_image_small = 'a'
    new_text_large = 'stand'
    new_text_small = 'maspark'
    new_url_large = 'https://orindance.party/butter.png'
    new_url_small = 'https://orindance.party/fly.png'
    
    activity_assets = ActivityAssets(
        image_large = old_image_large,
        image_small = old_image_small,
        text_large = old_text_large,
        text_small = old_text_small,
        url_large = old_url_large,
        url_small = old_url_small,
    )
    copy = activity_assets.copy_with(
        image_large = new_image_large,
        image_small = new_image_small,
        text_large = new_text_large,
        text_small = new_text_small,
        url_large = new_url_large,
        url_small = new_url_small,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(activity_assets, copy)

    vampytest.assert_eq(copy.image_large, new_image_large)
    vampytest.assert_eq(copy.image_small, new_image_small)
    vampytest.assert_eq(copy.text_large, new_text_large)
    vampytest.assert_eq(copy.text_small, new_text_small)
    vampytest.assert_eq(copy.url_large, new_url_large)
    vampytest.assert_eq(copy.url_small, new_url_small)
