import vampytest

from ....bases import IconType, Icon
from ....color import Color

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
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'suika'
    
    user = OrinUserBase(
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
    )
    user.id = user_id
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
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
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'suika'
    
    user = OrinUserBase()
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'banner': banner.as_base_16_hash,
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'public_flags': int(flags),
        'username': name,
    }
    
    user._update_attributes(data)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)


def test__OrinUserBase__difference_update_attributes():
    """
    Tests whether ``OrinUserBase._difference_update_attributes` works as intended.
    """
    old_avatar = Icon(IconType.static, 24)
    old_banner = Icon(IconType.animated, 12)
    old_banner_color = Color(1236)
    old_discriminator = 2222
    old_flags = UserFlag(1)
    old_name = 'suika'
    
    new_avatar = Icon(IconType.animated, 13)
    new_banner = Icon(IconType.animated, 14)
    new_banner_color = Color(12)
    new_discriminator = 11
    new_flags = UserFlag(2)
    new_name = 'ibuki'
    
    user = OrinUserBase(
        avatar = old_avatar,
        banner = old_banner,
        banner_color = old_banner_color,
        discriminator = old_discriminator,
        flags = old_flags,
        name = old_name,
    )
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'banner': new_banner.as_base_16_hash,
        'accent_color': int(new_banner_color),
        'discriminator': str(new_discriminator).rjust(4, '0'),
        'public_flags': int(new_flags),
        'username': new_name,
    }
    
    old_attributes = user._difference_update_attributes(data)
    
    vampytest.assert_eq(user.avatar, new_avatar)
    vampytest.assert_eq(user.banner, new_banner)
    vampytest.assert_eq(user.banner_color, new_banner_color)
    vampytest.assert_eq(user.discriminator, new_discriminator)
    vampytest.assert_eq(user.flags, new_flags)
    vampytest.assert_eq(user.name, new_name)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'avatar': old_avatar,
            'banner': old_banner,
            'banner_color': old_banner_color,
            'discriminator': old_discriminator,
            'flags': old_flags,
            'name': old_name,
        },
    )
