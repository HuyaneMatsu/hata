import vampytest

from ....bases import IconType, Icon
from ....color import Color

from ...avatar_decoration import AvatarDecoration
from ...user_clan import UserClan

from ..flags import UserFlag
from ..orin_user_base import OrinUserBase


def test__OrinUserBase__from_data():
    """
    Tests whether ``OrinUserBase.from_data`` works as intended.
    """
    data = {}
    
    with vampytest.assert_raises(NotImplementedError):
        OrinUserBase.from_data(data)


def test__OrinUserBase__to_data():
    """
    Tests whether ``OrinUserBase.to_data`` works as intended.
    
    Case: Include internals and defaults.
    """
    user_id = 202302040015
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160067)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    clan = UserClan(guild_id = 202405180003, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    
    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
    )
    user.id = user_id
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'clan': clan.to_data(defaults = True),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'banner': banner.as_base_16_hash,
        'id': str(user_id),
        'public_flags': int(flags),
        'bot': False,
    }
    
    vampytest.assert_eq(
        user.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__OrinUserBase__update_attributes():
    """
    Tests whether ``OrinUserBase._update_attributes` works as intended.
    """
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160069)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    clan = UserClan(guild_id = 202405180004, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    
    user = OrinUserBase()
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'banner': banner.as_base_16_hash,
        'accent_color': int(banner_color),
        'clan': clan.to_data(),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'public_flags': int(flags),
        'username': name,
    }
    
    user._update_attributes(data)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.clan, clan)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)


def test__OrinUserBase__difference_update_attributes():
    """
    Tests whether ``OrinUserBase._difference_update_attributes` works as intended.
    """
    old_avatar = Icon(IconType.static, 24)
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160070)
    old_banner = Icon(IconType.animated, 12)
    old_banner_color = Color(1236)
    old_clan = UserClan(guild_id = 202405180005, tag = 'miau')
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'suika'
    
    new_avatar = Icon(IconType.animated, 13)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160091)
    new_banner = Icon(IconType.animated, 14)
    new_banner_color = Color(12)
    new_clan = UserClan(guild_id = 202405180006, tag = 'meow')
    new_discriminator = 11
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'ibuki'
    
    user = OrinUserBase(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
        clan = old_clan,
        discriminator = old_discriminator,
        display_name = old_display_name,
        flags = old_flags,
        name = old_name,
    )
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'avatar_decoration_data': new_avatar_decoration.to_data(),
        'banner': new_banner.as_base_16_hash,
        'accent_color': int(new_banner_color),
        'clan': new_clan.to_data(),
        'discriminator': str(new_discriminator).rjust(4, '0'),
        'global_name': new_display_name,
        'public_flags': int(new_flags),
        'username': new_name,
    }
    
    old_attributes = user._difference_update_attributes(data)
    
    vampytest.assert_eq(user.avatar, new_avatar)
    vampytest.assert_eq(user.avatar_decoration, new_avatar_decoration)
    vampytest.assert_eq(user.banner, new_banner)
    vampytest.assert_eq(user.banner_color, new_banner_color)
    vampytest.assert_eq(user.clan, new_clan)
    vampytest.assert_eq(user.discriminator, new_discriminator)
    vampytest.assert_eq(user.display_name, new_display_name)
    vampytest.assert_eq(user.flags, new_flags)
    vampytest.assert_eq(user.name, new_name)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'avatar': old_avatar,
            'avatar_decoration': old_avatar_decoration,
            'banner': old_banner,
            'banner_color': old_banner_color,
            'clan': old_clan,
            'discriminator': old_discriminator,
            'display_name': old_display_name,
            'flags': old_flags,
            'name': old_name,
        },
    )
