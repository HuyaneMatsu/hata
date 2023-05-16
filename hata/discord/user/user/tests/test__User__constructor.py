import vampytest

from .....env import CACHE_PRESENCE

from ....activity import Activity, ActivityType
from ....bases import Icon, IconType
from ....color import Color

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
    vampytest.assert_instance(user.avatar_decoration, Icon)
    vampytest.assert_instance(user.banner, Icon)
    vampytest.assert_instance(user.banner_color, Color, nullable = True)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.display_name, str, nullable = True)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.id, int)
    vampytest.assert_instance(user.name, str)
    vampytest.assert_instance(user.bot, bool)
    vampytest.assert_instance(user.guild_profiles, dict)
    vampytest.assert_instance(user.thread_profiles, dict, nullable = True)
    
    if CACHE_PRESENCE:
        vampytest.assert_instance(user.activities, list, nullable = True)
        vampytest.assert_instance(user.status, Status)
        vampytest.assert_instance(user.statuses, dict, nullable = True)


def test__User__precreate__0():
    """
    Tests whether ``User.precreate`` works as intended.
    
    Case: No fields given.
    """
    user_id = 202302080008
    user = User.precreate(user_id)
    _assert_fields_set(user)
    vampytest.assert_eq(user.id, user_id)


def test__User__precreate__1():
    """
    Tests whether ``User.precreate`` works as intended.
    
    Case: All fields given.
    """
    user_id = 202302080009
    avatar = Icon(IconType.static, 32)
    avatar_decoration = Icon(IconType.animated_apng, 25)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    bot = True
    activities = [Activity('orin dance', activity_type = ActivityType.game)]
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
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        bot = bot,
        **presence_keyword_parameters,
    )
    _assert_fields_set(user)
    vampytest.assert_eq(user.id, user_id)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.bot, bot)
    
    if CACHE_PRESENCE:
        vampytest.assert_eq(user.activities, activities)
        vampytest.assert_is(user.status, status)
        vampytest.assert_eq(user.statuses, statuses)


def test__User__precreate__2():
    """
    Tests whether ``User.precreate`` works as intended.
    
    Case: No fields given.
    """
    user_id = 202302080010
    user = User.precreate(user_id)
    
    test_user = User.precreate(user_id)
    vampytest.assert_is(user, test_user)
