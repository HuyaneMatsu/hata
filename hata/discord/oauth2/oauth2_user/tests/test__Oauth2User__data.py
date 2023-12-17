import vampytest

from ....bases import IconType, Icon
from ....color import Color
from ....localization import Locale
from ....user import AvatarDecoration, PremiumType, UserFlag

from ...oauth2_access import Oauth2Access

from ..oauth2_user import Oauth2User

from .test__Oauth2User__constructor import _assert_fields_set


def test__Oauth2User__from_data():
    """
    Tests whether ``Oauth2User.from_data`` works as intended.
    """
    access = Oauth2Access()
    
    user_id = 202302040030
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160039)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'banner': banner.as_base_16_hash,
        'id': str(user_id),
        'flags': int(flags),
        'public_flags': int(flags),
        'bot': False,
        'email': email,
        'verified': email_verified,
        'locale': locale.value,
        'mfa_enabled': mfa_enabled,
        'premium_type': premium_type.value,
    }
    
    user = Oauth2User.from_data(data, access)
    _assert_fields_set(user)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_is(user.access, access)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.email, email)
    vampytest.assert_eq(user.email_verified, email_verified)
    vampytest.assert_is(user.locale, locale)
    vampytest.assert_eq(user.mfa_enabled, mfa_enabled)
    vampytest.assert_is(user.premium_type, premium_type)


def test__Oauth2User__to_data():
    """
    Tests whether ``Oauth2User.to_data`` works as intended.
    
    Case: Include internals and defaults.
    """
    user_id = 202302040023
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160040)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
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
    user.id = user_id
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'banner': banner.as_base_16_hash,
        'id': str(user_id),
        'flags': int(flags),
        'public_flags': int(flags),
        'bot': False,
        'email': email,
        'verified': email_verified,
        'locale': locale.value,
        'mfa_enabled': mfa_enabled,
        'premium_type': premium_type.value,
    }
    
    vampytest.assert_eq(
        user.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Oauth2User__update_attributes():
    """
    Tests whether ``Oauth2User._update_attributes` works as intended.
    """
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160041)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro_basic
    
    user = Oauth2User()
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'banner': banner.as_base_16_hash,
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'public_flags': int(flags),
        'username': name,
        'email': email,
        'verified': email_verified,
        'locale': locale.value,
        'mfa_enabled': mfa_enabled,
        'premium_type': premium_type.value,
    }
    
    user._update_attributes(data)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.email, email)
    vampytest.assert_eq(user.email_verified, email_verified)
    vampytest.assert_is(user.locale, locale)
    vampytest.assert_eq(user.mfa_enabled, mfa_enabled)
    vampytest.assert_is(user.premium_type, premium_type)


def test__Oauth2User__difference_update_attributes():
    """
    Tests whether ``Oauth2User._difference_update_attributes` works as intended.
    """
    old_avatar = Icon(IconType.static, 24)
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160042)
    old_banner = Icon(IconType.animated, 12)
    old_banner_color = Color(1236)
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'suika'
    old_email = 'rin@orindance.party'
    old_email_verified = True
    old_locale = Locale.greek
    old_mfa_enabled = True
    old_premium_type = PremiumType.nitro
    
    new_avatar = Icon(IconType.animated, 13)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160094)
    new_banner = Icon(IconType.animated, 14)
    new_banner_color = Color(12)
    new_discriminator = 11
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'ibuki'
    new_email = 'okuu@orindance.party'
    new_email_verified = False
    new_locale = Locale.dutch
    new_mfa_enabled = False
    new_premium_type = PremiumType.nitro_classic
    
    user = Oauth2User(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
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
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'avatar_decoration_data': new_avatar_decoration.to_data(),
        'banner': new_banner.as_base_16_hash,
        'accent_color': int(new_banner_color),
        'discriminator': str(new_discriminator).rjust(4, '0'),
        'global_name': new_display_name,
        'public_flags': int(new_flags),
        'username': new_name,
        'email': new_email,
        'verified': new_email_verified,
        'locale': new_locale.value,
        'mfa_enabled': new_mfa_enabled,
        'premium_type': new_premium_type.value,
    }
    
    old_attributes = user._difference_update_attributes(data)
    
    vampytest.assert_eq(user.avatar, new_avatar)
    vampytest.assert_eq(user.avatar_decoration, new_avatar_decoration)
    vampytest.assert_eq(user.banner, new_banner)
    vampytest.assert_eq(user.banner_color, new_banner_color)
    vampytest.assert_eq(user.discriminator, new_discriminator)
    vampytest.assert_eq(user.display_name, new_display_name)
    vampytest.assert_eq(user.flags, new_flags)
    vampytest.assert_eq(user.name, new_name)
    vampytest.assert_eq(user.email, new_email)
    vampytest.assert_eq(user.email_verified, new_email_verified)
    vampytest.assert_is(user.locale, new_locale)
    vampytest.assert_eq(user.mfa_enabled, new_mfa_enabled)
    vampytest.assert_is(user.premium_type, new_premium_type)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'avatar': old_avatar,
            'avatar_decoration': old_avatar_decoration,
            'name': old_name,
            'banner': old_banner,
            'banner_color': old_banner_color,
            'discriminator': old_discriminator,
            'display_name': old_display_name,
            'email': old_email,
            'email_verified': old_email_verified,
            'flags': old_flags,
            'locale': old_locale,
            'mfa_enabled': old_mfa_enabled,
            'premium_type': old_premium_type,
        },
    )
