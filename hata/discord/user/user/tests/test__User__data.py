import vampytest

from ....core import USERS
from ....guild import Guild
from ....bases import Icon, IconType
from ....color import Color

from ...avatar_decoration import AvatarDecoration
from ...guild_profile import GuildProfile

from ..flags import UserFlag
from ..user import User

from .test__User__constructor import _assert_fields_set


def test__User__from_data__0():
    """
    Tests whether ``User.from_data`` works as intended.
    
    Case: User data only.
    """
    user_id = 202302080011
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160076)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    bot = True
    
    user_data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'banner': banner.as_base_16_hash,
        'id': str(user_id),
        'public_flags': int(flags),
        'bot': bot,
    }
    
    
    user = User.from_data(user_data)
    _assert_fields_set(user)
    vampytest.assert_eq(user.id, user_id)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.bot, bot)


def test__User__from_data__1():
    """
    Tests whether ``User.from_data`` works as intended.
    
    Case: Caching data only.
    """
    user_id = 202302080012
    
    user_data = {
        'id': str(user_id)
    }
    
    user = User.from_data(user_data)
    test_user = User.from_data(user_data)
    
    vampytest.assert_is(user, test_user)


def test__User__from_data__2():
    """
    Tests whether ``User.from_data`` works as intended.
    
    Case: New to guild.
    """
    user_id = 202302080012
    guild_id = 202302080013
    
    guild_profile = GuildProfile(nick = 'ibuki')
    guild = Guild.precreate(guild_id)
    
    user_data = {
        'id': str(user_id)
    }
    guild_profile_data = guild_profile.to_data(defaults = True)
    
    
    user = User.from_data(user_data, guild_profile_data, guild_id)
    _assert_fields_set(user)
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})


def test__User__from_data__3():
    """
    Tests whether ``User.from_data`` works as intended.
    
    Case: In the guild
    """
    user_id = 202302080014
    guild_id = 202302080015
    
    old_guild_profile = GuildProfile(nick = 'ibuki')
    new_guild_profile = GuildProfile(nick = 'suika')
    
    user = User.precreate(user_id)
    guild = Guild.precreate(guild_id)
    user.guild_profiles[guild_id] = old_guild_profile
    guild.users[user_id] = user
    
    user_data = {
        'id': str(user_id)
    }
    guild_profile_data = new_guild_profile.to_data(defaults = True)
    
    
    user = User.from_data(user_data, guild_profile_data, guild_id)
    _assert_fields_set(user)
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: new_guild_profile})


def test__User__from_data_and_difference_update_profile__user_missing():
    """
    Tests whether ``User._from_data_and_difference_update_profile`` works as intended.
    
    Case: User missing.
    """
    user_id = 202302080016
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160077)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    bot = True
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    user_data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'banner': banner.as_base_16_hash,
        'id': str(user_id),
        'public_flags': int(flags),
        'bot': bot,
    }
    
    data = {
        'user': user_data,
        **guild_profile.to_data(defaults = True),
    }
    
    guild_id = 202302080017
    guild = Guild.precreate(guild_id)
    
    user, old_attributes = User._from_data_and_difference_update_profile(data, guild)
    
    _assert_fields_set(user)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_is(old_attributes, None)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.bot, bot)


def test__User__from_data_and_difference_update_profile__1():
    """
    Tests whether ``User._from_data_and_difference_update_profile`` works as intended.
    
    Case: User missing -> caching.
    """
    user_id = 202302080018
    guild_id = 202302080019
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    data = {
        'user': {'id': str(user_id)},
        **guild_profile.to_data(defaults = True),
    }
    
    user, old_attributes = User._from_data_and_difference_update_profile(data, guild)
    
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})
    
    test_user, old_attributes = User._from_data_and_difference_update_profile(data, guild)
    vampytest.assert_is(user, test_user)


def test__User__from_data_and_difference_update_profile__guild_profile_missing():
    """
    Tests whether ``User._from_data_and_difference_update_profile`` works as intended.
    
    Case: guild profile missing.
    """
    user_id = 202302080020
    guild_id = 202302080021
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    user = User._create_empty(user_id)
    USERS[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **guild_profile.to_data(defaults = True),
    }
    
    output_user, old_attributes = User._from_data_and_difference_update_profile(data, guild)
    
    vampytest.assert_is(user, output_user)
    vampytest.assert_is(old_attributes, None)
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})


def test__User__from_data_and_difference_update_profile__normal_update():
    """
    Tests whether ``User._from_data_and_difference_update_profile`` works as intended.
    
    Case: Normal update.
    """
    user_id = 202302080022
    guild_id = 202302080023
    guild = Guild.precreate(guild_id)
    
    old_guild_profile = GuildProfile(nick = 'ibuki')
    new_guild_profile = GuildProfile(nick = 'suika')
    
    user = User._create_empty(user_id)
    user.guild_profiles[guild_id] = old_guild_profile
    USERS[user_id] = user
    guild.users[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **new_guild_profile.to_data(defaults = True),
    }
    
    output_user, old_attributes = User._from_data_and_difference_update_profile(data, guild)
    
    vampytest.assert_is(user, output_user)
    vampytest.assert_instance(old_attributes, dict)
    vampytest.assert_eq(old_attributes, {'nick': 'ibuki'})
    vampytest.assert_eq(user.guild_profiles.get(guild_id, None), new_guild_profile)


def test__User__from_data_and_update_profile__user_missing_cache():
    """
    Tests whether ``User._from_data_and_update_profile`` works as intended.
    
    Case: User missing + caching.
    """
    user_id = 202302080024
    guild_id = 202302080025
    avatar = Icon(IconType.static, 24)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160078)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    bot = True
    
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    user_data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'banner': banner.as_base_16_hash,
        'id': str(user_id),
        'public_flags': int(flags),
        'bot': bot,
    }
    
    data = {
        'user': user_data,
        **guild_profile.to_data(defaults = True),
    }
    
    user = User._from_data_and_update_profile(data, guild)
    
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})
    
    test_user = User._from_data_and_update_profile(data, guild)
    
    vampytest.assert_is(user, test_user)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.bot, bot)


def test__User__from_data_and_update_profile__guild_profile_missing():
    """
    Tests whether ``User._from_data_and_update_profile`` works as intended.
    
    Case: guild profile missing.
    """
    user_id = 202302080026
    guild_id = 202302080027
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    user = User._create_empty(user_id)
    USERS[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **guild_profile.to_data(defaults = True),
    }
    
    output_user = User._from_data_and_update_profile(data, guild)
    
    vampytest.assert_is(user, output_user)
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})


def test__User__from_data_and_update_profile__normal_update():
    """
    Tests whether ``User._from_data_and_update_profile`` works as intended.
    
    Case: Normal update.
    """
    user_id = 202302080028
    guild_id = 202302080029
    guild = Guild.precreate(guild_id)
    
    old_guild_profile = GuildProfile(nick = 'ibuki')
    new_guild_profile = GuildProfile(nick = 'suika')
    
    
    user = User._create_empty(user_id)
    user.guild_profiles[guild_id] = old_guild_profile
    USERS[user_id] = user
    guild.users[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **new_guild_profile.to_data(defaults = True),
    }
    
    output_user = User._from_data_and_update_profile(data, guild)
    
    vampytest.assert_is(user, output_user)
    vampytest.assert_eq(user.guild_profiles, {guild_id: new_guild_profile})
