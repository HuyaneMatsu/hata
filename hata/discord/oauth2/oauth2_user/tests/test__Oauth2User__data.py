import vampytest

from ....bases import IconType, Icon
from ....color import Color
from ....localization import Locale
from ....guild import GuildBadge
from ....user import AvatarDecoration, NamePlate, PremiumType, UserFlag

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
    email = 'rin@orindance.party'
    email_verified = True
    flags = UserFlag(1)
    locale = Locale.greek
    mfa_enabled = True
    name = 'suika'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030041,
    )
    premium_type = PremiumType.nitro
    primary_guild_badge = GuildBadge(guild_id = 202405180016, tag = 'miau')
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'banner': banner.as_base_16_hash,
        'bot': False,
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'email': email,
        'verified': email_verified,
        'flags': int(flags),
        'id': str(user_id),
        'locale': locale.value,
        'mfa_enabled': mfa_enabled,
        'username': name,
        'collectibles': {
            'nameplate': name_plate.to_data(),
        },
        'premium_type': premium_type.value,
        'primary_guild': primary_guild_badge.to_data(),
        'public_flags': int(flags),
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
    vampytest.assert_eq(user.email, email)
    vampytest.assert_eq(user.email_verified, email_verified)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_is(user.locale, locale)
    vampytest.assert_eq(user.mfa_enabled, mfa_enabled)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.name_plate, name_plate)
    vampytest.assert_is(user.premium_type, premium_type)
    vampytest.assert_eq(user.primary_guild_badge, primary_guild_badge)


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
    email = 'rin@orindance.party'
    email_verified = True
    flags = UserFlag(1)
    locale = Locale.greek
    mfa_enabled = True
    name = 'suika'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030042,
    )
    premium_type = PremiumType.nitro
    primary_guild_badge = GuildBadge(guild_id = 202405180017, tag = 'miau')
    
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
    user.id = user_id
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(defaults = True),
        'banner': banner.as_base_16_hash,
        'accent_color': int(banner_color),
        'bot': False,
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'email': email,
        'verified': email_verified,
        'flags': int(flags),
        'id': str(user_id),
        'locale': locale.value,
        'mfa_enabled': mfa_enabled,
        'username': name,
        'collectibles': {
            'nameplate': name_plate.to_data(defaults = True),
        },
        'premium_type': premium_type.value,
        'primary_guild': primary_guild_badge.to_data(defaults = True),
        'public_flags': int(flags),
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
    email = 'rin@orindance.party'
    email_verified = True
    flags = UserFlag(1)
    locale = Locale.greek
    mfa_enabled = True
    name = 'suika'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030043,
    )
    premium_type = PremiumType.nitro_basic
    primary_guild_badge = GuildBadge(guild_id = 202405180018, tag = 'miau')
    
    user = Oauth2User()
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'banner': banner.as_base_16_hash,
        'bot': False,
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'email': email,
        'verified': email_verified,
        'flags': int(flags),
        'locale': locale.value,
        'mfa_enabled': mfa_enabled,
        'username': name,
        'collectibles': {
            'nameplate': name_plate.to_data(),
        },
        'premium_type': premium_type.value,
        'primary_guild': primary_guild_badge.to_data(),
        'public_flags': int(flags),
    }
    
    user._update_attributes(data)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.email, email)
    vampytest.assert_eq(user.email_verified, email_verified)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_is(user.locale, locale)
    vampytest.assert_eq(user.mfa_enabled, mfa_enabled)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.name_plate, name_plate)
    vampytest.assert_is(user.premium_type, premium_type)
    vampytest.assert_eq(user.primary_guild_badge, primary_guild_badge)


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
    old_email = 'rin@orindance.party'
    old_email_verified = True
    old_flags = UserFlag(1)
    old_locale = Locale.greek
    old_mfa_enabled = True
    old_name = 'suika'
    old_name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030044,
    )
    old_premium_type = PremiumType.nitro
    old_primary_guild_badge = GuildBadge(guild_id = 202405180019, tag = 'miau')
    
    new_avatar = Icon(IconType.animated, 13)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160094)
    new_banner = Icon(IconType.animated, 14)
    new_banner_color = Color(12)
    new_discriminator = 11
    new_display_name = 'East'
    new_email = 'okuu@orindance.party'
    new_email_verified = False
    new_flags = UserFlag(2)
    new_locale = Locale.dutch
    new_mfa_enabled = False
    new_name = 'ibuki'
    new_name_plate = NamePlate(
        asset_path = 'koishi/koishi/eye/',
        sku_id = 202506030045,
    )
    new_premium_type = PremiumType.nitro_classic
    new_primary_guild_badge = GuildBadge(guild_id = 202405180020, tag = 'meow')
    
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
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'avatar_decoration_data': new_avatar_decoration.to_data(),
        'accent_color': int(new_banner_color),
        'banner': new_banner.as_base_16_hash,
        'bot': False,
        'discriminator': str(new_discriminator).rjust(4, '0'),
        'global_name': new_display_name,
        'email': new_email,
        'verified': new_email_verified,
        'flags': int(new_flags),
        'locale': new_locale.value,
        'mfa_enabled': new_mfa_enabled,
        'username': new_name,
        'collectibles': {
            'nameplate': new_name_plate.to_data(),
        },
        'premium_type': new_premium_type.value,
        'primary_guild': new_primary_guild_badge.to_data(),
        'public_flags': int(new_flags),
    }
    
    old_attributes = user._difference_update_attributes(data)
    
    vampytest.assert_eq(user.avatar, new_avatar)
    vampytest.assert_eq(user.avatar_decoration, new_avatar_decoration)
    vampytest.assert_eq(user.banner, new_banner)
    vampytest.assert_eq(user.banner_color, new_banner_color)
    vampytest.assert_eq(user.discriminator, new_discriminator)
    vampytest.assert_eq(user.display_name, new_display_name)
    vampytest.assert_eq(user.email, new_email)
    vampytest.assert_eq(user.email_verified, new_email_verified)
    vampytest.assert_eq(user.flags, new_flags)
    vampytest.assert_is(user.locale, new_locale)
    vampytest.assert_eq(user.mfa_enabled, new_mfa_enabled)
    vampytest.assert_eq(user.name, new_name)
    vampytest.assert_eq(user.name_plate, new_name_plate)
    vampytest.assert_is(user.premium_type, new_premium_type)
    vampytest.assert_eq(user.primary_guild_badge, new_primary_guild_badge)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'avatar': old_avatar,
            'avatar_decoration': old_avatar_decoration,
            'banner': old_banner,
            'banner_color': old_banner_color,
            'discriminator': old_discriminator,
            'display_name': old_display_name,
            'email': old_email,
            'email_verified': old_email_verified,
            'flags': old_flags,
            'locale': old_locale,
            'mfa_enabled': old_mfa_enabled,
            'name': old_name,
            'name_plate': old_name_plate,
            'premium_type': old_premium_type,
            'primary_guild_badge': old_primary_guild_badge,
        },
    )
