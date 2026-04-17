import vampytest

from ..assets import ActivityAssets


def _assert_fields_set(activity_assets):
    """
    Checks whether every attribute is set of the given activity assets field.
    
    Parameters
    ----------
    activity_assets : ``ActivityAssets``
        The field to check.
    """
    vampytest.assert_instance(activity_assets, ActivityAssets)
    vampytest.assert_instance(activity_assets.image_invite_cover, str, nullable = True)
    vampytest.assert_instance(activity_assets.image_large, str, nullable = True)
    vampytest.assert_instance(activity_assets.image_small, str, nullable = True)
    vampytest.assert_instance(activity_assets.text_large, str, nullable = True)
    vampytest.assert_instance(activity_assets.text_small, str, nullable = True)
    vampytest.assert_instance(activity_assets.url_large, str, nullable = True)
    vampytest.assert_instance(activity_assets.url_small, str, nullable = True)


def test__ActivityAssets__new__no_fields():
    """
    Tests whether ``ActivityAssets.__new__`` works as intended.
    
    Case: No fields given.
    """
    activity_assets = ActivityAssets()
    _assert_fields_set(activity_assets)


def test__ActivityAssets__new__all_fields():
    """
    Tests whether ``ActivityAssets.__new__`` works as intended.
    
    Case: Fields given.
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
    _assert_fields_set(activity_assets)
    
    vampytest.assert_eq(activity_assets.image_invite_cover, image_invite_cover)
    vampytest.assert_eq(activity_assets.image_large, image_large)
    vampytest.assert_eq(activity_assets.image_small, image_small)
    vampytest.assert_eq(activity_assets.text_large, text_large)
    vampytest.assert_eq(activity_assets.text_small, text_small)
    vampytest.assert_eq(activity_assets.url_large, url_large)
    vampytest.assert_eq(activity_assets.url_small, url_small)
