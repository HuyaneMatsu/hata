from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType

from ..avatar_decoration import AvatarDecoration


def _check_is_all_fields_set(avatar_decoration):
    """
    Asserts whether all fields of the given avatar decoration are set.
    
    Parameters
    ----------
    avatar_decoration : ``AvatarDecoration``
    """
    vampytest.assert_instance(avatar_decoration, AvatarDecoration)
    vampytest.assert_instance(avatar_decoration.asset, Icon)
    vampytest.assert_instance(avatar_decoration.expires_at, DateTime, nullable = True)
    vampytest.assert_instance(avatar_decoration.sku_id, int)


def test__AvatarDecoration__new__no_fields():
    """
    Tests whether ``AvatarDecoration.__new__`` works as intended.
    
    Case: No parameters.
    """
    avatar_decoration = AvatarDecoration()
    _check_is_all_fields_set(avatar_decoration)


def test__AvatarDecoration__new__all_fields():
    """
    Tests whether ``AvatarDecoration.__new__`` works as intended.
    
    Case: all fields.
    """
    asset = Icon(IconType.static, 12)
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    sku_id = 202310160003
    
    avatar_decoration = AvatarDecoration(
        asset = asset,
        expires_at = expires_at,
        sku_id = sku_id,
    )
    _check_is_all_fields_set(avatar_decoration)
    
    vampytest.assert_eq(avatar_decoration.asset, asset)
    vampytest.assert_eq(avatar_decoration.expires_at, expires_at)
    vampytest.assert_eq(avatar_decoration.sku_id, sku_id)


def test__AvatarDecoration__create_empty():
    """
    Tests whether ``AvatarDecoration._create_empty`` works as intended.
    
    Case: No parameters.
    """
    avatar_decoration = AvatarDecoration._create_empty()
    _check_is_all_fields_set(avatar_decoration)
