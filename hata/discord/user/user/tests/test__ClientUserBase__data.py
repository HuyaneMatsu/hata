import vampytest

from ....bases import IconType, Icon
from ....color import Color
from ....core import USERS
from ....guild import Guild

from ...guild_profile import GuildProfile

from ..flags import UserFlag
from ..client_user_base import ClientUserBase

from .test__ClientUserBase__constructor import _assert_fields_set


def test__ClientUserBase__from_data():
    """
    Tests whether ``ClientUserBase.from_data`` works as intended.
    """
    data = {}
    
    with vampytest.assert_raises(NotImplementedError):
        ClientUserBase.from_data(data, None, 0)


def test__ClientUserBase__to_data():
    """
    Tests whether ``ClientUserBase.to_data`` works as intended.
    
    Case: Include internals and defaults.
    """
    user_id = 202302060007
    avatar = Icon(IconType.static, 24)
    avatar_decoration = Icon(IconType.animated_apng, 25)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'suika'
    bot = True
    
    user = ClientUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        bot = bot
    )
    user.id = user_id
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration': avatar_decoration.as_base_16_hash,
        'accent_color': int(banner_color),
        'discriminator': str(discriminator).rjust(4, '0'),
        'global_name': display_name,
        'username': name,
        'banner': banner.as_base_16_hash,
        'id': str(user_id),
        'public_flags': int(flags),
        'bot': bot,
    }
    
    vampytest.assert_eq(
        user.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__ClientUserBase__difference_update_profile__0():
    """
    Tests whether ``ClientUserBase._difference_update_profile`` works as intended.
    
    Case: User missing.
    """
    user_id = 202302060008
    avatar = Icon(IconType.static, 24)
    avatar_decoration = Icon(IconType.animated_apng, 25)
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
        'avatar_decoration': avatar_decoration.as_base_16_hash,
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
    
    guild_id = 202302060009
    guild = Guild.precreate(guild_id)
    
    with vampytest.assert_raises(NotImplementedError):
        user, old_attributes = ClientUserBase._difference_update_profile(data, guild)
    
    return # sub-type only
    
    _assert_fields_set(user)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_instance(old_attributes, dict)
    vampytest.assert_eq(old_attributes, {})
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.bot, bot)


def test__ClientUserBase__difference_update_profile__1():
    """
    Tests whether ``ClientUserBase._difference_update_profile`` works as intended.
    
    Case: User missing -> caching.
    """
    user_id = 202302060010
    guild_id = 202302060011
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    data = {
        'user': {'id': str(user_id)},
        **guild_profile.to_data(defaults = True),
    }
    
    with vampytest.assert_raises(NotImplementedError):
        user, old_attributes = ClientUserBase._difference_update_profile(data, guild)
    
    return # sub-type only
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})
    
    test_user, old_attributes = ClientUserBase._difference_update_profile(data, guild)
    vampytest.assert_is(user, test_user)


def test__ClientUserBase__difference_update_profile__2():
    """
    Tests whether ``ClientUserBase._difference_update_profile`` works as intended.
    
    Case: guild profile missing.
    """
    user_id = 202302060012
    guild_id = 202302060013
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    user = ClientUserBase._create_empty(user_id)
    USERS[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **guild_profile.to_data(defaults = True),
    }
    
    output_user, old_attributes = ClientUserBase._difference_update_profile(data, guild)
    
    vampytest.assert_is(user, output_user)
    vampytest.assert_instance(old_attributes, dict)
    vampytest.assert_eq(old_attributes, {})
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})


def test__ClientUserBase__difference_update_profile__3():
    """
    Tests whether ``ClientUserBase._difference_update_profile`` works as intended.
    
    Case: Normal update.
    """
    user_id = 202302060014
    guild_id = 202302060015
    guild = Guild.precreate(guild_id)
    
    old_guild_profile = GuildProfile(nick = 'ibuki')
    new_guild_profile = GuildProfile(nick = 'suika')
    
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = old_guild_profile
    USERS[user_id] = user
    guild.users[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **new_guild_profile.to_data(defaults = True),
    }
    
    output_user, old_attributes = ClientUserBase._difference_update_profile(data, guild)
    
    vampytest.assert_is(user, output_user)
    vampytest.assert_instance(old_attributes, dict)
    vampytest.assert_eq(old_attributes, {'nick': 'ibuki'})
    vampytest.assert_eq(user.guild_profiles.get(guild_id, None), new_guild_profile)


