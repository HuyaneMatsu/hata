import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....localization import Locale
from ....user import PremiumType, UserFlag

from ..oauth2_user import Oauth2User

from .test__Oauth2User__constructor import _assert_fields_set


def test__Oauth2User__copy():
    """
    Tests whether ``Oauth2User.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = Icon(IconType.animated_apng, 25)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa = mfa,
        premium_type = premium_type,
    )
    
    copy = user.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__Oauth2User__copy_with__0():
    """
    Tests whether ``Oauth2User.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = Icon(IconType.animated_apng, 25)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa = mfa,
        premium_type = premium_type,
    )
    
    copy = user.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__Oauth2User__copy_with__1():
    """
    Tests whether ``Oauth2User.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 14)
    old_avatar_decoration = Icon(IconType.animated_apng, 25)
    old_banner = Icon(IconType.static, 15)
    old_banner_color = Color(1236)
    old_discriminator = 2222
    old_flags = UserFlag(1)
    old_name = 'orin'
    old_email = 'rin@orindance.party'
    old_email_verified = True
    old_locale = Locale.greek
    old_mfa = True
    old_premium_type = PremiumType.nitro
    
    new_avatar = Icon(IconType.animated, 23)
    new_avatar_decoration = Icon(IconType.static, 11)
    new_banner = Icon(IconType.static, 10)
    new_banner_color = Color(1236)
    new_discriminator = 1
    new_flags = UserFlag(2)
    new_name = 'okuu'
    new_email = 'orin@orindance.party'
    new_email_verified = False
    new_locale = Locale.greek
    new_mfa = False
    new_premium_type = PremiumType.nitro_classic
    
    user = Oauth2User(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
        discriminator = old_discriminator,
        flags = old_flags,
        name = old_name,
        email = old_email,
        email_verified = old_email_verified,
        locale = old_locale,
        mfa = old_mfa,
        premium_type = old_premium_type,
    )
    
    copy = user.copy_with(
        avatar = new_avatar,
        avatar_decoration = new_avatar_decoration,
        banner = new_banner,
        banner_color = new_banner_color,
        discriminator = new_discriminator,
        flags = new_flags,
        name = new_name,
        email = new_email,
        email_verified = new_email_verified,
        mfa = new_mfa,
        locale = new_locale,
        premium_type = new_premium_type,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.avatar_decoration, new_avatar_decoration)
    vampytest.assert_eq(copy.banner, new_banner)
    vampytest.assert_eq(copy.banner_color, new_banner_color)
    vampytest.assert_eq(copy.discriminator, new_discriminator)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.email, new_email)
    vampytest.assert_eq(copy.email_verified, new_email_verified)
    vampytest.assert_is(copy.locale, new_locale)
    vampytest.assert_eq(copy.mfa, new_mfa)
    vampytest.assert_is(copy.premium_type, new_premium_type)
