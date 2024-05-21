import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....localization import Locale
from ....user import AvatarDecoration, PremiumType, UserClan, UserFlag

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
    clan = UserClan(guild_id = 202405180025, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa_enabled = mfa_enabled,
        premium_type = premium_type,
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
    clan = UserClan(guild_id = 202405180026, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa_enabled = mfa_enabled,
        premium_type = premium_type,
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
    old_clan = UserClan(guild_id = 202405180027, tag = 'miau')
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'orin'
    old_email = 'rin@orindance.party'
    old_email_verified = True
    old_locale = Locale.greek
    old_mfa_enabled = True
    old_premium_type = PremiumType.nitro
    
    new_avatar = Icon(IconType.animated, 23)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160093)
    new_banner = Icon(IconType.static, 10)
    new_banner_color = Color(1236)
    new_clan = UserClan(guild_id = 202405180028, tag = 'meow')
    new_discriminator = 1
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'okuu'
    new_email = 'orin@orindance.party'
    new_email_verified = False
    new_locale = Locale.greek
    new_mfa_enabled = False
    new_premium_type = PremiumType.nitro_classic
    
    user = Oauth2User(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
        clan = old_clan,
        discriminator = old_discriminator,
        display_name = old_display_name,
        flags = old_flags,
        name = old_name,
        email = old_email,
        email_verified = old_email_verified,
        locale = old_locale,
        mfa_enabled = old_mfa_enabled,
        premium_type = old_premium_type,
    )
    
    copy = user.copy_with(
        avatar = new_avatar,
        avatar_decoration = new_avatar_decoration,
        banner = new_banner,
        banner_color = new_banner_color,
        clan = new_clan,
        discriminator = new_discriminator,
        display_name = new_display_name,
        flags = new_flags,
        name = new_name,
        email = new_email,
        email_verified = new_email_verified,
        mfa_enabled = new_mfa_enabled,
        locale = new_locale,
        premium_type = new_premium_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.avatar_decoration, new_avatar_decoration)
    vampytest.assert_eq(copy.banner, new_banner)
    vampytest.assert_eq(copy.banner_color, new_banner_color)
    vampytest.assert_eq(copy.clan, new_clan)
    vampytest.assert_eq(copy.discriminator, new_discriminator)
    vampytest.assert_eq(copy.display_name, new_display_name)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.email, new_email)
    vampytest.assert_eq(copy.email_verified, new_email_verified)
    vampytest.assert_is(copy.locale, new_locale)
    vampytest.assert_eq(copy.mfa_enabled, new_mfa_enabled)
    vampytest.assert_is(copy.premium_type, new_premium_type)
