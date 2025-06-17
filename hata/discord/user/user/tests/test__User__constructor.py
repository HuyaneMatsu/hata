import vampytest

from .....env import CACHE_PRESENCE

from ....activity import Activity, ActivityType
from ....bases import Icon, IconType
from ....color import Color
from ....guild import GuildBadge

from ...avatar_decoration import AvatarDecoration
from ...name_plate import NamePlate

from ..flags import UserFlag
from ..user import User
from ..preinstanced import Status


def _assert_fields_set(user):
    """
    Asserts whether every fields of the given user are set.
    
    Parameters
    ----------
    user : ``User``
        The user to check.
    """
    vampytest.assert_instance(user, User)
    vampytest.assert_instance(user.avatar, Icon)
    vampytest.assert_instance(user.avatar_decoration, AvatarDecoration, nullable = True)
    vampytest.assert_instance(user.banner, Icon)
    vampytest.assert_instance(user.banner_color, Color, nullable = True)
    vampytest.assert_instance(user.bot, bool)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.display_name, str, nullable = True)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.guild_profiles, dict)
    vampytest.assert_instance(user.id, int)
    vampytest.assert_instance(user.name, str)
    vampytest.assert_instance(user.name_plate, NamePlate, nullable = True)
    vampytest.assert_instance(user.primary_guild_badge, GuildBadge, nullable = True)
    vampytest.assert_instance(user.thread_profiles, dict, nullable = True)
    
    if CACHE_PRESENCE:
        vampytest.assert_instance(user.activities, list, nullable = True)
        vampytest.assert_instance(user.status, Status)
        vampytest.assert_instance(user.statuses, dict, nullable = True)


def test__User__precreate__no_fields():
    """
    Tests whether ``User.precreate`` works as intended.
    
    Case: No fields given.
    """
    user_id = 202302080008
    user = User.precreate(user_id)
    _assert_fields_set(user)
    vampytest.assert_eq(user.id, user_id)


def test__User__precreate__all_fields():
    """
    Tests whether ``User.precreate`` works as intended.
    
    Case: All fields given.
    """
    user_id = 202302080009
    
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160075)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030080,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180054, tag = 'meow')
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    if CACHE_PRESENCE:
        presence_keyword_parameters = {
            'activities': activities,
            'status': status,
            'statuses': statuses,
        }
    else:
        presence_keyword_parameters = {}
        
    user = User.precreate(
        user_id,
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
        **presence_keyword_parameters,
    )
    _assert_fields_set(user)
    vampytest.assert_eq(user.id, user_id)
    
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
    
    if CACHE_PRESENCE:
        vampytest.assert_eq(user.activities, activities)
        vampytest.assert_is(user.status, status)
        vampytest.assert_eq(user.statuses, statuses)


def test__User__precreate__caching():
    """
    Tests whether ``User.precreate`` works as intended.
    
    Case: Caching.
    """
    user_id = 202302080010
    user = User.precreate(user_id)
    
    test_user = User.precreate(user_id)
    vampytest.assert_is(user, test_user)
