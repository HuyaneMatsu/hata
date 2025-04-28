import vampytest

from ...bases import IconType, Icon
from ...color import Color
from ...guild import Guild, GuildBadge
from ...localization import Locale
from ...user import AvatarDecoration, GuildProfile, PremiumType, UserFlag

from ..client import Client


def test__Client__to_data():
    """
    Tests whether ``Client.to_data`` works as intended.
    
    Case: Include internals and defaults.
    """
    client_id = 202302080030
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160016)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    primary_guild_badge = GuildBadge(guild_id = 202405180060, tag = 'meow')
    bot = True
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'primary_guild': primary_guild_badge.to_data(defaults = True),
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
        primary_guild_badge = primary_guild_badge,
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
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160017)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    primary_guild_badge = GuildBadge(guild_id = 202405180061, tag = 'meow')
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro_basic
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'banner': banner.as_base_16_hash,
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'public_flags': int(flags),
        'username': name,
        'primary_guild': primary_guild_badge.to_data(),
        'email': email,
        'verified': email_verified,
        'locale': locale.value,
        'mfa_enabled': mfa_enabled,
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
        vampytest.assert_eq(client.primary_guild_badge, primary_guild_badge)
        vampytest.assert_eq(client.email, email)
        vampytest.assert_eq(client.email_verified, email_verified)
        vampytest.assert_is(client.locale, locale)
        vampytest.assert_eq(client.mfa_enabled, mfa_enabled)
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
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160018)
    old_banner = Icon(IconType.animated, 12)
    old_banner_color = Color(1236)
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'suika'
    old_primary_guild_badge = GuildBadge(guild_id = 202405180062, tag = 'meow')
    old_email = 'rin@orindance.party'
    old_email_verified = True
    old_locale = Locale.greek
    old_mfa_enabled = True
    old_premium_type = PremiumType.nitro
    
    new_avatar = Icon(IconType.animated, 13)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160019)
    new_banner = Icon(IconType.animated, 14)
    new_banner_color = Color(12)
    new_discriminator = 11
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'ibuki'
    new_primary_guild_badge = GuildBadge(guild_id = 202405180063, tag = 'miau')
    new_email = 'okuu@orindance.party'
    new_email_verified = False
    new_locale = Locale.dutch
    new_mfa_enabled = False
    new_premium_type = PremiumType.nitro_classic
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'avatar_decoration_data': new_avatar_decoration.to_data(),
        'banner': new_banner.as_base_16_hash,
        'accent_color': int(new_banner_color),
        'discriminator': str(new_discriminator).rjust(4, '0'),
        'global_name': new_display_name,
        'public_flags': int(new_flags),
        'username': new_name,
        'primary_guild': new_primary_guild_badge.to_data(),
        'email': new_email,
        'verified': new_email_verified,
        'locale': new_locale.value,
        'mfa_enabled': new_mfa_enabled,
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
        'mfa_enabled': old_mfa_enabled,
        'premium_type': old_premium_type,
        'primary_guild_badge': old_primary_guild_badge,
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
        primary_guild_badge = old_primary_guild_badge,
        email = old_email,
        email_verified = old_email_verified,
        locale = old_locale,
        mfa_enabled = old_mfa_enabled,
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
        vampytest.assert_eq(client.primary_guild_badge, new_primary_guild_badge)
        vampytest.assert_eq(client.email, new_email)
        vampytest.assert_eq(client.email_verified, new_email_verified)
        vampytest.assert_is(client.locale, new_locale)
        vampytest.assert_eq(client.mfa_enabled, new_mfa_enabled)
        vampytest.assert_is(client.premium_type, new_premium_type)
        
        vampytest.assert_eq(
            old_attributes,
            expected_output,
        )
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__ClientUserBase__difference_update_profile__guild_profile_missing():
    """
    Tests whether ``ClientUserBase._difference_update_profile`` works as intended.
    
    Case: guild profile missing.
    """
    client_id = 202312070012
    guild_id = 202312070013
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    data = guild_profile.to_data(defaults = True)
    
    client = Client(
        token = 'token_20231207_0012',
        client_id = client_id,
    )
    
    try:
        guild.cached_permissions_for(client)
        vampytest.assert_is_not(guild._cache_permission, None)
        
        old_attributes = client._difference_update_profile(data, guild)
        vampytest.assert_is(old_attributes, None)
        vampytest.assert_eq(guild.users, {client_id: client})
        vampytest.assert_eq(client.guild_profiles, {guild_id: guild_profile})
        vampytest.assert_is(guild._cache_permission, None)
    
    finally:
        client._delete()
        client = None
        

def test__ClientUserBase__difference_update_profile__normal_update():
    """
    Tests whether ``ClientUserBase._difference_update_profile`` works as intended.
    
    Case: Normal update.
    """
    client_id = 202312070014
    guild_id = 202312070015
    guild = Guild.precreate(guild_id)
    
    old_guild_profile = GuildProfile(nick = 'ibuki')
    new_guild_profile = GuildProfile(nick = 'suika')
    
    data = new_guild_profile.to_data(defaults = True)
    
    client = Client(
        token = 'token_20231207_0014',
        client_id = client_id,
    )
    try:
        guild.cached_permissions_for(client)
        vampytest.assert_is_not(guild._cache_permission, None)
        
        client.guild_profiles[guild_id] = old_guild_profile
        guild.users[client_id] = client
        
        old_attributes = client._difference_update_profile(data, guild)
        
        vampytest.assert_instance(old_attributes, dict)
        vampytest.assert_eq(old_attributes, {'nick': 'ibuki'})
        vampytest.assert_eq(client.guild_profiles.get(guild_id, None), new_guild_profile)
        vampytest.assert_is(guild._cache_permission, None)
    
    finally:
        client._delete()
        client = None
        


def test__ClientUserBase__update_profile__guild_profile_missing():
    """
    Tests whether ``ClientUserBase._update_profile`` works as intended.
    
    Case: guild profile missing.
    """
    client_id = 202312070016
    guild_id = 202312070017
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    data = guild_profile.to_data(defaults = True)
    
    client = Client(
        token = 'token_20231207_0016',
        client_id = client_id,
    )
    try:
        guild.cached_permissions_for(client)
        vampytest.assert_is_not(guild._cache_permission, None)
        
        output = client._update_profile(data, guild)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
        vampytest.assert_eq(guild.users, {client_id: client})
        vampytest.assert_eq(client.guild_profiles, {guild_id: guild_profile})
        vampytest.assert_is(guild._cache_permission, None)
    finally:
        client._delete()
        client = None


def test__ClientUserBase__update_profile__normal_update():
    """
    Tests whether ``ClientUserBase._update_profile`` works as intended.
    
    Case: Normal update.
    """
    client_id = 202312070018
    guild_id = 202312070019
    guild = Guild.precreate(guild_id)
    
    old_guild_profile = GuildProfile(nick = 'ibuki')
    new_guild_profile = GuildProfile(nick = 'suika')
    
    data = new_guild_profile.to_data(defaults = True)
    
    client = Client(
        token = 'token_20231207_0018',
        client_id = client_id,
    )
    
    try:
        guild.cached_permissions_for(client)
        vampytest.assert_is_not(guild._cache_permission, None)
        
        client.guild_profiles[guild_id] = old_guild_profile
        guild.users[client_id] = client
        
        output = client._update_profile(data, guild)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
        
        vampytest.assert_eq(client.guild_profiles, {guild_id: new_guild_profile})
        vampytest.assert_is(guild._cache_permission, None)
    finally:
        client._delete()
        client = None
