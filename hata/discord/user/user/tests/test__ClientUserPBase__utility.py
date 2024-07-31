import vampytest

from ....activity import Activity, ActivityType
from ....bases import Icon, IconType
from ....color import Color

from ...avatar_decoration import AvatarDecoration
from ...user_clan import UserClan

from ..flags import UserFlag
from ..client_user_presence_base import ClientUserPBase
from ..preinstanced import Status

from .test__ClientUserPBase__constructor import _assert_fields_set


def test__ClientUserPBase__copy():
    """
    Tests whether ``ClientUserPBase.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160063)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    clan = UserClan(guild_id = 202405180050, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    user = ClientUserPBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        bot = bot,
        activities = activities,
        status = status,
        statuses = statuses,
    )
    
    copy = user.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__ClientUserPBase__copy_with__no_fields():
    """
    Tests whether ``ClientUserPBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160064)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    clan = UserClan(guild_id = 202405180051, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    user = ClientUserPBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        bot = bot,
        activities = activities,
        status = status,
        statuses = statuses,
    )
    
    copy = user.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__ClientUserPBase__copy_with__all_fields():
    """
    Tests whether ``ClientUserPBase.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 14)
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160065)
    old_banner = Icon(IconType.static, 15)
    old_banner_color = Color(1236)
    old_clan = UserClan(guild_id = 202405180052, tag = 'miau')
    old_discriminator = 2222
    old_display_name = 'Far'
    old_flags = UserFlag(1)
    old_name = 'orin'
    old_bot = True
    old_activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    old_status = Status.online
    old_statuses = {'mobile': Status.online.value}
    
    new_avatar = Icon(IconType.animated, 23)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160092)
    new_banner = Icon(IconType.static, 10)
    new_banner_color = Color(1236)
    new_clan = UserClan(guild_id = 202405180053, tag = 'meow')
    new_discriminator = 1
    new_display_name = 'East'
    new_flags = UserFlag(2)
    new_name = 'okuu'
    new_bot = False
    new_activities = [Activity('okuu dance', activity_type = ActivityType.playing)]
    new_status = Status.idle
    new_statuses = {'desktop': Status.online.value}
    
    user = ClientUserPBase(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        banner_color = old_banner_color,
        clan = old_clan,
        discriminator = old_discriminator,
        display_name = old_display_name,
        flags = old_flags,
        name = old_name,
        bot = old_bot,
        activities = old_activities,
        status = old_status,
        statuses = old_statuses,
    )
    
    copy = user.copy_with(
        avatar = new_avatar,
        avatar_decoration = new_avatar_decoration,
        banner = new_banner,
        banner_color = new_banner_color,
        clan = new_clan,
        discriminator = new_discriminator,
        display_name = new_display_name,
        flags = new_flags,
        name = new_name,
        bot = new_bot,
        activities = new_activities,
        status = new_status,
        statuses = new_statuses,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.banner, new_banner)
    vampytest.assert_eq(copy.banner_color, new_banner_color)
    vampytest.assert_eq(copy.clan, new_clan)
    vampytest.assert_eq(copy.discriminator, new_discriminator)
    vampytest.assert_eq(copy.display_name, new_display_name)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.bot, new_bot)
    vampytest.assert_eq(copy.activities, new_activities)
    vampytest.assert_eq(copy.status, new_status)
    vampytest.assert_eq(copy.statuses, new_statuses)
