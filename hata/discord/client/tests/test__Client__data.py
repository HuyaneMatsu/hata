import vampytest

from ...bases import IconType, Icon
from ...color import Color
from ...localization import Locale
from ...user import PremiumType, UserFlag

from ..client import Client


def test__Client__to_data():
    """
    Tests whether ``Client.to_data`` works as intended.
    
    Case: Include internals and defaults.
    """
    client_id = 202302080030
    avatar = Icon(IconType.static, 24)
    avatar_decoration = Icon(IconType.animated_apng, 25)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    bot = True
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration': avatar_decoration.as_base_16_hash,
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'banner': banner.as_base_16_hash,
        'id': str(client_id),
        'public_flags': int(flags),
        'bot': bot,
    }
    
    client = Client(
        token = 'token_20230208_0002',
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        bot = bot,
        client_id = client_id,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
    )

    try:
        vampytest.assert_eq(
            client.to_data(defaults = True, include_internals = True),
            expected_output,
        )
    
    # Cleanup
    finally:
        client._delete()
        client = None
        

def test__Client__update_attributes():
    """
    Tests whether ``Client._update_attributes` works as intended.
    """
    avatar = Icon(IconType.static, 24)
    avatar_decoration = Icon(IconType.animated_apng, 25)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa = True
    premium_type = PremiumType.nitro_basic
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration': avatar_decoration.as_base_16_hash,
        'banner': banner.as_base_16_hash,
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'public_flags': int(flags),
        'username': name,
        'email': email,
        'verified': email_verified,
        'locale': locale.value,
        'mfa_enabled': mfa,
        'premium_type': premium_type.value,
    }

    client = Client(
        token = 'token_20230208_0003',
    )
    
    try:
        client._update_attributes(data)
        
        vampytest.assert_eq(client.avatar, avatar)
        vampytest.assert_eq(client.avatar_decoration, avatar_decoration)
        vampytest.assert_eq(client.banner, banner)
        vampytest.assert_eq(client.banner_color, banner_color)
        vampytest.assert_eq(client.discriminator, discriminator)
        vampytest.assert_eq(client.display_name, display_name)
        vampytest.assert_eq(client.flags, flags)
        vampytest.assert_eq(client.name, name)
        vampytest.assert_eq(client.email, email)
        vampytest.assert_eq(client.email_verified, email_verified)
        vampytest.assert_is(client.locale, locale)
        vampytest.assert_eq(client.mfa, mfa)
        vampytest.assert_is(client.premium_type, premium_type)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Client__difference_update_attributes():
    """
    Tests whether ``Client._difference_update_attributes` works as intended.
    """
    old_avatar = Icon(IconType.static, 24)
    old_avatar_decoration = Icon(IconType.animated_apng, 25)
    old_banner = Icon(IconType.animated, 12)
    old_banner_color = Color(1236)
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'suika'
    old_email = 'rin@orindance.party'
    old_email_verified = True
    old_locale = Locale.greek
    old_mfa = True
    old_premium_type = PremiumType.nitro
    
    new_avatar = Icon(IconType.animated, 13)
    new_avatar_decoration = Icon(IconType.static, 10)
    new_banner = Icon(IconType.animated, 14)
    new_banner_color = Color(12)
    new_discriminator = 11
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'ibuki'
    new_email = 'okuu@orindance.party'
    new_email_verified = False
    new_locale = Locale.dutch
    new_mfa = False
    new_premium_type = PremiumType.nitro_classic
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'avatar_decoration': new_avatar_decoration.as_base_16_hash,
        'banner': new_banner.as_base_16_hash,
        'accent_color': int(new_banner_color),
        'discriminator': str(new_discriminator).rjust(4, '0'),
        'global_name': new_display_name,
        'public_flags': int(new_flags),
        'username': new_name,
        'email': new_email,
        'verified': new_email_verified,
        'locale': new_locale.value,
        'mfa_enabled': new_mfa,
        'premium_type': new_premium_type.value,
    }
    
    expected_output = {
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
        'mfa': old_mfa,
        'premium_type': old_premium_type,
    }
    
    client = Client(
        token = 'token_20230208_0004',
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
        mfa = old_mfa,
        premium_type = old_premium_type,
    )
    
    try:
        old_attributes = client._difference_update_attributes(data)
        
        vampytest.assert_eq(client.avatar, new_avatar)
        vampytest.assert_eq(client.avatar_decoration, new_avatar_decoration)
        vampytest.assert_eq(client.banner, new_banner)
        vampytest.assert_eq(client.banner_color, new_banner_color)
        vampytest.assert_eq(client.discriminator, new_discriminator)
        vampytest.assert_eq(client.display_name, new_display_name)
        vampytest.assert_eq(client.flags, new_flags)
        vampytest.assert_eq(client.name, new_name)
        vampytest.assert_eq(client.email, new_email)
        vampytest.assert_eq(client.email_verified, new_email_verified)
        vampytest.assert_is(client.locale, new_locale)
        vampytest.assert_eq(client.mfa, new_mfa)
        vampytest.assert_is(client.premium_type, new_premium_type)
        
        vampytest.assert_eq(
            old_attributes,
            expected_output,
        )
    
    # Cleanup
    finally:
        client._delete()
        client = None
