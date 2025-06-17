import vampytest

from ...bases import Icon, IconType
from ...color import Color
from ...guild import GuildBadge

from ...user import AvatarDecoration, NamePlate, User, UserFlag
from ...client import Client


def test__Client__copy():
    """
    Tests whether ``Client.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160020)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030095,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180064, tag = 'meow')
    
    client = Client(
        'token_20230208_0006',
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        bot = bot,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
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
        vampytest.assert_eq(copy.bot, bot)
        vampytest.assert_eq(copy.discriminator, discriminator)
        vampytest.assert_eq(copy.display_name, display_name)
        vampytest.assert_eq(copy.flags, flags)
        vampytest.assert_eq(copy.name, name)
        vampytest.assert_eq(copy.name_plate, name_plate)
        vampytest.assert_eq(copy.primary_guild_badge, primary_guild_badge)
    
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
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030096,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180065, tag = 'meow')
    
    client = Client(
        'token_20230208_0007',
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        bot = bot,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
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
        vampytest.assert_eq(copy.bot, bot)
        vampytest.assert_eq(copy.discriminator, discriminator)
        vampytest.assert_eq(copy.display_name, display_name)
        vampytest.assert_eq(copy.flags, flags)
        vampytest.assert_eq(copy.name, name)
        vampytest.assert_eq(copy.name_plate, name_plate)
        vampytest.assert_eq(copy.primary_guild_badge, primary_guild_badge)
    
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
    old_bot = True
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'orin'
    old_name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030096,
    )
    old_primary_guild_badge = GuildBadge(guild_id = 202405180066, tag = 'meow')
    
    new_avatar = Icon(IconType.animated, 23)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160024)
    new_banner = Icon(IconType.static, 10)
    new_banner_color = Color(1236)
    new_bot = False
    new_discriminator = 1
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'okuu'
    new_name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030097,
    )
    new_primary_guild_badge = GuildBadge(guild_id = 202405180067, tag = 'miau')
    
    client = Client(
        'token_20230208_0008',
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
        bot = old_bot,
        discriminator = old_discriminator,
        display_name = old_display_name,
        flags = old_flags,
        name = old_name,
        name_plate = old_name_plate,
        primary_guild_badge = old_primary_guild_badge,
    )
    
    try:
        copy = client.copy_with(
            avatar = new_avatar,
            avatar_decoration = new_avatar_decoration,
            banner = new_banner,
            banner_color = new_banner_color,
            bot = new_bot,
            discriminator = new_discriminator,
            display_name = new_display_name,
            flags = new_flags,
            name = new_name,
            name_plate = new_name_plate,
            primary_guild_badge = new_primary_guild_badge,
        )
        vampytest.assert_instance(copy, User)
        vampytest.assert_is_not(client, copy)
        
        vampytest.assert_eq(copy.avatar, new_avatar)
        vampytest.assert_eq(copy.avatar_decoration, new_avatar_decoration)
        vampytest.assert_eq(copy.banner, new_banner)
        vampytest.assert_eq(copy.banner_color, new_banner_color)
        vampytest.assert_eq(copy.bot, new_bot)
        vampytest.assert_eq(copy.discriminator, new_discriminator)
        vampytest.assert_eq(copy.display_name, new_display_name)
        vampytest.assert_eq(copy.flags, new_flags)
        vampytest.assert_eq(copy.name, new_name)
        vampytest.assert_eq(copy.name_plate, new_name_plate)
        vampytest.assert_eq(copy.primary_guild_badge, new_primary_guild_badge)

    # Cleanup
    finally:
        client._delete()
        client = None
