import vampytest

from ...bases import Icon, IconType
from ...color import Color

from ...user import AvatarDecoration, User, UserClan, UserFlag
from ...client import Client


def test__Client__copy():
    """
    Tests whether ``Client.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160020)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    clan = UserClan(guild_id = 202405180064, tag = 'meow')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    
    client = Client(
        'token_20230208_0006',
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
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
        vampytest.assert_eq(copy.avatar_decoration, avatar_decoration)
        vampytest.assert_eq(copy.banner, banner)
        vampytest.assert_eq(copy.banner_color, banner_color)
        vampytest.assert_eq(copy.clan, clan)
        vampytest.assert_eq(copy.discriminator, discriminator)
        vampytest.assert_eq(copy.display_name, display_name)
        vampytest.assert_eq(copy.flags, flags)
        vampytest.assert_eq(copy.name, name)
        vampytest.assert_eq(copy.bot, bot)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Client__copy_with__no_fields():
    """
    Tests whether ``Client.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160022)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    clan = UserClan(guild_id = 202405180065, tag = 'meow')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    
    client = Client(
        'token_20230208_0007',
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
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
        vampytest.assert_eq(copy.avatar_decoration, avatar_decoration)
        vampytest.assert_eq(copy.banner, banner)
        vampytest.assert_eq(copy.banner_color, banner_color)
        vampytest.assert_eq(copy.clan, clan)
        vampytest.assert_eq(copy.discriminator, discriminator)
        vampytest.assert_eq(copy.display_name, display_name)
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
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160023)
    old_banner = Icon(IconType.static, 15)
    old_banner_color = Color(1236)
    old_clan = UserClan(guild_id = 202405180066, tag = 'meow')
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'orin'
    old_bot = True
    
    new_avatar = Icon(IconType.animated, 23)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160024)
    new_banner = Icon(IconType.static, 10)
    new_banner_color = Color(1236)
    new_clan = UserClan(guild_id = 202405180067, tag = 'miau')
    new_discriminator = 1
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'okuu'
    new_bot = False
    
    client = Client(
        'token_20230208_0008',
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
        clan = old_clan,
        discriminator = old_discriminator,
        display_name = old_display_name,
        flags = old_flags,
        name = old_name,
        bot = old_bot,
    )
    
    try:
        copy = client.copy_with(
            avatar = new_avatar,
            avatar_decoration = new_avatar_decoration,
            banner = new_banner,
            banner_color = new_banner_color,
            clan = new_clan,
            discriminator = new_discriminator,
            display_name = new_display_name,
            flags = new_flags,
            name = new_name,
            bot = new_bot,
        )
        vampytest.assert_instance(copy, User)
        vampytest.assert_is_not(client, copy)
        
        vampytest.assert_eq(copy.avatar, new_avatar)
        vampytest.assert_eq(copy.avatar_decoration, new_avatar_decoration)
        vampytest.assert_eq(copy.banner, new_banner)
        vampytest.assert_eq(copy.banner_color, new_banner_color)
        vampytest.assert_eq(copy.clan, new_clan)
        vampytest.assert_eq(copy.discriminator, new_discriminator)
        vampytest.assert_eq(copy.display_name, new_display_name)
        vampytest.assert_eq(copy.flags, new_flags)
        vampytest.assert_eq(copy.name, new_name)
        vampytest.assert_eq(copy.bot, new_bot)

    # Cleanup
    finally:
        client._delete()
        client = None
