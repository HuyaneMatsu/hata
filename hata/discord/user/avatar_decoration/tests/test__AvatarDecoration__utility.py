from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType

from ..avatar_decoration import AvatarDecoration

from .test__AvatarDecoration__constructor import _check_is_all_fields_set


def test__AvatarDecoration__copy():
    """
    Tests whether ``AvatarDecoration.copy`` works as intended.
    """
    asset = Icon(IconType.static, 12)
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_id = 202310160011
    
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        expires_at = expires_at,
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
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_id = 202310160010
    
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        expires_at = expires_at,
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
    old_expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_sku_id = 202310160009
    
    new_asset = Icon(IconType.animated, 13)
    new_expires_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    new_sku_id = 202310160008
    
    avatar_decoration = AvatarDecoration(
        asset = old_asset,
        expires_at = old_expires_at,
        sku_id = old_sku_id,
    )
    copy = avatar_decoration.copy_with(
        asset = new_asset,
        expires_at = new_expires_at,
        sku_id = new_sku_id,
    )
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(avatar_decoration, copy)

    vampytest.assert_eq(copy.asset, new_asset)
    vampytest.assert_eq(copy.expires_at, new_expires_at)
    vampytest.assert_eq(copy.sku_id, new_sku_id)


def _iter_options__url():
    yield 202506010030, None, False
    yield 202506010031, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__url()).returning_last())
def test__AvatarDecoration__url(sku_id, icon):
    """
    Tests whether ``AvatarDecoration.url`` works as intended.
    
    Parameters
    ----------
    sku_id : `int`
        SKU identifier to create avatar decoration with.
    
    icon : ``None | Icon``
        Icon to create the avatar decoration with.
    
    Returns
    -------
    has_url : `bool`
    """
    avatar_decoration = AvatarDecoration(
        sku_id = sku_id,
        asset = icon,
    )
    
    output = avatar_decoration.url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__url_as():
    yield 202506010032, None, {'ext': 'webp', 'size': 128}, False
    yield 202506010033, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__url_as()).returning_last())
def test__AvatarDecoration__url_as(sku_id, icon, keyword_parameters):
    """
    Tests whether ``AvatarDecoration.url_as`` works as intended.
    
    Parameters
    ----------
    sku_id : `int`
        SKU identifier to create avatar decoration with.
    
    icon : ``None | Icon``
        Icon to create the avatar decoration with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    hash_url : `bool`
    """
    avatar_decoration = AvatarDecoration(
        sku_id = sku_id,
        asset = icon,
    )
    
    output = avatar_decoration.url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
