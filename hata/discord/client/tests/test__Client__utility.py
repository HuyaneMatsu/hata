import vampytest

from ...bases import IconType, Icon
from ...color import Color
from ...localization import Locale
from ...user import PremiumType, UserFlag

from ..client import Client

import vampytest

from ...bases import Icon, IconType
from ...color import Color

from ...user import User, UserFlag
from ...client import Client

from .test__Client__constructor import _assert_fields_set


def test__Client__copy():
    """
    Tests whether ``Client.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    
    client = Client(
        'token_20230208_0006',
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        bot = bot,
    )
    
    try:
        copy = client.copy()
        
        vampytest.assert_instance(copy, User)
        vampytest.assert_is_not(client, copy)
        
        vampytest.assert_eq(client, copy)
        
        vampytest.assert_eq(copy.avatar, avatar)
        vampytest.assert_eq(copy.banner, banner)
        vampytest.assert_eq(copy.banner_color, banner_color)
        vampytest.assert_eq(copy.discriminator, discriminator)
        vampytest.assert_eq(copy.flags, flags)
        vampytest.assert_eq(copy.name, name)
        vampytest.assert_eq(copy.bot, bot)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Client__copy_with__0():
    """
    Tests whether ``Client.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    
    client = Client(
        'token_20230208_0007',
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        bot = bot,
    )
    
    try:
        copy = client.copy_with()
        
        vampytest.assert_instance(copy, User)
        vampytest.assert_is_not(client, copy)
        
        vampytest.assert_eq(client, copy)
        
        vampytest.assert_eq(copy.avatar, avatar)
        vampytest.assert_eq(copy.banner, banner)
        vampytest.assert_eq(copy.banner_color, banner_color)
        vampytest.assert_eq(copy.discriminator, discriminator)
        vampytest.assert_eq(copy.flags, flags)
        vampytest.assert_eq(copy.name, name)
        vampytest.assert_eq(copy.bot, bot)
    
    # Cleanup
    finally:
        client._delete()
        client = None



def test__Client__copy_with__1():
    """
    Tests whether ``Client.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 14)
    old_banner = Icon(IconType.static, 15)
    old_banner_color = Color(1236)
    old_discriminator = 2222
    old_flags = UserFlag(1)
    old_name = 'orin'
    old_bot = True
    
    new_avatar = Icon(IconType.animated, 23)
    new_banner = Icon(IconType.static, 10)
    new_banner_color = Color(1236)
    new_discriminator = 1
    new_flags = UserFlag(2)
    new_name = 'okuu'
    new_bot = False
    
    client = Client(
        'token_20230208_0008',
        avatar = old_avatar,
        banner = old_banner,
        banner_color = old_banner_color,
        discriminator = old_discriminator,
        flags = old_flags,
        name = old_name,
        bot = old_bot,
    )
    
    try:
        copy = client.copy_with(
            avatar = new_avatar,
            banner = new_banner,
            banner_color = new_banner_color,
            discriminator = new_discriminator,
            flags = new_flags,
            name = new_name,
            bot = new_bot,
        )
        vampytest.assert_instance(copy, User)
        vampytest.assert_is_not(client, copy)
        
        vampytest.assert_eq(copy.avatar, new_avatar)
        vampytest.assert_eq(copy.banner, new_banner)
        vampytest.assert_eq(copy.banner_color, new_banner_color)
        vampytest.assert_eq(copy.discriminator, new_discriminator)
        vampytest.assert_eq(copy.flags, new_flags)
        vampytest.assert_eq(copy.name, new_name)
        vampytest.assert_eq(copy.bot, new_bot)

    # Cleanup
    finally:
        client._delete()
        client = None
