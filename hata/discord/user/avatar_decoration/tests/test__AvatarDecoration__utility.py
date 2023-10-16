import vampytest

from ....bases import Icon, IconType

from ..avatar_decoration import AvatarDecoration

from .test__AvatarDecoration__constructor import _check_is_all_fields_set


def test__AvatarDecoration__copy():
    """
    Tests whether ``AvatarDecoration.copy`` works as intended.
    """
    asset = Icon(IconType.static, 12)
    sku_id = 202310160011
    
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        sku_id = sku_id,
    )
    copy = avatar_decoration.copy()
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(avatar_decoration, copy)
    vampytest.assert_eq(avatar_decoration, copy)


def test__AvatarDecoration__copy_with__no_fields():
    """
    Tests whether ``AvatarDecoration.copy_with`` works as intended.
    
    Case: No fields given.
    """
    asset = Icon(IconType.static, 12)
    sku_id = 202310160010
    
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        sku_id = sku_id,
    )
    copy = avatar_decoration.copy_with()
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(avatar_decoration, copy)
    vampytest.assert_eq(avatar_decoration, copy)


def test__AvatarDecoration__copy_with__all_fields():
    """
    Tests whether ``AvatarDecoration.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_asset = Icon(IconType.static, 12)
    old_sku_id = 202310160009
    
    new_asset = Icon(IconType.animated, 13)
    new_sku_id = 202310160008
    
    avatar_decoration = AvatarDecoration(
        asset = old_asset,
        sku_id = old_sku_id,
    )
    copy = avatar_decoration.copy_with(
        asset = new_asset,
        sku_id = new_sku_id,
    )
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(avatar_decoration, copy)

    vampytest.assert_eq(copy.asset, new_asset)
    vampytest.assert_eq(copy.sku_id, new_sku_id)
