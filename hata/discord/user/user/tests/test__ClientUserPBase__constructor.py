import vampytest

from ....activity import Activity, ActivityType
from ....bases import Icon, IconType
from ....client import Client
from ....color import Color
from ....guild import GuildBadge

from ...avatar_decoration import AvatarDecoration 

from ...guild_profile import GuildProfile
from ...thread_profile import ThreadProfile

from ..flags import UserFlag
from ..client_user_presence_base import ClientUserPBase
from ..preinstanced import Status


def _assert_fields_set(user):
    """
    Asserts whether every fields of the given user are set.
    
    Parameters
    ----------
    user : ``ClientUserPBase``
        The user to check.
    """
    vampytest.assert_instance(user, ClientUserPBase)
    vampytest.assert_instance(user.avatar, Icon)
    vampytest.assert_instance(user.avatar_decoration, AvatarDecoration, nullable = True)
    vampytest.assert_instance(user.banner, Icon)
    vampytest.assert_instance(user.banner_color, Color, nullable = True)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.display_name, str, nullable = True)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.id, int)
    vampytest.assert_instance(user.name, str)
    vampytest.assert_instance(user.primary_guild_badge, GuildBadge, nullable = True)
    vampytest.assert_instance(user.bot, bool)
    vampytest.assert_instance(user.guild_profiles, dict)
    vampytest.assert_instance(user.thread_profiles, dict, nullable = True)
    vampytest.assert_instance(user.activities, list, nullable = True)
    vampytest.assert_instance(user.status, Status)
    vampytest.assert_instance(user.statuses, dict, nullable = True)


def test__ClientUserPBase__new__no_fields():
    """
    Tests whether ``ClientUserPBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    user = ClientUserPBase()
    _assert_fields_set(user)


def test__ClientUserPBase__new__all_fields():
    """
    Tests whether ``ClientUserPBase.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160055)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    primary_guild_badge = GuildBadge(guild_id = 202405180043, tag = 'miau')
    bot = True
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    user = ClientUserPBase(
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
        activities = activities,
        status = status,
        statuses = statuses,
    )
    _assert_fields_set(user)
    
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
    vampytest.assert_eq(user.activities, activities)
    vampytest.assert_is(user.status, status)
    vampytest.assert_eq(user.statuses, statuses)


def test__ClientUserPBase__create_empty():
    """
    Tests whether ``ClientUserPBase._create_empty`` works as intended.
    """
    user_id = 202302070000
    user = ClientUserPBase._create_empty(user_id)
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.id, user_id)


def test_ClientUserPBase___from_client__0():
    """
    Tests whether ``ClientUserPBase._from_client`` works as intended.
    
    Case: include internals.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160056)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    primary_guild_badge = GuildBadge(guild_id = 202405180044, tag = 'miau')
    bot = True
    
    user_id = 202302070001
    guild_profiles = {2023020700002: GuildProfile(nick = 'hello')}
    thread_profiles = {202302070003: ThreadProfile(flags = 2)}
    
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    client = Client(
        token = 'token_20230207_0000',
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

    client.activities = activities
    client.status = status
    client.statuses = statuses
    
    try:
        client.guild_profiles = guild_profiles
        client.thread_profiles = thread_profiles
        
        user = ClientUserPBase._from_client(client, True)
        _assert_fields_set(user)
        vampytest.assert_is(type(user), ClientUserPBase)
            
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
        
        vampytest.assert_eq(user.id, user_id)
        vampytest.assert_eq(user.guild_profiles, guild_profiles)
        vampytest.assert_is_not(user.guild_profiles, guild_profiles)
        vampytest.assert_eq(user.thread_profiles, thread_profiles)
        vampytest.assert_is_not(user.thread_profiles, thread_profiles)
        
        vampytest.assert_eq(user.activities, activities)
        vampytest.assert_is(user.status, status)
        vampytest.assert_eq(user.statuses, statuses)
        
    finally:
        client._delete()
        client = None


def test_ClientUserPBase___from_client__1():
    """
    Tests whether ``ClientUserPBase._from_client`` works as intended.
    
    Case: not include internals.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160057)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    primary_guild_badge = GuildBadge(guild_id = 202405180045, tag = 'miau')
    bot = True
    
    user_id = 202302070004
    guild_profiles = {202302070005: GuildProfile(nick = 'hello')}
    thread_profiles = {202302070006: ThreadProfile(flags = 2)}

    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    client = Client(
        token = 'token_20230207_0001',
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
    
    client.activities = activities
    client.status = status
    client.statuses = statuses
    
    try:
        client.guild_profiles = guild_profiles
        client.thread_profiles = thread_profiles
        
        user = ClientUserPBase._from_client(client, False)
        _assert_fields_set(user)
        vampytest.assert_is(type(user), ClientUserPBase)
            
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
        
        vampytest.assert_eq(user.activities, activities)
        vampytest.assert_is(user.status, status)
        vampytest.assert_eq(user.statuses, statuses)
        
    finally:
        client._delete()
        client = None
