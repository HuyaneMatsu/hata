import vampytest

from ....activity import Activity, ActivityType
from ....bases import Icon, IconType
from ....color import Color
from ....guild import GuildBadge

from ...avatar_decoration import AvatarDecoration
from ...name_plate import NamePlate
from ...status_by_platform import Status, StatusByPlatform

from ..flags import UserFlag
from ..client_user_presence_base import ClientUserPBase


def test__ClientUserPBase__repr():
    """
    Tests whether ``ClientUserPBase.__repr__`` works as intended.
    """
    user_id = 202302060001
    
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160058)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030063,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180046, tag = 'miau')
    status = Status.online
    status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    user = ClientUserPBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = ClientUserPBase(
        activities = activities,
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
        status = status,
        status_by_platform = status_by_platform,
    )
    vampytest.assert_instance(repr(user), str)


def test__ClientUserPBase__hash():
    """
    Tests whether ``ClientUserPBase.__hash__`` works as intended.
    """
    user_id = 202302060002
    
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160059)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030064,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180047, tag = 'miau')
    status = Status.online
    status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    user = ClientUserPBase._create_empty(user_id)
    vampytest.assert_instance(hash(user), int)
    
    user = ClientUserPBase(
        activities = activities,
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
        status = status,
        status_by_platform = status_by_platform,
    )
    vampytest.assert_instance(hash(user), int)


def test__ClientUserPBase__eq__non_partial_and_different_object():
    """
    Tests whether ``ClientUserPBase.__eq__`` works as intended.
    
    Case: non partial and non user object.
    """
    user_id = 202504260013
    
    name = 'Orin'
    
    user = ClientUserPBase(name = name)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())
    
    test_user = ClientUserPBase._create_empty(user_id)
    vampytest.assert_eq(test_user, test_user)
    vampytest.assert_ne(user, test_user)


def _iter_options__eq():
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160036)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030065,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180009, tag = 'miau')
    status = Status.online
    status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    keyword_parameters = {
        'activities': activities,
        'avatar': avatar,
        'avatar_decoration': avatar_decoration,
        'banner': banner,
        'banner_color': banner_color,
        'bot': bot,
        'discriminator': discriminator,
        'display_name': display_name,
        'flags': flags,
        'name': name,
        'name_plate': name_plate,
        'primary_guild_badge': primary_guild_badge,
        'status': status,
        'status_by_platform': status_by_platform,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'activities': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'avatar': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'avatar_decoration': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'banner': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'banner_color': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'bot': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'discriminator': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'display_name': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': UserFlag(0),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'okuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name_plate': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'primary_guild_badge': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'status': Status.idle,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'status_by_platform': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ClientUserPBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ClientUserPBase.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    instance_0 = ClientUserPBase(**keyword_parameters_0)
    instance_1 = ClientUserPBase(**keyword_parameters_1)
    
    output = instance_0 == instance_1
    vampytest.assert_instance(output, bool)
    return output


def test__ClientUserPBase__format():
    """
    Tests whether ``ClientUserPBase.__format__`` works as intended.
    
    Case: Shallow.
    """
    activities = [Activity('orin dance', activity_type = ActivityType.playing)]
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160061)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030066,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180049, tag = 'miau')
    status = Status.online
    status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    user = ClientUserPBase(
        activities = activities,
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
        status = status,
        status_by_platform = status_by_platform,
    )
    
    vampytest.assert_instance(format(user, ''), str)


def test__ClientUserPBase__sort():
    """
    Tests whether sorting ``ClientUserPBase` works as intended.
    """
    user_id_0 = 202302080005
    user_id_1 = 202302080006
    user_id_2 = 202302080007
    
    user_0 = ClientUserPBase._create_empty(user_id_0)
    user_1 = ClientUserPBase._create_empty(user_id_1)
    user_2 = ClientUserPBase._create_empty(user_id_2)
    
    to_sort = [
        user_1,
        user_2,
        user_0,
    ]
    
    expected_output = [
        user_0,
        user_1,
        user_2,
    ]
    
    vampytest.assert_eq(sorted(to_sort), expected_output)