def test__ClientUserBase__update_profile__0():
    """
    Tests whether ``ClientUserBase._update_profile`` works as intended.
    
    Case: User missing + caching.
    """
    user_id = 202302060016
    guild_id = 202302060017
    avatar = Icon(IconType.static, 24)
    avatar_decoration = Icon(IconType.animated_apng, 25)
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
        'avatar_decoration': avatar_decoration.as_base_16_hash,
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
    
    with vampytest.assert_raises(NotImplementedError):
        user = ClientUserBase._update_profile(data, guild)
    
    return # sub-type only
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})
    
    test_user = ClientUserBase._update_profile(data, guild)
    
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


def test__ClientUserBase__update_profile__1():
    """
    Tests whether ``ClientUserBase._update_profile`` works as intended.
    
    Case: guild profile missing.
    """
    user_id = 202302060018
    guild_id = 202302060019
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    user = ClientUserBase._create_empty(user_id)
    USERS[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **guild_profile.to_data(defaults = True),
    }
    
    output_user = ClientUserBase._update_profile(data, guild)
    
    vampytest.assert_is(user, output_user)
    vampytest.assert_eq(guild.users, {user_id: user})
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})


def test__ClientUserBase__update_profile__2():
    """
    Tests whether ``ClientUserBase._update_profile`` works as intended.
    
    Case: Normal update.
    """
    user_id = 202302060020
    guild_id = 202302060021
    guild = Guild.precreate(guild_id)
    
    old_guild_profile = GuildProfile(nick = 'ibuki')
    new_guild_profile = GuildProfile(nick = 'suika')
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = old_guild_profile
    USERS[user_id] = user
    guild.users[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **new_guild_profile.to_data(defaults = True),
    }
    
    output_user = ClientUserBase._update_profile(data, guild)
    
    vampytest.assert_is(user, output_user)
    vampytest.assert_eq(user.guild_profiles, {guild_id: new_guild_profile})


def test__ClientUserBase__bypass_no_cache__0():
    """
    Tests whether ``ClientUserBase._bypass_no_cache`` works as intended.
    
    Case: user missing.
    """
    user_id = 202302060022
    guild_id = 202302060023
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    user = ClientUserBase._create_empty(user_id)
    
    data = {
        'user': {'id': str(user_id)},
        **guild_profile.to_data(defaults = True),
    }
    
    ClientUserBase._bypass_no_cache(data, guild)
    
    vampytest.assert_eq(user.guild_profiles, {})
    vampytest.assert_eq(guild.users, {})


def test__ClientUserBase__bypass_no_cache__1():
    """
    Tests whether ``ClientUserBase._bypass_no_cache`` works as intended.
    
    Case: user existing.
    """
    user_id = 202302060024
    guild_id = 202302060025
    guild = Guild.precreate(guild_id)
    
    guild_profile = GuildProfile(nick = 'ibuki')
    
    user = ClientUserBase._create_empty(user_id)
    USERS[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **guild_profile.to_data(defaults = True),
    }
    
    ClientUserBase._bypass_no_cache(data, guild)
    
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})
    vampytest.assert_eq(guild.users, {user_id: user})


def test__ClientUserBase__bypass_no_cache__2():
    """
    Tests whether ``ClientUserBase._bypass_no_cache`` works as intended.
    
    Case: guild profile existing.
    """
    user_id = 202302060026
    guild_id = 202302060027
    guild = Guild.precreate(guild_id)
    
    old_guild_profile = GuildProfile(nick = 'ibuki')
    new_guild_profile = GuildProfile(nick = 'suika')
    
    user = ClientUserBase._create_empty(user_id)
    user.guild_profiles[guild_id] = old_guild_profile
    USERS[user_id] = user
    guild.users[user_id] = user
    
    data = {
        'user': {'id': str(user_id)},
        **new_guild_profile.to_data(defaults = True),
    }
    
    ClientUserBase._bypass_no_cache(data, guild)
    
    vampytest.assert_eq(user.guild_profiles, {guild_id: new_guild_profile})
    vampytest.assert_eq(guild.users, {user_id: user})
