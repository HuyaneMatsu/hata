import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....localization import Locale
from ....guild import GuildBadge
from ....user import AvatarDecoration, NamePlate, PremiumType, UserFlag

from ..oauth2_user import Oauth2User

from .test__Oauth2User__constructor import _assert_fields_set


def test__Oauth2User__copy():
    """
    Tests whether ``Oauth2User.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160047)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    email = 'rin@orindance.party'
    email_verified = True
    flags = UserFlag(1)
    locale = Locale.greek
    mfa_enabled = True
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030050,
    )
    premium_type = PremiumType.nitro
    primary_guild_badge = GuildBadge(guild_id = 202405180025, tag = 'miau')
    
    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        email = email,
        email_verified = email_verified,
        flags = flags,
        locale = locale,
        mfa_enabled = mfa_enabled,
        name = name,
        name_plate = name_plate,
        premium_type = premium_type,
        primary_guild_badge = primary_guild_badge,
    )
    
    copy = user.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__Oauth2User__copy_with__no_fields():
    """
    Tests whether ``Oauth2User.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160048)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    email = 'rin@orindance.party'
    email_verified = True
    flags = UserFlag(1)
    locale = Locale.greek
    mfa_enabled = True
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030050,
    )
    premium_type = PremiumType.nitro
    primary_guild_badge = GuildBadge(guild_id = 202405180026, tag = 'miau')
    
    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        email = email,
        email_verified = email_verified,
        flags = flags,
        locale = locale,
        mfa_enabled = mfa_enabled,
        name = name,
        name_plate = name_plate,
        premium_type = premium_type,
        primary_guild_badge = primary_guild_badge,
    )
    
    copy = user.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__Oauth2User__copy_with__all_fields():
    """
    Tests whether ``Oauth2User.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 14)
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160049)
    old_banner = Icon(IconType.static, 15)
    old_banner_color = Color(1236)
    old_discriminator = 2222
    old_display_name = 'Far'
    old_email = 'rin@orindance.party'
    old_email_verified = True
    old_flags = UserFlag(1)
    old_locale = Locale.greek
    old_mfa_enabled = True
    old_name = 'orin'
    old_name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030051,
    )
    old_premium_type = PremiumType.nitro
    old_primary_guild_badge = GuildBadge(guild_id = 202405180027, tag = 'miau')
    
    new_avatar = Icon(IconType.animated, 23)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160093)
    new_banner = Icon(IconType.static, 10)
    new_banner_color = Color(1236)
    new_discriminator = 1
    new_display_name = 'East'
    new_email = 'orin@orindance.party'
    new_email_verified = False
    new_flags = UserFlag(2)
    new_locale = Locale.greek
    new_mfa_enabled = False
    new_name = 'okuu'
    new_name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030052,
    )
    new_premium_type = PremiumType.nitro_classic
    new_primary_guild_badge = GuildBadge(guild_id = 202405180028, tag = 'meow')
    
    user = Oauth2User(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
        discriminator = old_discriminator,
        display_name = old_display_name,
        email = old_email,
        email_verified = old_email_verified,
        flags = old_flags,
        locale = old_locale,
        mfa_enabled = old_mfa_enabled,
        name = old_name,
        name_plate = old_name_plate,
        premium_type = old_premium_type,
        primary_guild_badge = old_primary_guild_badge,
    )
    
    copy = user.copy_with(
        avatar = new_avatar,
        avatar_decoration = new_avatar_decoration,
        banner = new_banner,
        banner_color = new_banner_color,
        discriminator = new_discriminator,
        display_name = new_display_name,
        email = new_email,
        email_verified = new_email_verified,
        flags = new_flags,
        mfa_enabled = new_mfa_enabled,
        locale = new_locale,
        name = new_name,
        name_plate = new_name_plate,
        premium_type = new_premium_type,
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
    vampytest.assert_eq(copy.email, new_email)
    vampytest.assert_eq(copy.email_verified, new_email_verified)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_is(copy.locale, new_locale)
    vampytest.assert_eq(copy.mfa_enabled, new_mfa_enabled)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.name_plate, new_name_plate)
    vampytest.assert_is(copy.premium_type, new_premium_type)
    vampytest.assert_eq(copy.primary_guild_badge, new_primary_guild_badge)
