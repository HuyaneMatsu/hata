import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....guild import GuildBadge

from ...avatar_decoration import AvatarDecoration
from ...name_plate import NamePlate

from ..flags import UserFlag
from ..orin_user_base import OrinUserBase

from .test__OrinUserBase__constructor import _assert_fields_set


def test__OrinUserBase__copy():
    """
    Tests whether ``OrinUserBase.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160072)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030011,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180011, tag = 'miau')
    
    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
    )
    
    copy = user.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__OrinUserBase__copy_with__0():
    """
    Tests whether ``OrinUserBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160073)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030012,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180012, tag = 'miau')
    
    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
    )
    
    copy = user.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__OrinUserBase__copy_with__1():
    """
    Tests whether ``OrinUserBase.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 14)
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160074)
    old_banner = Icon(IconType.static, 15)
    old_banner_color = Color(1236)
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'orin'
    old_name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030013,
    )
    old_primary_guild_badge = GuildBadge(guild_id = 202405180013, tag = 'miau')
    
    new_avatar = Icon(IconType.animated, 23)
    new_avatar_decoration =AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160090)
    new_banner = Icon(IconType.static, 10)
    new_banner_color = Color(1236)
    new_discriminator = 1
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'okuu'
    new_name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030014,
    )
    new_primary_guild_badge = GuildBadge(guild_id = 202405180014, tag = 'meow')
    
    user = OrinUserBase(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
        discriminator = old_discriminator,
        display_name = old_display_name,
        flags = old_flags,
        name = old_name,
        name_plate = old_name_plate,
        primary_guild_badge = old_primary_guild_badge,
    )
    
    copy = user.copy_with(
        avatar = new_avatar,
        avatar_decoration = new_avatar_decoration,
        banner = new_banner,
        banner_color = new_banner_color,
        discriminator = new_discriminator,
        display_name = new_display_name,
        flags = new_flags,
        name = new_name,
        name_plate = new_name_plate,
        primary_guild_badge = new_primary_guild_badge,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.avatar_decoration, new_avatar_decoration)
    vampytest.assert_eq(copy.banner, new_banner)
    vampytest.assert_eq(copy.banner_color, new_banner_color)
    vampytest.assert_eq(copy.discriminator, new_discriminator)
    vampytest.assert_eq(copy.display_name, new_display_name)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.name_plate, new_name_plate)
    vampytest.assert_eq(copy.primary_guild_badge, new_primary_guild_badge)
