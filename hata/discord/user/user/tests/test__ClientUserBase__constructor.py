import vampytest

from ....bases import Icon, IconType
from ....client import Client
from ....color import Color
from ....guild import GuildBadge

from ...avatar_decoration import AvatarDecoration
from ...guild_profile import GuildProfile
from ...name_plate import NamePlate
from ...thread_profile import ThreadProfile

from ..flags import UserFlag
from ..client_user_base import ClientUserBase


def _assert_fields_set(user):
    """
    Asserts whether every fields of the given user are set.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to check.
    """
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_instance(user.avatar, Icon)
    vampytest.assert_instance(user.avatar_decoration, AvatarDecoration, nullable = True)
    vampytest.assert_instance(user.banner, Icon)
    vampytest.assert_instance(user.banner_color, Color, nullable = True)
    vampytest.assert_instance(user.bot, bool)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.display_name, str, nullable = True)
    vampytest.assert_instance(user.guild_profiles, dict)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.id, int)
    vampytest.assert_instance(user.name, str)
    vampytest.assert_instance(user.name_plate, NamePlate, nullable = True)
    vampytest.assert_instance(user.primary_guild_badge, GuildBadge, nullable = True)
    vampytest.assert_instance(user.thread_profiles, dict, nullable = True)


def test__ClientUserBase__new__no_fields():
    """
    Tests whether ``ClientUserBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    user = ClientUserBase()
    _assert_fields_set(user)


def test__ClientUserBase__new__all_fields():
    """
    Tests whether ``ClientUserBase.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160025)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030020,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180029, tag = 'miau')
    
    user = ClientUserBase(
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
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.bot, bot)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.name_plate, name_plate)
    vampytest.assert_eq(user.primary_guild_badge, primary_guild_badge)


def test__ClientUserBase__create_empty():
    """
    Tests whether ``ClientUserBase._create_empty`` works as intended.
    """
    user_id = 202302060000
    user = ClientUserBase._create_empty(user_id)
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.id, user_id)


def test__ClientUserBase___from_client__include_internals():
    """
    Tests whether ``ClientUserBase._from_client`` works as intended.
    
    Case: Include internals.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160026)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030021,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180030, tag = 'miau')
    
    user_id = 202302060032
    guild_profiles = {202302060028: GuildProfile(nick = 'hello')}
    thread_profiles = {202302060029: ThreadProfile(flags = 2)}
    
    client = Client(
        token = 'token_20230206_0000',
        client_id = user_id,
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
        bot = bot,
    )
    try:
        client.guild_profiles = guild_profiles
        client.thread_profiles = thread_profiles
        
        user = ClientUserBase._from_client(client, True)
        _assert_fields_set(user)
        vampytest.assert_is(type(user), ClientUserBase)
            
        vampytest.assert_eq(user.avatar, avatar)
        vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
        vampytest.assert_eq(user.banner, banner)
        vampytest.assert_eq(user.banner_color, banner_color)
        vampytest.assert_eq(user.discriminator, discriminator)
        vampytest.assert_eq(user.display_name, display_name)
        vampytest.assert_eq(user.flags, flags)
        vampytest.assert_eq(user.name, name)
        vampytest.assert_eq(user.name_plate, name_plate)
        vampytest.assert_eq(user.primary_guild_badge, primary_guild_badge)
        vampytest.assert_eq(user.bot, bot)
        
        vampytest.assert_eq(user.id, user_id)
        vampytest.assert_eq(user.guild_profiles, guild_profiles)
        vampytest.assert_is_not(user.guild_profiles, guild_profiles)
        vampytest.assert_eq(user.thread_profiles, thread_profiles)
        vampytest.assert_is_not(user.thread_profiles, thread_profiles)
        
    finally:
        client._delete()
        client = None


def test__ClientUserBase___from_client__not_include_internals():
    """
    Tests whether ``ClientUserBase._from_client`` works as intended.
    
    Case: not include internals.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160027)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    primary_guild_badge = GuildBadge(guild_id = 202405180031, tag = 'miau')
    bot = True
    
    user_id = 202302060033
    guild_profiles = {202302060030: GuildProfile(nick = 'hello')}
    thread_profiles = {202302060031: ThreadProfile(flags = 2)}
    
    client = Client(
        token = 'token_20230206_0001',
        client_id = user_id,
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        primary_guild_badge = primary_guild_badge,
        bot = bot,
    )
    try:
        client.guild_profiles = guild_profiles
        client.thread_profiles = thread_profiles
        
        user = ClientUserBase._from_client(client, False)
        _assert_fields_set(user)
        vampytest.assert_is(type(user), ClientUserBase)
            
        vampytest.assert_eq(user.avatar, avatar)
        vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
        vampytest.assert_eq(user.banner, banner)
        vampytest.assert_eq(user.banner_color, banner_color)
        vampytest.assert_eq(user.discriminator, discriminator)
        vampytest.assert_eq(user.display_name, display_name)
        vampytest.assert_eq(user.flags, flags)
        vampytest.assert_eq(user.name, name)
        vampytest.assert_eq(user.primary_guild_badge, primary_guild_badge)
        vampytest.assert_eq(user.bot, bot)
        
        vampytest.assert_eq(user.id, 0)
        vampytest.assert_eq(user.guild_profiles, {})
        vampytest.assert_eq(user.thread_profiles, None)
        
    finally:
        client._delete()
        client = None
