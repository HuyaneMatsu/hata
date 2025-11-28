import vampytest

from ..assets import ActivityAssets

from .test__ActivityAssets__constructor import _assert_fields_set


def test__ActivityAssets__from_data__0():
    """
    Tests whether ``ActivityAssets.from_data`` works as intended.
    
    Case: all fields given.
    """
    image_invite_cover = 'last'
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    url_large = 'https://orindance.party/bbo.png'
    url_small = 'https://orindance.party/llo.png'
    
    data = {
        'invite_cover_image': image_invite_cover,
        'large_image': image_large,
        'small_image': image_small,
        'large_text': text_large,
        'small_text': text_small,
        'large_url': url_large,
        'small_url': url_small,
    }
    
    activity_assets = ActivityAssets.from_data(data)
    _assert_fields_set(activity_assets)
    
    vampytest.assert_eq(activity_assets.image_invite_cover, image_invite_cover)
    vampytest.assert_eq(activity_assets.image_large, image_large)
    vampytest.assert_eq(activity_assets.image_small, image_small)
    vampytest.assert_eq(activity_assets.text_large, text_large)
    vampytest.assert_eq(activity_assets.text_small, text_small)
    vampytest.assert_eq(activity_assets.url_large, url_large)
    vampytest.assert_eq(activity_assets.url_small, url_small)


def test__ActivityAssets__to_data():
    """
    Tests whether ``ActivityAssets.to_data`` works as intended.
    
    Case: Include defaults.
    """
    image_invite_cover = 'last'
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    url_large = 'https://orindance.party/bbo.png'
    url_small = 'https://orindance.party/llo.png'
    
    activity_assets = ActivityAssets(
        image_invite_cover = image_invite_cover,
        image_large = image_large,
        image_small = image_small,
        text_large = text_large,
        text_small = text_small,
        url_large = url_large,
        url_small = url_small,
    )
    
    expected_output = {
        'invite_cover_image': image_invite_cover,
        'large_image': image_large,
        'small_image': image_small,
        'large_text': text_large,
        'small_text': text_small,
        'large_url': url_large,
        'small_url': url_small,
    }
    
    vampytest.assert_eq(
        activity_assets.to_data(defaults = True),
        expected_output,
    )
